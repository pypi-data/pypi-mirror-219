import sys
from datetime import datetime
from .snowflake import get_id
from enum import Enum, IntEnum
from functools import lru_cache
from .support import DBError, simple_sql, NotFoundError
from typing import Sequence, Union, List, Tuple
from .constant import LIMIT_1, NO_LIMIT, DEFAULT_PK_FIELD, SYMBOLS, BETWEEN, LIKE, IN, PK, PK_SEQ, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG, \
    PK_STRATEGY, COLUMN_SQL, CONFIG_DICT, CACHE_SIZE
from .db import do_get_limit, do_query, do_query_one_limit, do_execute, insert, save, do_select, do_select_one_limit, transaction, batch_insert, \
    do_query_page, do_select_page, do_get
from .log_support import logger, orm_page_log, orm_insert_log, orm_by_log, orm_delete_by_id_log, orm_by_page_log, orm_inst_log, orm_find_by_id_log, \
    orm_logical_delete_by_ids_log, orm_count_log, orm_find_log, orm_find_by_ids_log


class DelFlag(IntEnum):
    UN_DELETE = 0
    DELETED = 1


class PkStrategy(Enum):
    """
    SNOWFLAKE: 由Snowflake算法生成主键
    DB_AUTO_INCREMENT: 由数据库的AUTO_INCREMENT自动生成主键

    在Windows上，使用Snowflake可能会报下列错误，这是因为Snowflake生成的id是15位的数字，而Windows上C语言的long类型是32位的
    OverflowError: Python int too large to convert to C long

    如果用的是mysql.connector，且在Windows上开发测试，可以就在初始化数据库的时候加上参数'use_pure'为True用纯python的connect; 在linux是部署生成环境时去掉'use_pure'用
    C语言写的connect, 以提高性能.
    """
    SNOWFLAKE = 'snowflake'
    DB_AUTO_INCREMENT = 'db_auto_increment'


