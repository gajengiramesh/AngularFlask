import logging
from sqlalchemy import desc, asc, inspect
from sqlalchemy.orm import load_only


_logger = logging.getLogger(__name__)

class ModelService():

    def __init__(self,session,request_user,id_field,model,schema,active_only=True):
        self.session = session
        self.request_user = request_user
        self.id_field = id_field
        self.model = model
        self.schema = schema
        self.active_only = active_only
        self._default_fields = None
        self._relation_fields = None

    def get_query(self,**kwargs):
        obj_id = kwargs.get("obj_id")
        fields = kwargs.get("fields")
        sort = kwargs.get("sort")
        limit = kwargs.get("limit")
        offset = kwargs.get("offset")


        query = self.get_query_join(**kwargs)

        query_options = self.get_query_options(**kwargs)

        if query_options:
            query = query.options(*query_options)

        if obj_id:
            query = query.filter(getattr(self.model,self.id_field) == obj_id)

        if self.active_only:
            query = query.filter(getattr(self.model,'is_active') == 'Y')

        query = self.handle_query_filter(query,**kwargs)

        if sort:
            order = self.get_order_by(sort)
            query = query.order_by(*order)
        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        return query

    def get_objects(self,**kwargs):
        query = self.get_query(**kwargs)
        objects = query.all()
        objects = self.handle_objects(objects,**kwargs)
        return objects

    def get_objects_dump(self,**kwargs):
        objects = self.get_objects(**kwargs)
        schema = self.get_schema(**kwargs)
        if schema:
            resp = schema.dump(objects)
        else:
            resp = objects
        return resp

    def get_order_by(self,sort):
        order = []
        for x in sort:
            col = None
            if x[0] =="-":
                col = desc(getattr(self.model,x[1:]))
            elif x[0] =="+":
                col = asc(getattr(self.model,x[1:]))
            else:
                col = asc(getattr(self.model, x))
            order.append(col)
        return order

    def _resolve_fields(self):
        _model = inspect(self.model)
        default_fields = [col.key for col in _model.column_attrs if not col.deferred]
        self._default_fields = default_fields
        self._relation_fields = _model.relationships.keys()

    def get_default_fields(self):
        if self._default_fields is None:
            self._resolve_fields()
        return self._default_fields

    def get_relation_fields(self):
        if self._relation_fields is None:
            self._resolve_fields()
        return self._relation_fields

    def get_default_schema_fields(self):
        schema_fields = [x for x in list(self.schema().dump_fields.keys()) if (x not in self.get_relation_fields() or x in self.get_default_fields())]
        return schema_fields

    def get_query_options(self,**kwargs):
        _query_options = []
        fields = kwargs.get("fields")
        _fields = None
        if fields:
            if '*' in fields:
                _fields = list(set(self.get_default_fields()+fields))
                _fields.remove('*')
            else:
                _fields = fields
        else:
            _fields = self.get_default_fields()

        if _fields:
            kwargs["fields"] = _fields

        non_rel_fields = [getattr(self.model,col) for col in _fields if col not in self.get_relation_fields()]
        if non_rel_fields:
            _query_options.append(load_only(*non_rel_fields))

        _query_options = self.handle_query_options(_query_options,**kwargs)
        return _query_options

    def get_schema(self,**kwargs):
        fields = kwargs.get("fields")
        if self.schema is None:
            return None

        _fields = None
        if fields:
            if '*' in fields:
                _fields = list(set(self.get_default_schema_fields()+fields))
                _fields.remove('*')
            else:
                _fields = fields
        else:
            _fields = self.get_default_schema_fields()

        schema = self.schema(only=_fields,many=True)
        schema = self.handle_schema(schema,**kwargs)
        return schema

    def handle_query_options(self,query_options,**kwargs):
        return query_options

    def handle_query_filter(self,query,**kwargs):
        return query

    def handle_objects(self,objects,**kwargs):
        return objects
    def handle_schema(self,schema,**kwargs):
        return schema
    def get_query_join(self,**kwargs):
        return self.session.query(self.model)


