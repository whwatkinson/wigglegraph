from typing import Optional

from pydantic import BaseModel

from enum import Enum


class PropertyType(Enum):
    NONE_TYPE = "NONE_TYPE"
    BOOL_TYPE = "BOOL_TYPE"
    FLOAT_TYPE = "FLOAT_TYPE"
    INT_TYPE = "INT_TYPE"
    LIST_TYPE = "LIST_TYPE"
    STRING_TYPE = "STRING_TYPE"


class ExtractedProperty(BaseModel):
    property_value: str
    property_type: PropertyType


class MakeProperty(BaseModel):
    property_name: str
    property_value: str
    none_type: Optional[str]
    bool_type: Optional[str]
    float_type: Optional[str]
    int_type: Optional[str]
    list_type: Optional[str]
    string_type: Optional[str]

    def yield_extracted_property(self) -> ExtractedProperty:
        """
        When using ALL_PARAMS_KEY_VALUE_REGEX on a property then calling groupdict() on the match.
        e.g.
            {str: 'foo'} -> {"string": 'foo'}

        This output


        :return:
        """
        skips = {"property_name", "property_value"}
        # return  {k: v for k, v in self.dict(exclude_none=True).items() if k not in skips}

        output = [
            prop_type
            for prop_type, v in self.dict(exclude_none=True).items()
            if prop_type not in skips
        ]
        if len(output) != 1:
            raise Exception()

        prop_type_enum = PropertyType[output[0].upper()]

        return ExtractedProperty(
            property_value=self.property_value, property_type=prop_type_enum
        )
