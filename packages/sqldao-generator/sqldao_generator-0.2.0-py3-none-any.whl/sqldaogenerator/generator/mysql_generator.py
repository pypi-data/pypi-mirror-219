import importlib.resources as pkg_resources
import re
from types import ModuleType

from sqlalchemy import create_engine, text

from sqldaogenerator import resources
from sqldaogenerator.generator.enums.MySqlTypeEnum import MySqlTypeEnum

primary_key_template = "{column} = Column({type}, autoincrement=True, primary_key=True, comment='{comment}')"
column_template = "{column} = Column({type}, comment='{comment}')"
set_template = """def set_{column}(self, value: {type}):
        self.values['{column}'] = value
        return self"""
ifelse_filter_template = """def {column}{suffix}(self, value: {type} = None, reverse=False{other}):
        if value is not None{condition}:
            if not reverse:
                self.filters.append({entity_name}.{column}{if_expression})
            else:
                self.filters.append({entity_name}.{column}{else_expression})
        return self"""
null_filter_template = """def {column}{suffix}(self, reverse=False):
        if not reverse:
            self.filters.append({entity_name}.{column}{if_expression})
        else:
            self.filters.append({entity_name}.{column}{else_expression})
        return self"""
filter_template = """def {column}{suffix}(self, value: {type} = None):
        if value is not None{condition}:
            self.filters.append({entity_name}.{column}{expression})
        return self"""


def add_set(sets: list[str], column: str, type: str):
    sets.append(set_template.format(column=column, type=type))


def add_equal(filters: list[str], column: str, type: str, entity_name: str):
    filters.append(ifelse_filter_template.format(column=column, suffix='', type=type, entity_name=entity_name,
                                                 condition='', if_expression=' == value', else_expression=' != value', other=''))
    filters.append(null_filter_template.format(column=column, suffix='_null', entity_name=entity_name,
                                               if_expression='.is_(None)', else_expression='.isnot(None)'))
    filters.append(ifelse_filter_template.format(column=column, suffix='_in', type=f"list[{type}]", entity_name=entity_name,
                                                 condition=" and len(value) > 0", if_expression='.in_(value)',
                                                 else_expression='.notin_(value)', other=''))


def add_num(filters: list[str], column: str, type: str, entity_name: str):
    filters.append(filter_template.format(column=column, suffix='_gte', type=type, entity_name=entity_name,
                                          condition="", expression=' >= value'))
    filters.append(filter_template.format(column=column, suffix='_lte', type=type, entity_name=entity_name,
                                          condition="", expression=' <= value'))


def add_datetime(filters: list[str], column: str, type: str, entity_name: str):
    filters.append(filter_template.format(column=column, suffix='_start', type=type, entity_name=entity_name,
                                          condition='', expression=' >= value'))
    filters.append(filter_template.format(column=column, suffix='_end', type=type, entity_name=entity_name,
                                          condition='', expression=' <= value'))


def add_like(filters: list[str], column: str, type: str, entity_name: str):
    filters.append(ifelse_filter_template.format(column=column, suffix='_like', type=type, entity_name=entity_name,
                                                 condition=" and value != ''", if_expression='.like(f"{left}{value}{right}")',
                                                 else_expression='.not_like(f"{left}{value}{right}")', other=", left='%', right='%'"))


def generate(user: str, password: str, host: str, port: int, database: str,
             datasource_package: ModuleType, datasource_name: str, base_dao_package: ModuleType, base_dao_name: str,
             dao_package: ModuleType, entity_package: ModuleType, entity_name: str, table: str, override_datasource=False):
    # create a Datasource
    datasource_file = pkg_resources.files(datasource_package).joinpath(f"{datasource_name}.py")
    if override_datasource or not datasource_file.is_file():
        template = pkg_resources.files(resources).joinpath('datasource_template.txt').read_text()
        template = template.format(datasource_name=datasource_name, user=user, password=password, host=host, port=port, dbname=database)
        with datasource_file.open('w', encoding='utf-8') as file:
            file.write(template)

    # create a BaseDao
    base_dao_file = pkg_resources.files(base_dao_package).joinpath(f"{base_dao_name}.py")
    template = pkg_resources.files(resources).joinpath('base_dao_template.txt').read_text()
    template = template.format(base_dao_name=base_dao_name,
                               datasource_package=datasource_package.__package__, datasource_name=datasource_name)
    with base_dao_file.open('w', encoding='utf-8') as file:
        file.write(template)

    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string, echo=True, pool_recycle=270)
    with engine.connect() as connection:
        results = connection.execute(text(f"""
            select COLUMN_NAME, DATA_TYPE, COLUMN_KEY, COLUMN_COMMENT
            from information_schema.columns
            where table_name = '{table}'
            order by ORDINAL_POSITION
            """)).all()

    # create entity, dao
    camelcased_word = re.findall('[A-Z][a-z0-9]*', entity_name)
    underlined_word = '_'.join(camelcased_word).lower()
    columns = []
    sets = []
    filters = []
    for result in results:
        column_name = result.COLUMN_NAME.lower()
        data_type = result.DATA_TYPE.decode() if isinstance(result.DATA_TYPE, bytes) else result.DATA_TYPE
        comment = result.COLUMN_COMMENT.decode() if isinstance(result.COLUMN_COMMENT, bytes) else result.COLUMN_COMMENT

        # column
        if result.COLUMN_KEY == 'PRI':
            template = primary_key_template
        else:
            template = column_template
        columns.append(template.format(
            column=column_name, comment=comment, type=MySqlTypeEnum[data_type].value))

        # fields, filters
        match [column_name, data_type]:
            case [_, ('varchar' | 'text')]:
                py_type = 'str'
                add_set(sets, column_name, py_type)
                add_equal(filters, column_name, py_type, entity_name)
                add_like(filters, column_name, py_type, entity_name)
            case [_, ('tinyint' | 'int' | 'double' | 'bigint') as db_type]:
                py_type = 'float' if db_type == 'double' else 'int'
                add_set(sets, column_name, py_type)
                add_equal(filters, column_name, py_type, entity_name)
                add_num(filters, column_name, py_type, entity_name)
            case [_, ('datetime')]:
                py_type = 'datetime | str'
                add_set(sets, column_name, py_type)
                add_equal(filters, column_name, py_type, entity_name)
                add_datetime(filters, column_name, py_type, entity_name)

    # entity
    tab = '    '
    filter_intent = f"\n\n{tab}"
    for template_name, file_name in [('entity_template.txt', entity_name), ('criterion_template.txt', f"{entity_name}Criterion")]:
        template = pkg_resources.files(resources).joinpath(template_name).read_text()
        template = template.format(entity_name=entity_name, table=table, columns=f'\n{tab}'.join(columns),
                                   sets=filter_intent.join(sets), filters=filter_intent.join(filters),
                                   entity_package=entity_package.__package__)
        entity_file = pkg_resources.files(entity_package).joinpath(f"{file_name}.py")
        with entity_file.open('w', encoding='utf-8') as file:
            file.write(template)

    # dao
    template = pkg_resources.files(resources).joinpath('dao_template.txt').read_text()
    template = template.format(base_dao_package=base_dao_package.__package__, base_dao_name=base_dao_name,
                               entity_package=entity_package.__package__, entity_name=entity_name, entity_variable=underlined_word)
    entity_file = pkg_resources.files(dao_package).joinpath(f"{entity_name}Dao.py")
    with entity_file.open('w', encoding='utf-8') as file:
        file.write(template)
