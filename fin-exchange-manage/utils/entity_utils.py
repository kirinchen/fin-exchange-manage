from enum import Enum
from typing import Any

from sqlalchemy.orm import DeclarativeMeta, Query


def gen_entity_from_dict(payload: dict, matched_schema: DeclarativeMeta, validate=True) -> object:
    object_dict = dict()
    column_names = matched_schema.__table__.columns.keys()
    invalid_columns = []
    for key, value in payload.items():
        if key not in column_names:
            invalid_columns.append(key)
        else:
            object_dict[key] = value
    if invalid_columns:
        if validate:
            raise KeyError(
                f"Some of the {matched_schema.__tablename__}'s keys are not allowed!! {invalid_columns}")
    orm_object = matched_schema(**object_dict)

    return orm_object


def gen_entity_from_obj(body: object, matched_schema: DeclarativeMeta) -> object:
    if type(body) is not dict:
        body: object = body
        body = body.__dict__
    return gen_entity_from_dict(body, matched_schema, validate=False)


class Operand(Enum):
    DEFAULT_EQ = ''
    EQ = 'eq_'


class ColumnCondition:

    def __init__(self, column: str, operand: Operand, value: Any):
        self.column: str = column
        self.operand: Operand = operand
        self.value: Any = value


class DictFilter:
    """
        startswith
            Operand
                eq_ : equals
    """

    def __init__(self, **kwargs):
        self.column_map: dict = kwargs

    def gen_query(self, q: Query) -> Query:
        for k, v in self.column_map.items():
            column_condition = get_column_condition(k, v)
            print(column_condition)


def get_column_condition(key: str, val: Any) -> ColumnCondition:
    operand = get_operand_by_key(key)
    column = key[len(operand.value)::]
    return ColumnCondition(column, operand, val)


def get_operand_by_key(key: str) -> Operand:
    for o in Operand:
        if key.startswith(o.value):
            return o
    raise NotImplementedError('get_operand_by_key=' + key)
