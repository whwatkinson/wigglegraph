from typing import Optional

from pydantic import BaseModel

from models.wql.enums.property_type import PropertyType


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
        Allows for dynamic fetching the extracted property from ALL_PARAMS_KEY_VALUE_REGEX.

        This is then fed into handle_extracted_property which correctly assigns the property type.

        :return: An ExtractedProperty
        """
        skips = {"property_name", "property_value"}

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
