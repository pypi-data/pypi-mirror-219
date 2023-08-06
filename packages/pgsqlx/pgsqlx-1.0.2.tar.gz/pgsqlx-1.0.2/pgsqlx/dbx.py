import os
import re
from typing import Mapping
from jinja2 import Template
from .log_support import logger, sql_id_log, page_sql_id_log
from .support import get_named_sql_args, SqlModel, MapperError, is_dynamic_sql, get_batch_args, SqlAction
from .db import do_get, do_query, do_query_one, do_execute, do_select_page, do_select, do_select_one, do_query_page, init_db as _init_db, \
    get_connection as _get_connection, insert as _insert, save as _save, batch_insert as _batch_insert, batch_execute as _batch_execute, do_save

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

_SQL_CONTAINER = dict()
_valid_sql_actions = (SqlAction.INSERT.value, SqlAction.UPDATE.value, SqlAction.DELETE.value, SqlAction.SELECT.value)


def init_db(person='root', password='', database='test', host='127.0.0.1', port=3306, show_sql=False, mapper_path='mapper', **kwargs):
    load_mapper(mapper_path)
    _init_db(person, password, database, host, port, show_sql, **kwargs)


def insert(table: str, **kwargs):
    """
    Insert data into table, return effect rowcount.
    :param table: table name
    :param kwargs: {'name': '张三', 'age': 20}
    return: Effect rowcount
    """
    return _insert(table, **kwargs)


def save(table: str, **kwargs):
    """
    Insert data into table, return primary key.
    :param table: table name
    :param kwargs: {'name': '张三', 'age': 20}
    :return: Primary key
    """
    return _save(table, **kwargs)


def mapper_save(sql_id: str, *args, **kwargs):
    """
    Execute insert SQL, return primary key.
    :return: Primary key
    """
    sql_id_log('dbx.mapper_save', sql_id, *args, **kwargs)
    sql_model = get_sql_model(sql_id)
    pk_seq = sql_model.pk_seq
    if 'pk_seq' in kwargs:
        pk_seq = kwargs.pop('pk_seq')
    sql, args = do_get_sql(sql_model, False, None, *args, **kwargs)
    assert SqlAction.INSERT.value in sql.lower(), 'Only insert sql can return primary key.'
    if not pk_seq:
        table = re.search('(?<=into )\w+', sql.lower())
        pk_seq = "{}_id_seq".format(table.group())
        logger.warning("Exec func 'mysqlx.dbx.mapper_save': 'pk_seq' is None, will use default '{}'.".format(pk_seq))

    return do_save(pk_seq, sql, *args)


