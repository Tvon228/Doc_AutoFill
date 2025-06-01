from enum import StrEnum


class FieldDataTypeEnum(StrEnum):
    NUMBER = "num"
    TEXT = "text"
    DATE = "date"
    OBJECT_ATTRIBUTE = "obj_attr"


class FieldTypeEnum(StrEnum):
    SCALAR = "scalar"
    OBJ_ATTR = "obj_attr"

    def __repr__(self):
        return f"<{self.value}>"
