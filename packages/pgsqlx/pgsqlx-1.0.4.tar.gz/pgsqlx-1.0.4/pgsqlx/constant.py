CACHE_SIZE = 'cache_size'

CONFIG_DICT = dict({CACHE_SIZE: 128})

LIMIT_1 = 1

NO_LIMIT = 0

NAMED_REGEX = r':[\w|\d]*'

DYNAMIC_REGEX = '{%|{{|}}|%}'

MAPPER_PATH = "mapper_path"

DEFAULT_PK_FIELD = 'id'

SYMBOLS = ['=', '>', '<']

BETWEEN, LIKE, IN = 'between', 'like', 'in'

PK, PK_SEQ, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG, PK_STRATEGY = '__pk__', '__pk_seq__', '__table__', '__update_by__', '__update_time__', \
    '__del_flag__', '__pk_strategy__'

COLUMN_SQL = '''SELECT array_to_string(array_agg(column_name),',') as column_name FROM information_schema.columns 
                 WHERE table_schema='public' and table_name = ? LIMIT ?'''


