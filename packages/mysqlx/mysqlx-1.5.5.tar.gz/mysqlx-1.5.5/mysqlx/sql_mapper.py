import os
import functools
from .log_support import logger
from .dbx import get_sql_model, do_get_sql, build_sql_id
from .support import SqlAction, get_named_sql_args, simple_sql, MapperError
from .db import do_get, do_query, do_query_one, do_execute, do_batch_execute, do_select, do_select_one, batch_execute, do_save

_UPDATE_ACTIONS = (SqlAction.INSERT.value, SqlAction.UPDATE.value, SqlAction.DELETE.value, SqlAction.CALL.value)


def mapper(namespace: str = None, sql_id: str = None, batch=False, return_pk=False):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            param_names = func.__code__.co_varnames
            full_sql_id, func_name = _before(func, namespace, sql_id, *args, **kwargs)
            sql_model = get_sql_model(full_sql_id)
            exec_func = _get_exec_func(func, sql_model.action, batch, return_pk)
            if not batch:
                use_sql, args = do_get_sql(sql_model, batch, param_names, *args, **kwargs)
                if return_pk and SqlAction.INSERT.value not in use_sql.lower():
                    raise MapperError("Only insert sql can return primary key.")
            else:
                if kwargs:
                    logger.warning("Batch exec sql better use like '{}(args)' or '{}(*args)' then '{}(args=args)'".format(func_name, func_name, func_name))
                    args = list(kwargs.values())[0]
                use_sql, _ = do_get_sql(sql_model, batch, param_names, *args)
            return exec_func(use_sql, *args)

        return _wrapper
    return _decorator


def sql(value: str, batch=False, return_pk=False):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            use_sql = value
            low_sql = value.lower()
            if any([action in low_sql for action in _UPDATE_ACTIONS]):
                if batch:
                    if kwargs:
                        args = list(kwargs.values())[0]
                    return batch_execute(use_sql, *args)
                if kwargs:
                    use_sql, args = get_named_sql_args(**kwargs)
                if return_pk:
                    assert SqlAction.INSERT.value in use_sql.lower(), 'Only insert sql can return primary key.'
                    return do_save(use_sql, *args)
                return do_execute(use_sql, *args)
            elif SqlAction.SELECT.value in low_sql:
                select_func = _get_select_func(func)
                use_sql, args = simple_sql(use_sql, *args, **kwargs)
                return select_func(use_sql, *args)
            else:
                return ValueError("Invalid sql: {}.".format(sql))

        return _wrapper
    return _decorator


def _get_exec_func(func, action, batch, return_pk):
    if action == SqlAction.SELECT.value:
        return _get_select_func(func)
    elif batch:
        return do_batch_execute
    elif return_pk:
        return do_save
    else:
        return do_execute


def _get_select_func(func):
    names = func.__code__.co_names
    is_list = 'list' in names or 'List' in names
    if 'Mapping' in names and is_list:
        return do_query
    elif 'Mapping' in names:
        return do_query_one
    elif len(names) == 1 and names[0] in ('int', 'float', 'Decimal', 'str', 'AnyStr', 'date', 'time', 'datetime'):
        return do_get
    elif len(names) == 1 and names[0] in ('tuple', 'Tuple'):
        return do_select_one
    elif is_list:
        return do_select
    else:
        return do_query


def _before(func, namespace, _id, *args, **kwargs):
    file_name = os.path.basename(func.__code__.co_filename)[:-3]
    _namespace = namespace if namespace else file_name
    _id = _id if _id else func.__name__
    sql_id = build_sql_id(_namespace, _id)
    func_name = file_name + '.' + func.__name__
    logger.debug("Exec mapper func: '%s', sql_id: '%s', args: %s, kwargs: %s" % (func_name, sql_id, args, kwargs))
    return sql_id, func_name
