LIMIT_1 = 1

NO_LIMIT = 0

NAMED_REGEX = r':[\w|\d]*'

DYNAMIC_REGEX = '{%|{{|}}|%}'

MAPPER_PATH = "mapper_path"

PK_SQL = 'SELECT LAST_INSERT_ID()'

DEFAULT_PK_FIELD = 'id'

SYMBOLS = ['=', '>', '<']

BETWEEN, LIKE, IN = 'between', 'like', 'in'

PK, TABLE, UPDATE_BY, UPDATE_TIME, DEL_FLAG, PK_STRATEGY = '__pk__', '__table__', '__update_by__', '__update_time__', '__del_flag__', '__pk_strategy__'

COLUMN_SQL = '''SELECT GROUP_CONCAT(CONCAT("`",column_name,"`") SEPARATOR ",") 
                 FROM information_schema.columns WHERE table_schema = (SELECT DATABASE()) AND table_name = ? limit ?'''
