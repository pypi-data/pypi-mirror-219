from decimal import Decimal
from datetime import date, datetime
from mysqlx.orm import Model, PkStrategy


class BaseModel(Model):
    __pk__ = '{{__pk__}}'
    __del_flag__ = '{{__del_flag__}}'
    __update_by__ = '{{__update_by__}}'
    __update_time__ = '{{__update_time__}}'
    __pk_strategy__ = PkStrategy.DB_AUTO_INCREMENT

    def __init__(self,{% for item in base_columns %}{% if loop.last %}{% if item.DATA_TYPE=='None' %} {{item.COLUMN_NAME}}=None{% else %} {{item.COLUMN_NAME}}: {{item.DATA_TYPE}} = None{% endif %}{% else %}{% if item.DATA_TYPE=='None' %} {{item.COLUMN_NAME}}=None{% else %} {{item.COLUMN_NAME}}: {{item.DATA_TYPE}} = None{% endif %},{% endif %}{% endfor %}): {% for item in base_columns %}
        self.{{item.COLUMN_NAME}} = {{item.COLUMN_NAME}} {% endfor %}

{% for meta in metas %}
class {{meta.class_name}}(BaseModel):{% if meta.pk != __pk__ %}
    __pk__ = '{{meta.pk}}'{% endif %}
    __table__ = '{{meta.table}}'

    def __init__(self,{% for item in meta.columns %}{% if loop.last %}{% if item.DATA_TYPE=='None' %} {{item.COLUMN_NAME}}=None{% else %} {{item.COLUMN_NAME}}: {{item.DATA_TYPE}} = None{% endif %}{% else %}{% if item.DATA_TYPE=='None' %} {{item.COLUMN_NAME}}=None{% else %} {{item.COLUMN_NAME}}: {{item.DATA_TYPE}} = None{% endif %},{% endif %}{% endfor %}):
        super().__init__({% for item in meta.super_columns %}{% if loop.first %}{{item.COLUMN_NAME}}={{item.COLUMN_NAME}}{% else %}, {{item.COLUMN_NAME}}={{item.COLUMN_NAME}}{% endif %}{% endfor %}) {% for item in meta.self_columns %}
        self.{{item.COLUMN_NAME}} = {{item.COLUMN_NAME}} {% endfor %}

{% endfor %}