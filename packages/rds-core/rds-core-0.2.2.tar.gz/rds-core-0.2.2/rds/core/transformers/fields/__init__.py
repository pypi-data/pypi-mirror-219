import logging
from typing import Union, Dict, Any, List
from datetime import datetime
from rds.core.helpers import get_dict_by_pathname

strptime = datetime.strptime


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Field:
    def __init__(self, source_field: Union[str, object, None], none_as: Any = None):
        self.source_field = source_field
        self.none_as = none_as

    def transform_to_dict(self, source_dict: Dict[str, Any], dest_dict: Dict[str, Any], dest_fieldname: str) -> None:
        if self.source_field is None:
            dest_dict[dest_fieldname] = None
        else:
            dest_dict[dest_fieldname] = self.cast_source_value(get_dict_by_pathname(source_dict, self.source_field))

    def cast_source_value(self, source_value: Union[str, int, bool, float]) -> Any:
        return source_value if source_value is not None else self.none_as


class CharField(Field):
    def cast_source_value(self, source_value: Union[str, int, bool, float]) -> str:
        return str(source_value) if source_value is not None else self.none_as


class IntegerField(Field):
    def cast_source_value(self, source_value: Union[None, str, int, float]) -> int:
        return int(source_value)


class FloatField(Field):
    def cast_source_value(self, source_value: Union[None, str, int, float]) -> float:
        return float(source_value)


class DateField(Field):
    def __init__(self, source_field: str, format: str = "%d/%m/%Y"):
        super().__init__(source_field)
        self.format = format

    def cast_source_value(self, source_value: Union[None, str, int, bool, float]) -> datetime.date:
        return strptime(source_value, self.format) if source_value is not None else None


class DateTimeField(Field):
    def __init__(self, source_field: str, format: str = "%d/%m/%Y %H:%M:%S"):
        super().__init__(source_field)
        self.format = format

    def cast_source_value(self, source_value: Union[str, int, bool, float]) -> datetime:
        return strptime(source_value, self.format) if source_value is not None else None


class SimpleConcatField(Field):
    def __init__(self, fields: Union[List[str], None] = None, separator: str = ""):
        super().__init__(None)
        self.fields = fields
        self.separator = separator

    def transform_to_dict(self, source_dict: Dict[str, Any], dest_dict: Dict[str, Any], dest_fieldname: str) -> str:
        if self.fields is not None:
            dest_dict[dest_fieldname] = self.separator.join(
                [self.cast_source_value(get_dict_by_pathname(source_dict, f)) for f in self.fields]
            )


class FixedField(Field):
    def __init__(self, fixed_value: str):
        super().__init__(None)
        self.fixed_value = fixed_value

    def transform_to_dict(self, source_dict: Dict[str, Any], dest_dict: Dict[str, Any], dest_fieldname: str) -> None:
        dest_dict[dest_fieldname] = self.cast_source_value(self.fixed_value)

    def cast_source_value(self, source_value: Any) -> Any:
        return source_value


class SubModelField(Field):
    def transform_to_dict(self, source_dict: Dict[str, Any], dest_dict: Dict[str, Any], dest_fieldname: str):
        dest_dict[dest_fieldname] = self.source_field.transform_to_dict(source_dict)
