from logging import basicConfig, INFO, getLogger

logger = getLogger(__name__)
basicConfig(level=INFO, format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def sql_log(function: str, sql: str, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.db.%s' \n\tsql: %s \n\targs: %s \n\tkwargs: %s" % (function, sql.strip(), args, kwargs))


def page_log(function: str, sql: str, page_num, page_size, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.db.%s', page_num: %d, page_size: %d \n\tsql: %s \n\targs: %s \n\tkwargs: %s" % (
        function, page_num, page_size, sql.strip(), args, kwargs))


def insert_log(function: str, table: str, **kwargs):
    logger.debug("Exec func 'mysqlx.db.%s' \n\t Table: '%s', kwargs: %s" % (function, table, kwargs))


def do_sql_log(function: str, sql: str, *args):
    logger.debug("Exec func 'mysqlx.db.%s' \n\t sql: %s \n\t args: %s" % (function, sql, args))


def do_page_log(function: str, sql: str, page_num, page_size, *args):
    logger.debug(
        "Exec func 'mysqlx.db.%s', page_num: %d, page_size: %d \n\t sql: %s \n\t args: %s" % (function, page_num, page_size, sql.strip(), args))


def sql_id_log(function: str, sql_id: str, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.dbx.%s', sql_id: %s, args: %s, kwargs: %s" % (function, sql_id.strip(), args, kwargs))


def page_sql_id_log(function: str, sql_id: str, page_num, page_size, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.dbx.%s', page_num: %d, page_size: %d, sql_id: %s, args: %s, kwargs: %s" % (
        function, page_num, page_size, sql_id.strip(), args, kwargs))


def orm_by_page_log(function, page_num, page_size, class_name, where, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s', page_num: %d, page_size: %d \n\t Class: '%s', where: %s, args: %s, kwargs: %s" % (
        function, page_num, page_size, class_name, where, args, kwargs))


def orm_page_log(function, page_num, page_size, class_name, *fields, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s', page_num: %d, page_size: %d \n\t Class: '%s', fields: %s, kwargs: %s" % (
        function, page_num, page_size, class_name, fields, kwargs))


def orm_insert_log(function, class_name, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', kwargs: %s" % (function, class_name, kwargs))


def orm_delete_by_id_log(function, class_name, _id, update_by):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', id: %d, update_by: %s" % (function, class_name, _id, update_by))


def orm_by_log(function, class_name, where, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', where: %s, args: %s, kwargs: %s" % (function, class_name, where, args, kwargs))


def orm_inst_log(function, class_name):
    logger.debug("Exec func 'mysqlx.orm.Model.%s', Class: '%s'" % (function, class_name))


def orm_logical_delete_by_ids_log(function, class_name, ids, update_by, batch_size):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', ids: %s, update_by: %s, batch_size: %s" % (
    function, class_name, ids, update_by, batch_size))


def orm_count_log(function, class_name, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', kwargs: %s" % (function, class_name, kwargs))


def orm_find_log(function, class_name, *fields, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', fields: %s, kwargs: %s" % (function, class_name, fields, kwargs))


def orm_find_by_id_log(function, class_name, _id, *fields):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', id: %d, fields: %s" % (function, class_name, _id, fields))


def orm_find_by_ids_log(function, class_name, ids, *fields):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t Class: '%s', ids: %s, fields: %s" % (function, class_name, ids, fields))
