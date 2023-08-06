import re
import threading
from enum import Enum
from jinja2 import Template
from functools import lru_cache
from .log_support import logger
from typing import Sequence, List
from .constant import NAMED_REGEX, DYNAMIC_REGEX, CONFIG_DICT, CACHE_SIZE

DB_LOCK = threading.RLock()


def get_batch_args(*args):
    return args[0] if isinstance(args, tuple) and len(args) == 1 and isinstance(args[0], Sequence) else args


def try_commit(db_ctx):
    if db_ctx.transactions == 0:
        logger.debug('Commit transaction...')
        try:
            db_ctx.connection.commit()
            logger.debug('Commit ok.')
        except Exception:
            logger.warning('Commit failed, try rollback...')
            db_ctx.connection.rollback()
            logger.warning('Rollback ok.')
            raise


def simple_sql(sql: str, *args, **kwargs):
    return get_named_sql_args(sql, **kwargs) if kwargs else (sql, args)


def dynamic_sql(sql: str, *args, **kwargs):
    sql_type = _get_sql_type(sql)
    if sql_type >= 1 and not kwargs:
        raise MapperError("Parameter 'kwargs' must not be empty when named mapping sql.")
    if sql_type == 0:
        return sql, args
    if sql_type == 1:
        sql = Template(sql).render(**kwargs)
    return get_named_sql_args(sql, **kwargs)


def is_dynamic_sql(sql: str):
    return re.search(DYNAMIC_REGEX, sql)


@lru_cache(maxsize=2*CONFIG_DICT[CACHE_SIZE])
def _get_sql_type(sql: str):
    """
    :return: 0: placeholder, 1: dynamic, 2: named mapping
    """
    if is_dynamic_sql(sql):
        return 1
    if ':' in sql:
        return 2
    return 0


def get_named_sql_args(sql: str, **kwargs):
    args = get_named_args(sql, **kwargs)
    return get_named_sql(sql), args


@lru_cache(maxsize=CONFIG_DICT[CACHE_SIZE])
def get_named_sql(sql: str):
    return re.sub(NAMED_REGEX, '?', sql)


def get_named_args(sql: str, **kwargs):
    return [kwargs[r[1:]] for r in re.findall(NAMED_REGEX, sql)]


class DBCtx(threading.local):
    """
    Thread local object that holds connection info.
    """

    def __init__(self, connect, is_pool):
        self.connect = connect
        self.connection = None
        self.transactions = 0
        self.prepared = True
        if is_pool:
            self.get_cursor = lambda: self.connection.cursor(prepared=self.prepared)
            self.log = lambda action: logger.debug('%s connection <%s>...' % (action, hex(id(self.connection._cnx))))
        else:
            self.get_cursor = lambda: self.connection.cursor()
            self.log = lambda action: logger.debug('%s connection <%s>...' % (action, hex(id(self.connection))))

    def is_not_init(self):
        return self.connection is None

    def init(self):
        self.transactions = 0
        self.connection = self.connect()
        self.log('Use')

    def release(self):
        if self.connection:
            self.log('Release')
            self.connection.close()
            self.connection = None

    def cursor(self):
        """
        Return cursor
        """
        # logger.debug('Cursor prepared: %s' % self.prepared)
        return self.get_cursor()

    def statement(self, sql: str):
        """
        Return statement
        """
        return self.connection.statement(sql)


class ConnectionCtx(object):
    """
    ConnectionCtx object that can open and close connection context. ConnectionCtx object can be nested and only the most
    outer connection has effect.
    with connection():
        pass
        with connection():
            pass
    """

    def __init__(self, db_ctx):
        self.db_ctx = db_ctx

    def __enter__(self):
        self.should_cleanup = False
        if self.db_ctx.is_not_init():
            self.db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        if self.should_cleanup:
            self.db_ctx.release()


class TransactionCtx(object):
    """
    TransactionCtx object that can handle transactions.
    with TransactionCtx():
        pass
    """

    def __init__(self, db_ctx):
        self.db_ctx = db_ctx

    def __enter__(self):
        self.should_close_conn = False
        if self.db_ctx.is_not_init():
            # needs open a connection first:
            self.db_ctx.init()
            self.should_close_conn = True
        self.db_ctx.transactions += 1
        logger.debug('Begin transaction...' if self.db_ctx.transactions == 1 else 'Join current transaction...')
        return self

    def __exit__(self, exctype, excvalue, traceback):
        self.db_ctx.transactions -= 1
        try:
            if self.db_ctx.transactions == 0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                self.db_ctx.release()

    def commit(self):
        try_commit(self.db_ctx)

    def rollback(self):
        logger.warning('Rollback transaction...')
        self.db_ctx.connection.rollback()
        logger.debug('Rollback ok.')


class DBError(Exception):
    pass


class MapperError(DBError):
    pass


class NotFoundError(DBError):
    pass


class MultiColumnsError(DBError):
    pass


class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class SqlModel:
    def __init__(self, sql: str, action: str, namespace: str, dynamic=False, includes: List[str] = None, pk_seq: str = None):
        self.sql = sql
        self.action = action
        self.namespace = namespace
        self.dynamic = dynamic
        self.includes = includes
        self.pk_seq = pk_seq
        self.mapping = True if dynamic else ':' in sql
        self.placeholder = False if self.mapping else '?' in sql


class SqlAction(Enum):
    CALL = 'call'
    INSERT = 'insert'
    UPDATE = 'update'
    DELETE = 'delete'
    SELECT = 'select'
