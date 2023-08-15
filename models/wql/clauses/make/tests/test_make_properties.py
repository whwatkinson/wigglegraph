import pytest

from exceptions.wql.make import MakePropertyTypeAssignmentError
from testing.test_helpers import does_not_raise
from models.wql.enums.property_type import PropertyType
from models.wql.clauses.make.make_properties import (
    MakeProperty,
    ExtractedProperty,
)


class TestMakeProprietiesModels:
    @pytest.mark.parametrize(
        "test_make_property, expected_extracted_property, exception",
        [
            pytest.param(
                MakeProperty(
                    property_name="foo", property_value="bar", string_type="bar"
                ),
                ExtractedProperty(
                    property_value="bar", property_type=PropertyType.STRING_TYPE
                ),
                does_not_raise(),
            ),
            pytest.param(
                MakeProperty(
                    property_name="foo",
                    property_value="bar",
                    string_type="bar",
                    bool_type="bar",
                ),
                None,
                pytest.raises(MakePropertyTypeAssignmentError),
            ),
        ],
    )
    def test_emit_nodes(
        self,
        test_make_property: MakeProperty,
        expected_extracted_property: ExtractedProperty,
        exception,
    ):
        with exception:
            test = test_make_property.yield_extracted_property()

            assert test == expected_extracted_property