def execute(sql_id: str, *args, **kwargs):
    """
    Execute SQL.
    sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO person(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('dbx.execute', sql_id, *args, **kwargs)
    sql, args = get_sql(sql_id, *args, **kwargs)
    return do_execute(sql, *args)


def batch_insert(table: str, *args):
    """
    Batch insert
    :param table: table name
    :param args: All number must have same key. [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    return _batch_insert(table, *args)


def batch_execute(sql_id: str, *args):
    """
    Batch execute
    sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: [('张三', 20), ('李四', 28)]
         INSERT INTO person(name, age) VALUES(:name,:age)  -->  args: [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    logger.debug("Exec func 'mysqlx.dbx.%s' \n\t sql_id: '%s' \n\t args: %s" % ('batch_execute', sql_id, args))
    args = get_batch_args(*args)
    sql, _ = do_get_sql(get_sql_model(sql_id), True, None, *args)
    return _batch_execute(sql, *args)


# ----------------------------------------------------------Query function------------------------------------------------------------------
def get(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' behind the sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('get', sql_id, *args, **kwargs)
    sql, args = get_sql(sql_id, *args, **kwargs)
    return do_get(sql, *args)


def query(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('query', sql_id, *args, **kwargs)
    sql, args = get_sql(sql_id, *args, **kwargs)
    return do_query(sql, *args)


def query_one(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(dict). Automatically add 'limit ?' behind the sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('query_one', sql_id, *args, **kwargs)
    sql, args = get_sql(sql_id, *args, **kwargs)
    return do_query_one(sql, *args)


def select(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('select', sql_id, *args, **kwargs)
    sql, args = get_sql(sql_id, *args, **kwargs)
    return do_select(sql, *args)


def select_one(sql_id: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(tuple). Automatically add 'limit ?' behind the sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql_id_log('select_one', sql_id, *args, **kwargs)
    sql, args = get_sql(sql_id, *args, **kwargs)
    return do_select_one(sql, *args)


def query_page(sql_id: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    page_sql_id_log('query_page', sql_id, page_num, page_size, *args, **kwargs)
    sql, args = get_sql(sql_id, *args, **kwargs)
    return do_query_page(sql, page_num, page_size, *args)


def select_page(sql_id: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    page_sql_id_log('select_page', sql_id, page_num, page_size, *args, **kwargs)
    sql, args = get_sql(sql_id, *args, **kwargs)
    return do_select_page(sql, page_num, page_size, *args)


def get_connection():
    return _get_connection()


def get_sql(sql_id: str, *args, **kwargs):
    sql_model = get_sql_model(sql_id)
    return do_get_sql(sql_model, False, None, *args, **kwargs)


def do_get_sql(sql_model, batch, param_names, *args, **kwargs):
    """
    Get sql from SqlModel.
    :param sql_model: SqlModel
    :param batch: bool, is batch or not
    :param param_names: original function parameter names
    :param args:
    :param kwargs:
    :return:
    """
    if sql_model.dynamic:
        if not kwargs:
            raise MapperError("Parameter 'kwargs' must not be empty when named mapping sql.")
        sql = sql_model.sql.render(**kwargs)
        logger.debug("Original sql: {}".format(sql))
        return get_named_sql_args(sql, **kwargs)
    else:
        logger.debug("Original sql: {}".format(sql_model.sql))
        if sql_model.mapping and kwargs:
            return get_named_sql_args(sql_model.sql, **kwargs)
        elif sql_model.placeholder and kwargs:
            logger.warning("Better use 'func(arg1, arg2...)' then 'func(arg1=arg1, arg2=arg2...)' if sql contain '?' placeholder.")
            args = [kwargs[name] for name in param_names if name in kwargs] if param_names else list(kwargs.values())
        elif sql_model.mapping and not kwargs and (not batch or
                                                   (batch and (not args or not isinstance(args[0], Mapping)))):  # batch_execute时args可能为List[Mapping]
            raise MapperError("Parameter 'kwargs' must not be empty when named mapping sql.")
        return sql_model.sql, args


def build_sql_id(namespace, _id):
    return namespace + "." + _id


def get_sql_model(sql_id: str):
    global _SQL_CONTAINER
    return _SQL_CONTAINER[sql_id]


# ----------------------------------------------------------Load mapper--------------------------------------------------------------------
def load_mapper(path: str):
    if os.path.isfile(path) and path.endswith(".xml"):
        _parse_mapper_file(path)
    elif os.path.isdir(path):
        for f in os.listdir(path):
            file = os.path.join(path, f)
            if os.path.isfile(file) and f.endswith(".xml"):
                _parse_mapper_file(file)
            elif os.path.isdir(file):
                load_mapper(file)


def _parse_mapper_file(file: str):
    global _SQL_CONTAINER
    tree = ET.parse(file)
    root = tree.getroot()
    namespace = root.attrib.get('namespace', '')
    results = list(map(lambda child: _load_sql(namespace, child, file), root))
    sql_ids, file_all_includes = zip(*results)
    for i, includes in enumerate(file_all_includes):
        if includes:
            for include in includes:
                if include not in sql_ids:
                    raise MapperError("Include '%s' are not exist in mapper file: %s" % (include, file))

                include_sql_id = build_sql_id(namespace, include)
                include_sql_model = _SQL_CONTAINER[include_sql_id]
                if include_sql_model.includes:
                    raise MapperError("Nested include: '%s' include '%s' and it include %s in mapper file: %s" % (
                        sql_ids[i], include, include_sql_model.includes, file))

    # include sql
    include_results = filter(lambda x: x[1] is not None, results)
    for sql_id, includes in include_results:
        _handle_includes(build_sql_id(namespace, sql_id), includes)

    # dynamic sql change to Template
    for sql_id in sql_ids:
        sql_model = _SQL_CONTAINER[build_sql_id(namespace, sql_id)]
        if sql_model.dynamic:
            sql_model.sql = Template(sql_model.sql)


def _handle_includes(sql_id, includes):
    is_dynamic = False
    sql_model = _SQL_CONTAINER[sql_id]
    for include in includes:
        include_sql_id = build_sql_id(sql_model.namespace, include)
        include_sql_model = _SQL_CONTAINER[include_sql_id]
        if include_sql_model.dynamic:
            is_dynamic = True
        if include_sql_model.includes:
            _handle_includes(include_sql_id, include_sql_model.includes)
        sql = re.sub(r'{{\s*%s\s*}}' % include, include_sql_model.sql, sql_model.sql)

    _valid_sql(sql_id, sql, sql_model.action)
    if is_dynamic or is_dynamic_sql(sql):
        sql_model.dynamic = True
        sql_model.mapping = True
        sql_model.placeholder = False
    else:
        sql_model.mapping = ':' in sql
        sql_model.placeholder = False if sql_model.mapping else '?' in sql
    sql_model.sql = sql
    sql_model.includes = None


def _load_sql(namespace, child, file):
    global _SQL_CONTAINER
    includes = None
    _id = child.attrib.get('id')
    assert _id, "Mapper 'id' must be set in mapper file: %s." % file
    sql_id = build_sql_id(namespace, _id)
    assert sql_id not in _SQL_CONTAINER, "Sql id '%s' repeat." % sql_id
    include = child.attrib.get('include')
    sql = child.text.strip()
    if include:
        includes = include.split(",")
        for include in set(includes):
            assert include != _id, "Include must not be it self, id: '%s' = include: '%s' " % (_id, include)
        _SQL_CONTAINER[sql_id] = SqlModel(sql=sql, action=child.tag, namespace=namespace, includes=includes, pk_seq=child.attrib.get('pk_seq'))
    elif is_dynamic_sql(sql):
        _valid_sql(sql_id, sql, child.tag)
        _SQL_CONTAINER[sql_id] = SqlModel(sql=sql, action=child.tag, namespace=namespace, dynamic=True, pk_seq=child.attrib.get('pk_seq'))
    else:
        _valid_sql(sql_id, sql, child.tag)
        _SQL_CONTAINER[sql_id] = SqlModel(sql=sql, action=child.tag, namespace=namespace, pk_seq=child.attrib.get('pk_seq'))

    return _id, includes


def _valid_sql(sql_id, sql, tag):
    assert tag in _valid_sql_actions and tag in sql.lower(), "Sql id: '{}' has not '{}' key word in {} sql.".format(sql_id, tag, tag)
