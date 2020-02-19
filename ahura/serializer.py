import datetime
from typing import List, Optional



class Serializer:
    DATE_DEFAULT = "%Y-%m-%d"
    DATETIME_DEFAULT = "%Y-%m-%dT%H:%M:%S"
    def __init__(
        self,
        exclude: List[str] = None,
        include: List[str] = None,
        datetime_format: str = DATETIME_DEFAULT,
        date_format: str = DATE_DEFAULT):
            self.exclude = exclude
            self.include = include
            self.datetime_format = datetime_format
            self.date_format = date_format
    
    def field_validator(self, fields: list) -> list:
        valid_fields = list()
        for field in fields:
            if not getattr(field, "editable", False):
                continue
            if self.include is not None and field.name not in self.include:
                continue
            if self.exclude and field.name in self.exclude:
                continue
            valid_fields.append(field)
        return valid_fields
    
    @staticmethod
    def fields_classifier(fields: list) -> dict:
        datetime_fields = list()
        date_fields = list()
        foreign_key_fields = list()
        one_to_one_fields = list()
        many_to_many_fields = list()
        file_fields = list()
        simple_fields = list()

        for field in fields:
            field_type = field.get_internal_type()
            if field_type == "DateTimeField":
                datetime_fields.append(field)
            elif field_type == "DateField":
                date_fields.append(field)
            elif field_type == "ForeignKey":
                foreign_key_fields.append(field)
            elif field_type == "OneToOneField":
                one_to_one_fields.append(field)
            elif field_type == "ManyToManyField":
                many_to_many_fields.append(field)
            elif field_type == "FileField":
                file_fields.append(field)
            else:
                simple_fields.append(field)

        data = dict()
        data["date_time"] = datetime_fields
        data["date_field"] = date_fields
        data["foreign_key"] = foreign_key_fields
        data["one_to_one"] = one_to_one_fields
        data["many_to_many"] = many_to_many_fields
        data["file"] = file_fields
        data["simple"] = simple_fields
        return data
    

    def single_object_field_resolver(
        self,
        obj,
        field,
        depth: Optional[int] = None
    ):
        if getattr(obj, field.attname, False):
            related_object = getattr(obj, field.attname)
            if depth == 0:
                return related_object.id
            elif depth and depth != 0:
                serializered_model = self.model_serializer(
                    related_object,
                    depth=depth - 1
                )
                return serializered_model
            else:
                serializered_model = self.model_serializer(
                    related_object
                )
                return serializered_model
    
    def many_object_field_resolver(
        self,
        obj,
        field,
        depth: Optional[int] = None,
    ):
        if getattr(obj, field.attname, False):
            related_objects = getattr(obj, field.attname).all()
            if depth == 0:
                related_ids = [item.id for item in related_objects]
                return related_ids
            elif depth and depth != 0:
                serializered_model = self.serialize(
                    related_objects,
                    depth=depth - 1
                )
                return serializered_model
            else:
                serializered_model = self.serialize(
                    related_objects
                )
                return serializered_model


    @staticmethod
    def value_from_object(field, obj):
        """Return the value of this field in the given model instance."""
        return getattr(obj, field.attname)

    def field_value_resolver(
        self,
        obj,
        date_time: list,
        date_field: list,
        foreign_key: list,
        one_to_one: list,
        many_to_many: list,
        file: list,
        simple: list,
        depth: Optional[int] = None,
    ) -> dict:
        if depth:
            try:
                depth = int(depth)
            except ValueError:
                raise ValueError("Depth Parameter Must Be Integer")
        data = dict()
        # datetime field resolver
        for item in date_time:
            data[item.attname] = datetime.datetime.strftime(
                getattr(obj, item.attname), self.datetime_format
            )
        # date field resolver
        for item in date_field:
            data[item.attname] = datetime.datetime.strftime(
                getattr(obj, item.attname), self.date_format
            )
        # foreign key resolver
        for item in foreign_key:
            data[item.attname] = self.single_object_field_resolver(
                obj=obj,
                field=item,
                depth=depth,
            )
        # one to one field resolver
        for item in one_to_one:
            data[item.attname] = self.single_object_field_resolver(
                obj=obj,
                field=item,
                depth=depth
            )
        # many to many field resolver
        for item in many_to_many:
            data[item.attname] = self.many_object_field_resolver(
                obj=obj,
                field=item,
                depth=depth
            )

        # simple fields resolver
        for item in simple:
            data[item.attname] = self.value_from_object(item, obj)
        return data


    def model_serializer(
        self,
        obj,
        depth: Optional[int] = None,
    ) -> dict:
        opts = obj._meta
        fields = list(opts.concrete_fields) + list(opts.private_fields) + list(opts.many_to_many)
        fields = self.field_validator(fields)
        classified_fields = self.fields_classifier(fields)
        serialized_model = self.field_value_resolver(
            obj=obj, depth=depth,**classified_fields
        )
        return serialized_model
    
    def serialize(
        self,
        objs,
        depth: Optional[int] = None,
    ) -> Optional[dict]:
        if hasattr(objs, "__iter__") or hasattr(objs, "__getitem__"):
            is_iterable = True
        else:
            is_iterable = False

        if not objs and is_iterable:
            return []
        if not objs and not is_iterable:
            return None

        if not is_iterable:
            data = self.model_serializer(
                obj=objs,
                depth=depth,
            )
            return data
        else:
            data = list()
            for obj in objs:
                item_dict = self.model_serializer(
                    obj=obj,
                    depth=depth,
                )
                data.append(item_dict)
            return data