class Model:
    """
    Create a class extends Model:

    class Person(Model):
        __pk__ = 'id'
        __table__ = 'person'
        __update_by__ = 'update_by'
        __update_time__ = 'update_time'
        __del_flag__ = 'del_flag'
        __pk_seq__ = 'person_id_seq'

        def __init__(self, id: int = None, name: str = None, age: int = None, update_by: int = None, update_time: datetime = None, del_flag: int = None):
            self.id = id
            self.update_by = update_by
            self.update_time = update_time
            self.del_flag = del_flag
            self.name = name
            self.age = age

    then you can use like follow:
        db.init_db(person='xxx', password='xxx', database='xxx', host='xxx', ...)  # or dbx.init_db(...) init db first,
        person = Person(name='张三', age=55)
        effect_rowcount = person.persist()
        id = person.inst_save()
    """

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if not k.startswith("__")})

    def __getattr__(self, name):
        if PK == name:
            return self._get_pk()
        elif TABLE == name:
            return self._get_table()
        elif UPDATE_BY == name:
            return self._get_update_by_field()
        elif UPDATE_TIME == name:
            return self._get_update_time_field()
        else:
            return None

    def persist(self):
        """
        person = Person(name='张三', age=55)
        effect_rowcount = person.persist()
        :return: effect rowcount
        """
        orm_inst_log('persist', self.__class__.__name__)
        kv = {k: v for k, v in self.__dict__.items() if v is not None}
        return self.insert(**kv)

    def inst_save(self):
        """
        person = Person(name='张三', age=55)
        id = person.save()
        :return: Primary key
        """
        orm_inst_log('inst_save', self.__class__.__name__)
        kv = {k: v for k, v in self.__dict__.items() if v is not None}
        pk = self._get_pk()
        _id = self.save(**kv)
        if pk not in kv:
            self.__dict__.update({pk: _id})
        return _id

    def update(self, ignored_none=True):
        """
        person = Person(id=1, name='李四', age=66)
        rowcount = person.update()
        :return: Effect rowcount
        """
        orm_inst_log('update', self.__class__.__name__)
        pk, table = self._get_pk_and_table()
        if ignored_none:
            kv = {k: v for k, v in self.__dict__.items() if v is not None}
        else:
            kv = {k: v for k, v in self.__dict__.items()}
        _id = kv[pk]
        assert _id is not None, 'Primary key must not be None.'
        update_kv = {k: v for k, v in kv.items() if k != pk}
        if update_kv:
            return self.update_by_id(_id, **update_kv)
        else:
            logger.warning("Exec func 'mysqlx.orm.Model.%s' not set fields, Class: '%s:'\n\t   %s" % ('update', self.__class__.__name__, self))
            return 0

    def load(self, *fields):
        """
        Return new object from database and update itself.
        :param fields: Default select all fields if not set. like: ('id', 'name', 'age')
        person = Person(id=1)
        person2 = person.load()
        """
        logger.debug("Exec func 'mysqlx.orm.Model.%s', Class: '%s', fields: %s" % ('load', self.__class__.__name__, fields))
        pk = self._get_pk()
        kv = self.__dict__
        _id = kv.get(pk)
        assert _id is not None, 'Primary key must not be None.'
        if not fields:
            fields, _ = zip(*kv.items())
        result = self.query_by_id(_id, *fields)
        if result:
            self.__dict__.update(result)
            return self
        else:
            raise NotFoundError("Load not found from db, Class: '%s', %s=%d." % (self.__class__.__name__, pk, _id))

    def logical_delete(self):
        """
        Logic delete only update the del flag
        person = Person(id=1)
        rowcount = person.logical_delete()
        """
        orm_inst_log('logical_delete', self.__class__.__name__)
        pk = self._get_pk()
        kv = self.__dict__
        _id = kv.get(pk)
        assert _id is not None, 'Primary key must not be None.'
        update_by = kv.get(self._get_update_by_field())
        return self.logical_delete_by_id(_id, update_by)

    def un_logical_delete(self):
        """
        Logic un delete only update the del flag
        person = Person(id=1)
        rowcount = person.un_logical_delete()
        """
        orm_inst_log('un_logical_delete', self.__class__.__name__)
        pk = self._get_pk()
        kv = self.__dict__
        _id = kv.get(pk)
        assert _id is not None, 'Primary key must not be None.'
        update_by = kv.get(self._get_update_by_field())
        return self.un_logical_delete_by_id(_id, update_by)

    def delete(self):
        """
        Physical delete
        person = Person(id=1)
        rowcount = person.delete()
        """
        orm_inst_log('delete', self.__class__.__name__)
        pk = self._get_pk()
        _id = self.__dict__.get(pk)
        assert _id is not None, 'Primary key must not be None.'
        return self.delete_by_id(_id)

    # ----------------------------------------------------------Class method------------------------------------------------------------------
    @classmethod
    def insert(cls, **kwargs):
        """
        rowcount = Person.insert(name='张三', age=20)
        return: Effect rowcount
        """
        orm_insert_log('insert', cls.__name__, **kwargs)
        pk, table = cls._get_pk_and_table()
        pk_strategy = cls._get_pk_strategy()
        if pk_strategy == PkStrategy.SNOWFLAKE and pk not in kwargs:
            kwargs[pk] = get_id()
        return insert(table, **kwargs)

    @classmethod
    def save(cls, **kwargs):
        """
        id = Person.save(name='张三', age=20)
        :return: Primary key
        """
        orm_insert_log('save', cls.__name__, **kwargs)
        pk, table = cls._get_pk_and_table()
        pk_strategy = cls._get_pk_strategy()
        if pk_strategy == PkStrategy.SNOWFLAKE:
            if pk in kwargs:
                _id = kwargs[pk]
            else:
                _id = get_id()
                kwargs[pk] = _id
            insert(table, **kwargs)
        else:
            kwargs['pk_seq'] = cls._get_pk_seq()
            _id = save(table, **kwargs)
        return _id

    @classmethod
    def create(cls, **kwargs):
        """
        person = Person.create(name='张三', age=20)
        :return: Instance object
        """
        orm_insert_log('create', cls.__name__, **kwargs)
        pk = cls._get_pk()
        _id = cls.save(**kwargs)
        if pk not in kwargs:
            kwargs[pk] = _id
        return cls.to_obj(**kwargs)

    @classmethod
    def update_by_id(cls, _id: Union[int, str], **kwargs):
        """
        rowcount = Person.update_by_id(id=1, name='王五')
        return: Effect rowcount
        """
        logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', id: %d, kwargs: %s" % ('update_by_id', cls.__name__, _id, kwargs))
        assert kwargs, 'Must set update kv'
        pk = cls._get_pk()
        where = '%s=?' % pk
        cols, args = zip(*kwargs.items())
        sql, update_time_arg = cls._update_sql(where, *cols)
        if update_time_arg:
            args = [*args, update_time_arg]
        return do_execute(sql, *args, _id)

    @classmethod
    def logical_delete_by_id(cls, _id: Union[int, str], update_by: Union[int, str] = None):
        """
        Logic delete only update the del flag
        rowcount = Person.delete_by_id(id=1, update_by=100)
        return: Effect rowcount
        """
        orm_delete_by_id_log('logical_delete_by_id', cls.__name__, _id, update_by)
        return cls._logical_delete_by_id_op(_id, update_by, DelFlag.DELETED)

    @classmethod
    def un_logical_delete_by_id(cls, _id: Union[int, str], update_by: Union[int, str] = None):
        """
        Logic delete only update the del flag
        rowcount = Person.un_logical_delete_by_id(id=1, update_by=100)
        return: Effect rowcount
        """
        orm_delete_by_id_log('un_logical_delete_by_id', cls.__name__, _id, update_by)
        return cls._logical_delete_by_id_op(_id, update_by, DelFlag.UN_DELETE)

    @classmethod
    def logical_delete_by_ids(cls, ids: Union[Sequence[int], Sequence[str]], update_by: Union[int, str] = None, batch_size=128):
        """
        Logic delete only update the del flag
        rowcount = Person.logical_delete_by_ids(id=[1,2], update_by=100)
        return: Effect rowcount
        """
        orm_logical_delete_by_ids_log('logical_delete_by_ids', cls.__name__, ids, update_by, batch_size)
        return cls._logical_delete_by_ids_op(ids, update_by=update_by, batch_size=batch_size, del_status=DelFlag.DELETED)

    @classmethod
    def un_logical_delete_by_ids(cls, ids: Union[Sequence[int], Sequence[str]], update_by: Union[int, str] = None, batch_size=128):
        """
        Logic delete only update the del flag
        rowcount = Person.un_logical_delete_by_ids(id=[1,2], update_by=100)
        return: Effect rowcount
        """
        orm_logical_delete_by_ids_log('un_logical_delete_by_ids', cls.__name__, ids, update_by, batch_size)
        return cls._logical_delete_by_ids_op(ids, update_by=update_by, batch_size=batch_size, del_status=DelFlag.UN_DELETE)

    @classmethod
    def delete_by(cls, where: str, *args, **kwargs):
        """
        Physical delete
        rowcount = Person.delete_by('where name=? and age=?', '张三', 55)
        return: Effect rowcount
        """
        orm_by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args, **kwargs)
        assert where.lower().startswith('where'), "Must start with 'WHERE' in the where parameter."
        table = cls._get_table()
        sql = 'DELETE FROM %s %s' % (table, where)
        sql, args = simple_sql(sql, *args, **kwargs)
        return do_execute(sql, *args)

    @classmethod
    def delete_by_id(cls, _id: Union[int, str]):
        """
        Physical delete
        rowcount = Person.delete_by_id(id=1)
        return: Effect rowcount
        """
        logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', id: %d" % ('delete_by_id', cls.__name__, _id))
        pk, table = cls._get_pk_and_table()
        sql = 'DELETE FROM %s WHERE %s=?' % (table, pk)
        return do_execute(sql, _id)

    @classmethod
    def delete_by_ids(cls, ids: Union[Sequence[int], Sequence[str]], batch_size=128):
        """
        Batch physical delete, they will be executed in batches if there are too many
        rowcount = Person.delete_by_ids(id=[1,2])
        return: Effect rowcount
        """
        logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', ids: %s, batch_size: %s" % ('delete_by_ids', cls.__name__, ids, batch_size))
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'
        if ids_size == 1:
            return cls.delete_by_id(ids[0])
        elif ids_size <= batch_size:
            return cls.do_delete_by_ids(ids)
        else:
            split_ids = _split_ids(ids, batch_size)
            with transaction():
                results = list(map(cls.do_delete_by_ids, split_ids))
            return sum(results)

    @classmethod
    def do_delete_by_ids(cls, ids: Union[Sequence[int], Sequence[str]]):
        """
        Batch physical delete, please use delete_by_ids if there are too many
        rowcount = Person.do_delete_by_ids(id=[1,2])
        return: Effect rowcount
        """
        ids_size = len(ids)
        pk, table = cls._get_pk_and_table()
        sql = 'DELETE FROM {} WHERE {} in ({})'.format(table, pk, ','.join(['?' for _ in range(ids_size)]))
        return do_execute(sql, *ids)

    @classmethod
    def batch_insert(cls, *args):
        """
        Batch insert
        rowcount = Person.batch_insert([{'name': '张三', 'age': 55},{'name': '李四', 'age': 66}])
        :param args: All number must have same key.
        :return: Effect rowcount
        """
        logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', args: %s" % ('batch_insert', cls.__name__, args))
        assert len(args) > 0, 'args must not be empty.'
        pk, table = cls._get_pk_and_table()
        pk_strategy = cls._get_pk_strategy()
        if pk_strategy == PkStrategy.SNOWFLAKE:
            for arg in args:
                if pk not in arg:
                    arg[pk] = get_id()

        return batch_insert(table, *args)

    # ------------------------------------------------Class query method--------------------------------------------------------
    @classmethod
    def count(cls, **kwargs):
        """
        count = Person.count(name='张三', age=55)
        """
        orm_count_log('count', cls.__name__, **kwargs)
        table = cls._get_table()
        where, args, _ = _get_where_arg_limit(**kwargs)
        fields = 'count(1)'
        sql = _select_sql(table, where, LIMIT_1, fields)
        return do_get_limit(sql, *args, LIMIT_1)

    @classmethod
    def count_by(cls, where: str, *args, **kwargs):
        """
        Automatically add 'limit ?' where if not.
        count = Person.count_by('where name=?', '李四')
        """
        orm_by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args, **kwargs)
        assert where.lower().startswith('where'), "Must start with 'where' in the where parameter."
        table = cls._get_table()
        sql = "SELECT count(1) FROM {} {}".format(table, where)
        sql, args = simple_sql(sql, *args, **kwargs)
        return do_get(sql, *args)

    @classmethod
    def exists(cls, **kwargs):
        orm_count_log('exists', cls.__name__, **kwargs)
        table = cls._get_table()
        where, args, _ = _get_where_arg_limit(**kwargs)
        sql = "SELECT 1 FROM {} {} limit ?".format(table, where)
        return do_get_limit(sql, *args, LIMIT_1) == 1

    @classmethod
    def exists_by(cls, where: str, *args, **kwargs):
        orm_by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args, **kwargs)
        assert where.lower().startswith('where'), "Must start with 'where' in the where parameter."
        table = cls._get_table()
        sql = "SELECT 1 FROM {} {}".format(table, where)
        sql, args = simple_sql(sql, *args, **kwargs)
        return do_get(sql, *args) == 1

    @classmethod
    def find(cls, *fields, **kwargs):
        """
        Return list(object) or empty list if no result.
        persons = Person.find('id', 'name', 'age', name='张三', age=55)
        :param fields: Default select all fields if not set
        """
        orm_find_log('find', cls.__name__, *fields, **kwargs)
        return [cls.to_obj(**d) for d in cls.query(*fields, **kwargs)]

    @classmethod
    def find_one(cls, *fields, **kwargs):
        """
        Return unique result(object) or None if no result.
        person = Person.find_one('id', 'name', 'age', name='张三', age=55)
        :param fields: Default select all fields if not set
        """
        orm_find_log('find_one', cls.__name__, *fields, **kwargs)
        result = cls.query_one(*fields, **kwargs)
        return cls.to_obj(**result) if result else None

    @classmethod
    def find_by(cls, where: str, *args, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.find_by('where name=?', '李四')
        """
        orm_by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args, **kwargs)
        return [cls.to_obj(**d) for d in cls.query_by(where, *args, **kwargs)]

    @classmethod
    def find_page(cls, page_num=1, page_size=10, *fields, **kwargs):
        """
        Return list(object) or empty list if no result.
        persons = Person.find_page(1, 10, 'name', 'age', name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        :param fields: Default select all fields if not set
        """
        orm_page_log('find_page', page_num, page_size, cls.__name__, *fields, **kwargs)
        result = cls.query_page(page_num, page_size, *fields, **kwargs)
        return [cls.to_obj(**d) for d in result]

    @classmethod
    def find_page_by(cls, page_num: int, page_size: int, where: str, *args, **kwargs):
        """
        Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
        rows = Person.find_by_page(1, 10, 'where name=?', '李四')
        """
        orm_page_log(sys._getframe().f_code.co_name, page_num, page_size, cls.__name__, where, *args, **kwargs)
        return [cls.to_obj(**d) for d in cls.query_page_by(page_num, page_size, where, *args, **kwargs)]

    @classmethod
    def find_by_id(cls, _id: Union[int, str], *fields):
        """
        Return one class object or None if no result.
        person = Person.find_by_id(1, 'id', 'name', 'age')
        :param _id: pk
        :param fields: Default select all fields if not set
        """
        orm_find_by_id_log('find_by_id', cls.__name__, _id, *fields)
        result = cls.query_by_id(_id, *fields)
        return cls.to_obj(**result) if result else None

    @classmethod
    def find_by_ids(cls, ids: Union[Sequence[int], Sequence[str]], *fields):
        """
        Return list(class object) or empty list if no result.
        persons = Person.find_by_ids([1,2], 'id', 'name', 'age')
        :param ids: List of pk
        :param fields: Default select all fields if not set
        """
        orm_find_by_ids_log('find_by_ids', cls.__name__, ids, *fields)
        return [cls.to_obj(**d) for d in cls.query_by_ids(ids, *fields)]

    @classmethod
    def query(cls, *fields, **kwargs):
        """
        Return list(dict) or empty list if no result.
        persons = Person.query('id', 'name', 'age', name='张三', age=55)
        :param fields: Default select all fields if not set
        """
        orm_find_log('query', cls.__name__, *fields, **kwargs)
        where, args, limit = _get_where_arg_limit(**kwargs)
        table = cls._get_table()
        sql = _select_sql(table, where, limit, *fields)
        if limit:
            if isinstance(limit, int):
                args = [*args, limit]
            else:
                args = [*args, *limit]
        return do_query(sql, *args)

    @classmethod
    def query_one(cls, *fields, **kwargs):
        """
        Return unique result(dict) or None if no result.
        persons = Person.query_one('id', 'name', 'age', name='张三', age=55)
        :param fields: Default select all fields if not set
        """
        orm_find_log('query_one', cls.__name__, *fields, **kwargs)
        where, args, _ = _get_where_arg_limit(**kwargs)
        table = cls._get_table()
        sql = _select_sql(table, where, LIMIT_1, *fields)
        return do_query_one_limit(sql, *args, LIMIT_1)

    @classmethod
    def query_by(cls, where: str, *args, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.query_by('where name=?', '李四')
        """
        orm_by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args, **kwargs)
        sql = cls._where_sql(where)
        sql, args = simple_sql(sql, *args, **kwargs)
        return do_query(sql, *args)

    @classmethod
    def query_page(cls, page_num=1, page_size=10, *fields, **kwargs):
        """
        Return list(dict) or empty list if no result.
        persons = Person.query_page(1, 10, 'id', 'name', 'age', name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        :param fields: Default select all fields if not set
        """
        orm_page_log('query_page', page_num, page_size, cls.__name__, *fields, **kwargs)
        table = cls._get_table()
        where, args, _ = _get_where_arg_limit(**kwargs)
        sql = _select_sql(table, where, NO_LIMIT, *fields)
        return do_query_page(sql, page_num, page_size, *args)

    @classmethod
    def query_page_by(cls, page_num: int, page_size: int, where: str, *args, **kwargs):
        """
        Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
        rows = Person.query_by_page(1, 10, 'where name=?', '李四')
        """
        orm_by_page_log(sys._getframe().f_code.co_name, page_num, page_size, cls.__name__, where, *args, **kwargs)
        sql = cls._where_sql(where)
        sql, args = simple_sql(sql, *args, **kwargs)
        return do_query_page(sql, page_num, page_size, *args)

    @classmethod
    def query_by_id(cls, _id: Union[int, str], *fields):
        """
        Return one row(dict) or None if no result.
        person = Person.query_by_id(1, 'id', 'name', 'age')
        :param _id: pk
        :param fields: Default select all fields if not set
        """
        orm_find_by_id_log('query_by_id', cls.__name__, _id, *fields)
        pk, table = cls._get_pk_and_table()
        where = 'WHERE {}=?'.format(pk)
        sql = _select_sql(table, where, LIMIT_1, *fields)
        return do_query_one_limit(sql, _id, LIMIT_1)

    @classmethod
    def query_by_ids(cls, ids: Union[Sequence[int], Sequence[str]], *fields):
        """
        Return list(dict) or empty list if no result.
        persons = Person.query_by_ids([1,2], 'id', 'name', 'age')
        :param ids: List of pk
        :param fields: Default select all fields if not set
        """
        orm_find_by_ids_log('query_by_ids', cls.__name__, ids, *fields)
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        pk, table = cls._get_pk_and_table()
        where = 'WHERE {} in ({})'.format(pk, ','.join(['?' for _ in range(ids_size)]))
        sql = _select_sql(table, where, ids_size, *fields)
        return do_query(sql, *ids, ids_size)

    @classmethod
    def select(cls, *fields, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.select('id', 'name', 'age', name='张三', age=55)
        :param fields: Default select all fields if not set
        """
        orm_find_log('select', cls.__name__, *fields, **kwargs)
        where, args, limit = _get_where_arg_limit(**kwargs)
        table = cls._get_table()
        sql = _select_sql(table, where, limit, *fields)
        if limit:
            if isinstance(limit, int):
                args = [*args, limit]
            else:
                args = [*args, *limit]
        return do_select(sql, *args)

    @classmethod
    def select_one(cls, *fields, **kwargs):
        """
        Return unique result(tuple) or None if no result.
        row = Person.select_one('id', 'name', 'age', name='张三', age=55)
        :param fields: Default select all fields if not set
        """
        orm_find_log('select_one', cls.__name__, *fields, **kwargs)
        where, args, _ = _get_where_arg_limit(**kwargs)
        table = cls._get_table()
        sql = _select_sql(table, where, LIMIT_1, *fields)
        return do_select_one_limit(sql, *args, LIMIT_1)

    @classmethod
    def select_by(cls, where: str, *args, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.select_by('where name=?', '李四')
        """
        orm_by_log(sys._getframe().f_code.co_name, cls.__name__, where, *args, **kwargs)
        sql = cls._where_sql(where)
        sql, args = simple_sql(sql, *args, **kwargs)
        return do_select(sql, *args)

    @classmethod
    def select_page(cls, page_num=1, page_size=10, *fields, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.select_page('id', 'name', 'age', name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        :param fields: Default select all fields if not set
        """
        orm_page_log('select_page', page_num, page_size, cls.__name__, *fields, **kwargs)
        table = cls._get_table()
        where, args, _ = _get_where_arg_limit(**kwargs)
        sql = _select_sql(table, where, NO_LIMIT, *fields)
        return do_select_page(sql, page_num, page_size, *args)

    @classmethod
    def select_page_by(cls, page_num: int, page_size: int, where: str, *args, **kwargs):
        """
        Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
        rows = Person.select_by_page(1, 10, 'where name=?', '李四')
        """
        orm_by_page_log(sys._getframe().f_code.co_name, page_num, page_size, cls.__name__, where, *args, **kwargs)
        sql = cls._where_sql(where)
        sql, args = simple_sql(sql, *args, **kwargs)
        return do_select_page(sql, page_num, page_size, *args)

    @classmethod
    def select_by_id(cls, _id: Union[int, str], *fields):
        """
        Return one row(dict) or None if no result.
        row = Person.select_by_id(1, 'id', 'name', 'age')
        :param _id: pk
        :param fields: Default select all fields if not set
        """
        orm_find_by_id_log('select_by_id', cls.__name__, _id, *fields)
        pk, table = cls._get_pk_and_table()
        where = 'WHERE {}=?'.format(pk)
        sql = _select_sql(table, where, LIMIT_1, *fields)
        return do_select_one_limit(sql, _id, LIMIT_1)

    @classmethod
    def select_by_ids(cls, ids: Union[Sequence[int], Sequence[str]], *fields):
        """
        Return list(dict) or empty list if no result.
        rows = Person.select_by_ids([1,2], 'id', 'name', 'age')
        :param ids: List of pk
        :param fields: Default select all fields if not set
        """
        orm_find_by_ids_log('select_by_ids', cls.__name__, ids, *fields)
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        pk, table = cls._get_pk_and_table()
        where = 'WHERE {} in ({})'.format(pk, ','.join(['?' for _ in range(ids_size)]))
        sql = _select_sql(table, where, ids_size, *fields)
        return do_select(sql, *ids, ids_size)

    @classmethod
    def to_obj(cls, **kwargs):
        model = cls.__new__(cls)
        model.__dict__.update(**kwargs)
        return model

    # ------------------------------------------------Private class method------------------------------------------------------------------
    @classmethod
    def _logical_delete_by_id_op(cls, _id: Union[int, str], update_by: Union[int, str] = None, del_status=DelFlag.DELETED):
        pk, table = cls._get_pk_and_table()
        del_flag_field = cls._get_del_flag_field()
        update_by_field = cls._get_update_by_field()

        where = '%s=?' % pk
        if update_by is not None and update_by_field is not None:
            sql, update_time_arg = cls._update_sql(where, del_flag_field, update_by_field)
            if update_time_arg:
                return do_execute(sql, del_status.value, update_by, update_time_arg, _id, LIMIT_1)
            return do_execute(sql, del_status.value, update_by, _id, LIMIT_1)
        else:
            sql, update_time_arg = cls._update_sql(where, del_flag_field)
            if update_time_arg:
                return do_execute(sql, del_status.value, update_time_arg, _id)
            return do_execute(sql, del_status.value, _id)

    @classmethod
    def _logical_delete_by_ids_op(cls, ids: Union[Sequence[int], Sequence[str]], update_by: Union[int, str] = None, batch_size=128,
            del_status=DelFlag.DELETED):
        ids_size = len(ids)
        assert ids_size > 0, 'ids must not be empty.'

        if ids_size == 1:
            return cls._logical_delete_by_id_op(ids[0], update_by, del_status)
        elif ids_size <= batch_size:
            return cls._do_logical_delete_by_ids(ids, update_by, del_status)
        else:
            split_ids = _split_ids(ids, batch_size)
            with transaction():
                results = [cls._do_logical_delete_by_ids(ids, update_by, del_status) for ids in split_ids]
            return sum(results)

    @classmethod
    def _do_logical_delete_by_ids(cls, ids: Union[Sequence[int], Sequence[str]], update_by: Union[int, str] = None, del_status=DelFlag.DELETED):
        pk = cls._get_pk()
        del_flag_field = cls._get_del_flag_field()
        update_by_field = cls._get_update_by_field()

        where = '%s in (%s)' % (pk, ','.join(['?' for _ in range(len(ids))]))
        if update_by is not None and update_by_field is not None:
            sql, update_time_arg = cls._update_sql(where, del_flag_field, update_by_field)
            if update_time_arg:
                return do_execute(sql, del_status.value, update_by, update_time_arg, *ids)
            return do_execute(sql, del_status.value, update_by, *ids)
        else:
            sql, update_time_arg = cls._update_sql(where, del_flag_field)
            if update_time_arg:
                return do_execute(sql, del_status.value, update_time_arg, *ids)
            return do_execute(sql, del_status.value, *ids)

    @classmethod
    def _get_pk(cls):
        if hasattr(cls, PK):
            return cls.__pk__
        logger.warning("%s not set attribute '%s'" % (cls.__name__, PK))
        return DEFAULT_PK_FIELD

    @classmethod
    def _get_pk_seq(cls):
        if hasattr(cls, PK_SEQ):
            return cls.__pk_seq__
        logger.warning("%s not set attribute '%s'" % (cls.__name__, PK_SEQ))
        pk, table = cls._get_pk_and_table()
        return "{}_{}_seq".format(table, pk)

    @classmethod
    def _get_table(cls):
        if hasattr(cls, TABLE):
            return cls.__table__
        logger.warning("%s not set attribute '%s'" % (cls.__name__, TABLE))
        return _get_table_name(cls.__name__)

    @classmethod
    def _get_pk_and_table(cls):
        return cls._get_pk(), cls._get_table()

    @classmethod
    def _get_pk_strategy(cls):
        if hasattr(cls, PK_STRATEGY):
            return cls.__pk_strategy__
        return None

    @classmethod
    def _get_update_by_field(cls):
        if hasattr(cls, UPDATE_BY):
            return cls.__update_by__
        return None

    @classmethod
    def _get_update_time_field(cls):
        if hasattr(cls, UPDATE_TIME):
            return cls.__update_time__
        return None

    @classmethod
    def _get_del_flag_field(cls):
        assert hasattr(cls, DEL_FLAG), "%s not set attribute '%s'" % (cls.__name__, DEL_FLAG)
        return cls.__del_flag__

    @classmethod
    def _update_sql(cls, where, *update_fields):
        update_time_arg = None
        table = cls._get_table()
        update_time_field = cls._get_update_time_field()
        if update_time_field is not None and update_time_field not in update_fields:
            update_fields = [*update_fields, update_time_field]
            update_time_arg = datetime.now()

        update_fields = ','.join(['{}=?'.format(col) for col in update_fields])
        return 'UPDATE {} SET {} WHERE {}'.format(table, update_fields, where), update_time_arg

    @classmethod
    def _where_sql(cls, where: str):
        low_where = where.lower()
        if low_where.startswith('where'):
            table = cls._get_table()
            return _select_sql(table, where, NO_LIMIT)
        elif low_where.startswith('select'):
            return where
        raise DBError("The where parameter must be a complete SQL statement or conditions start with 'where'")


# ----------------------------------------------------------Private function------------------------------------------------------------------
def _select_sql(table: str, where: str, limit: Union[int, Tuple[int], List[int]], *fields):
    if fields:
        fields = ','.join([col if '(' in col else '{}'.format(col) for col in fields])
    else:
        fields = _get_table_columns(table)

    if limit:
        if isinstance(limit, int):
            return 'SELECT {} FROM {} {} LIMIT ?'.format(fields, table, where)
        elif (isinstance(limit, Tuple) or isinstance(limit, List)) and len(limit) == 2:
            return 'SELECT {} FROM {} {} LIMIT ? OFFSET ?'.format(fields, table, where)
        else:
            raise ValueError("The type of the parameter 'limit' must be 'int' or tuple, list, and it length is 2.")
    else:
        return 'SELECT {} FROM {} {}'.format(fields, table, where)


@lru_cache(maxsize=CONFIG_DICT[CACHE_SIZE])
def _get_table_columns(table: str):
    return do_get_limit(COLUMN_SQL, table, LIMIT_1)


def _get_condition_arg(k: str, v: object):
    if k.endswith("__eq"):
        return "{}=?".format(k[:-4]), v
    if k.endswith("__gt"):
        return "{}>?".format(k[:-4]), v
    if k.endswith("__lt"):
        return "{}<?".format(k[:-4]), v
    if k.endswith("__ge"):
        return "{}>=?".format(k[:-4]), v
    if k.endswith("__gte"):
        return "{}>=?".format(k[:-5]), v
    if k.endswith("__le"):
        return "{}<=?".format(k[:-4]), v
    if k.endswith("__lte"):
        return "{}<=?".format(k[:-5]), v
    if k.endswith("__in") and isinstance(v, Sequence) and not isinstance(v, str):
        return "{} in ({})".format(k[:-4], ','.join(['?' for _ in v])), v
    if k.endswith("__in"):
        return "{} in ({})".format(k[:-4], '?'), v
    if k.endswith("__startswith"):
        return "{} like ?".format(k[:-12]), '{}%'.format(v)
    if k.endswith("__endswith"):
        return "{} like ?".format(k[:-10]), '%{}'.format(v)
    if k.endswith("__contains"):
        return "{} like ?".format(k[:-10]), '%{}%'.format(v)
    if k.endswith("__between") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
        return "{} between ? and ?".format(k[:-9]), v
    if k.endswith("__between"):
        return ValueError("Must is instance of Sequence with length 2 when use between statement")

    if not isinstance(v, str):
        return "{}=?".format(k), v
    lower_v = v.lower()
    if any([symbol in SYMBOLS for symbol in lower_v]):
        return "{}{}".format(k, v), None
    elif BETWEEN in lower_v or LIKE in lower_v or IN in lower_v:
        return "{} {}".format(k, v), None
    else:
        return "{}=?".format(k), v


def _get_where_arg_limit(**kwargs):
    where, args, limit = '', [], 0
    if 'limit' in kwargs:
        limit = kwargs.pop('limit')

    if kwargs:
        conditions, tmp_args = zip(*[_get_condition_arg(k, v) for k, v in kwargs.items()])
        tmp_args = [arg for arg in tmp_args if arg is not None]

        for arg in tmp_args:
            if arg:
                if isinstance(arg, Sequence) and not isinstance(arg, str):
                    args.extend(arg)
                else:
                    args.append(arg)
        where = 'WHERE {}'.format(' and '.join(conditions))

    return where, args, limit


def _split_ids(ids: Sequence[int], batch_size):
    ids_size = len(ids)
    n = ids_size // batch_size
    n += 0 if ids_size % batch_size == 0 else 1
    return [ids[i:i + batch_size] for i in range(0, ids_size, batch_size)]


def _get_table_name(class_name):
    for i in range(1, len(class_name) - 1)[::-1]:
        if class_name[i].isupper():
            class_name = class_name[:i] + '_' + class_name[i:]
    return class_name.lower()
