import datetime
from typing import List, Optional

from .delta_template import DeltaTemplate


class Serializer:
    DATE_DEFAULT = "%Y-%m-%d"
    DATETIME_DEFAULT = "%Y-%m-%dT%H:%M:%S"
    TIMEDELTA_DEFAULT = "%DT%H:%M:%S"

    def __init__(
        self,
        rename: dict = {},
        include_statics: bool = False,
        exclude: List[str] = None,
        include: List[str] = None,
        datetime_format: str = DATETIME_DEFAULT,
        date_format: str = DATE_DEFAULT,
        timedelta_format: str = TIMEDELTA_DEFAULT,
    ):
        self.exclude = exclude
        self.include = include
        self.datetime_format = datetime_format
        self.date_format = date_format
        self.timedelta_format = timedelta_format
        self.include_statics = include_statics
        self.rename = rename

    def field_validator(self, fields: list) -> list:
        valid_fields = list()
        for field in fields:
            if not getattr(field, "editable", False) and not self.include_statics:
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
        image_fields = list()
        timedelta_fields = list()
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
            elif field_type == "ImageField":
                image_fields.append(field)
            elif field_type == "DurationField":
                timedelta_fields.append(field)
            else:
                simple_fields.append(field)

        data = dict()
        data["date_time"] = datetime_fields
        data["date_field"] = date_fields
        data["foreign_key"] = foreign_key_fields
        data["one_to_one"] = one_to_one_fields
        data["many_to_many"] = many_to_many_fields
        data["file"] = file_fields
        data["image"] = image_fields
        data["timedelta"] = timedelta_fields
        data["simple"] = simple_fields
        return data

    def single_object_field_resolver(self, obj, field, depth: Optional[int] = None):
        if getattr(obj, field.attname, False):
            related_object = getattr(obj, field.attname)
            if depth == 0:
                return related_object.id
            elif depth and depth != 0:
                serializered_model = self.model_serializer(
                    related_object, depth=depth - 1
                )
                return serializered_model
            else:
                serializered_model = self.model_serializer(related_object)
                return serializered_model

    def many_object_field_resolver(
        self, obj, field, depth: Optional[int] = None,
    ):
        if getattr(obj, field.attname, False):
            related_objects = getattr(obj, field.attname).all()
            if depth == 0:
                related_ids = [item.id for item in related_objects]
                return related_ids
            elif depth and depth != 0:
                serializered_model = self.serialize(related_objects, depth=depth - 1)
                return serializered_model
            else:
                serializered_model = self.serialize(related_objects)
                return serializered_model

    def timedelta_resolver(self, obj, field):
        timedelta_object = getattr(obj, item.attname)
        data = {}
        data["y"], remaining = divmod(timedelta_object.days, 365)
        data["m"], data["d"] = divmod(remaining, 30)
        data["D"] = timedelta_object.days
        data["H"], remaining = divmod(timedelta_object.seconds, 3600)
        data["M"], data["S"] = divmod(remaining, 60)

        template_object = DeltaTemplate(self.timedelta_format)
        # TODO: SOME ERROR HANDELING SHOULD TAKE PALCE AROUND HERE
        timedelta_string = template_object.substitute(**data)
        return timedelta_string

    @staticmethod
    def value_from_object(field, obj):
        """Return the value of this field in the given model instance."""
        return getattr(obj, field.attname)

    def field_name_selector(self, field):
        if field.attname in self.rename:
            alter_name = self.rename[field.attname]
            if not isinstance(alter_name, str):
                raise ValueError("Alternative Name Must Be String")
            return alter_name
        else:
            return field.attname

    def field_value_resolver(self, obj, depth: Optional[int] = None, **kwargs) -> dict:
        date_time = kwargs.get("date_time", [])
        date_field = kwargs.get("date_field", [])
        foreign_key = kwargs.get("foreign_key", [])
        one_to_one = kwargs.get("one_to_one", [])
        many_to_many = kwargs.get("many_to_many", [])
        file = kwargs.get("file", [])
        image = kwargs.get("image", [])
        timedelta = kwargs.get("timedelta", [])
        simple = kwargs.get("simple", [])
        if depth:
            try:
                depth = int(depth)
            except ValueError:
                raise ValueError("Depth Parameter Must Be Integer")
        data = dict()
        # datetime field resolver
        for item in date_time:
            data[self.field_name_selector(item)] = datetime.datetime.strftime(
                getattr(obj, item.attname), self.datetime_format
            )
        # date field resolver
        for item in date_field:
            data[self.field_name_selector(item)] = datetime.datetime.strftime(
                getattr(obj, item.attname), self.date_format
            )
        # foreign key resolver
        for item in foreign_key:
            data[self.field_name_selector(item)] = self.single_object_field_resolver(
                obj=obj, field=item, depth=depth,
            )
        # one to one field resolver
        for item in one_to_one:
            data[self.field_name_selector(item)] = self.single_object_field_resolver(
                obj=obj, field=item, depth=depth
            )
        # many to many field resolver
        for item in many_to_many:
            data[self.field_name_selector(item)] = self.many_object_field_resolver(
                obj=obj, field=item, depth=depth
            )

        # file field resolver
        for item in file:
            field_file = getattr(obj, item.attname)
            data[self.field_name_selector(item)] = field_file.url

        # image field resolver
        for item in image:
            field_image = getattr(obj, item.attname)
            data[self.field_name_selector(item)] = field_image.url

        # timedelta field resolver
        for item in timedelta:
            data[self.field_name_selector(item)] = self.timedelta_resolver(
                obj, field=item
            )

        # simple fields resolver
        for item in simple:
            data[self.field_name_selector(item)] = self.value_from_object(item, obj)
        return data

    def model_serializer(self, obj, depth: Optional[int] = None,) -> dict:
        opts = obj._meta
        fields = (
            list(opts.concrete_fields)
            + list(opts.private_fields)
            + list(opts.many_to_many)
        )
        fields = self.field_validator(fields)
        classified_fields = self.fields_classifier(fields)
        serialized_model = self.field_value_resolver(
            obj=obj, depth=depth, **classified_fields
        )
        return serialized_model

    def serialize(self, objs, depth: Optional[int] = None,) -> Optional[dict]:
        if hasattr(objs, "__iter__") or hasattr(objs, "__getitem__"):
            is_iterable = True
        else:
            is_iterable = False

        if not objs and is_iterable:
            return []
        if not objs and not is_iterable:
            return None

        if not is_iterable:
            data = self.model_serializer(obj=objs, depth=depth,)
            return data
        else:
            data = list()
            for obj in objs:
                item_dict = self.model_serializer(obj=obj, depth=depth,)
                data.append(item_dict)
            return data
