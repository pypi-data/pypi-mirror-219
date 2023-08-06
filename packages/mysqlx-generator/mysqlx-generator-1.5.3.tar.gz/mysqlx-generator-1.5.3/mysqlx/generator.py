import os
from mysqlx import db
from jinja2 import FileSystemLoader, Environment
from typing import Union, Iterable

COMMON_COLS = ['create_by', 'create_time']
ATTRIBUTES = {'__pk__': 'id', '__update_by__': 'update_by', '__update_time__': 'update_time', '__del_flag__': 'del_flag'}


class Generator:
    comma1 = ','
    comma2 = '，'
    sql = '''
    SELECT column_name, data_type, character_maximum_length, NUMERIC_precision, NUMERIC_scale, column_key FROM information_schema.columns
     WHERE table_schema = (SELECT DATABASE()) AND table_name = ? 
    '''

    def __init__(self, user='root', password='', database='test', host='127.0.0.1', port=3306, use_unicode=True, pool_size=1, show_sql=False,
            **kwargs):
        db.init_db(user, password, database, host, port, pool_size, use_unicode, show_sql, **kwargs)

    def generate_with_schema(self, schema: str = None, path: str = None, *args, **kwargs):
        if schema:
            db.execute('use %s' % schema)
        tables = db.select('show tables')
        tables = [table[0] for table in tables]
        self.generate_with_tables(tables=tables, path=path, *args, **kwargs)

    def generate_with_tables(self, tables: Union[str, Iterable[str]], path: str = None, *args, **kwargs):
        metas = None
        only_one_table = False
        if not args:
            args = COMMON_COLS
        if not kwargs:
            kwargs = ATTRIBUTES

        columns = [v for v in kwargs.values()]
        if args:
            args.reverse()
            for i in range(0, len(args)):
                columns.insert(1, args[i])

            # 去重
            base_columns = list(set(columns))
            # 保持原有顺序
            base_columns.sort(key=columns.index)
        else:
            base_columns = columns

        if isinstance(tables, str):
            if self.comma1 in tables:
                tables = tables.split(self.comma1)
            elif self.comma2 in tables:
                tables = tables.split(self.comma2)
            else:
                only_one_table = True
                metas = [self._get_table_meta(tables, base_columns)]

        if not only_one_table:
            if not isinstance(tables, set):
                tables = set(tables)
            metas = [self._get_table_meta(table.strip(), base_columns) for table in tables]

        no_pk_tables = [meta for meta in metas if isinstance(meta, str)]
        if len(no_pk_tables) > 0:
            print("There isn't primary key in the tables %s, it will not generate model class." % no_pk_tables)

        metas = [meta for meta in metas if isinstance(meta, dict)]
        if len(metas) > 0:
            cols = [col for mata in metas for col in mata['super_columns']]
            col_dict = {col['COLUMN_NAME']: col for col in cols}

            def get_type(col):
                if col in col_dict:
                    return col_dict[col]['DATA_TYPE']
                elif col == kwargs.get('__pk__') or col == kwargs.get('__update_by__') or col == kwargs.get('__del_flag__'):
                    return 'int'
                elif col == kwargs.get('__update_time__'):
                    return 'datetime'
                elif col.endswith("_time"):
                    return 'datetime'
                elif col.endswith("_date"):
                    return 'date'
                else:
                    return 'None'

            kwargs['metas'] = metas
            kwargs['base_columns'] = [{'COLUMN_NAME': col, 'DATA_TYPE': get_type(col)} for col in base_columns]
            self._generate(kwargs, path)

    def _get_table_meta(self, table: str, base_columns):
        def convert_type(col_type):
            if col_type in ('int', 'tinyint', 'bigint'):
                return 'int'
            elif col_type in ('float', 'double'):
                return 'float'
            elif col_type == 'decimal':
                return 'Decimal'
            elif col_type in ('char', 'varchar', 'text'):
                return 'str'
            elif col_type in ('date', 'datetime'):
                return col_type
            else:
                return 'None'

        pk = None
        super_columns = []
        columns = db.do_query(self.sql, table)
        for col in columns:
            if col['COLUMN_KEY'] == 'PRI':
                pk = col['COLUMN_NAME']
            if col['COLUMN_NAME'] in base_columns:
                super_columns.append(col)
            col['DATA_TYPE'] = convert_type(col['DATA_TYPE'])

        if pk is None:
            return table

        class_name = self._get_class_name(table)
        return {
            'pk': pk,
            'table': table,
            'class_name': class_name,
            'columns': columns,
            'self_columns': [col for col in columns if col['COLUMN_NAME'] not in base_columns],
            'super_columns': super_columns
        }

    @staticmethod
    def _generate(metas: dict, path: str):
        loader = FileSystemLoader(searchpath=os.path.dirname(__file__))
        environment = Environment(loader=loader)
        tpl = environment.get_template('generator.tpl')
        output = tpl.render(**metas)
        if path:
            suffix = '.py'
            path = path if path.endswith(suffix) else path + suffix
            with open(path, 'w', encoding='utf-8') as f:
                f.write(output)
            print('Model文件已生成：%s' % path)
        else:
            print(output)

    @staticmethod
    def _get_class_name(table):
        if '_' not in table:
            return table.capitalize()

        names = table.split('_')
        names = [name.capitalize() for name in names]
        return ''.join(names)