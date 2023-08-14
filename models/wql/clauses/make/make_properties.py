from typing import Optional


from pydantic import BaseModel


class MakeListProperty(BaseModel):
    property_name: str
    property_value: str


class MakePrimitiveProperty(BaseModel):
    property_name: str
    property_value: str
    none: Optional[str]
    bool: Optional[str]
    float: Optional[str]
    int: Optional[str]
    # list: Optional[str]
    string: Optional[str]

    def yield_extracted_param(self) -> dict:
        skips = {"property_name", "property_value"}

        return {k: v for k, v in self.dict(exclude_none=True).items() if k not in skips}