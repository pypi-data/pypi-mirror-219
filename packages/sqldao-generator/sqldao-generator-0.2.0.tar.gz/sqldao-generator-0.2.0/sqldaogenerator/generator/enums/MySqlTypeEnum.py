from enum import Enum


# from sqlalchemy import BigInteger, VARCHAR, Text, SmallInteger, Integer, Double, DateTime


class MySqlTypeEnum(Enum):
    bigint = 'BigInteger'
    varchar = 'VARCHAR'
    text = 'Text'
    tinyint = 'SmallInteger'
    int = 'Integer'
    double = 'Double'
    datetime = 'DateTime'
