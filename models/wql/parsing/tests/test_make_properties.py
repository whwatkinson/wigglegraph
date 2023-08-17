import pytest

from exceptions.wql.parsing import PropertyTypeAssignmentError
from models.wql.parsing.properties_pre import (
    ExtractedPropertyPre,
    WiggleGraphPropertyPre,
)
from models.wql.enums.property_type import PropertyType
from testing.test_helpers import does_not_raise


class TestMakeProprietiesModels:
    @pytest.mark.parametrize(
        "test_make_property, expected_extracted_property, exception",
        [
            pytest.param(
                WiggleGraphPropertyPre(
                    property_name="foo", property_value="bar", string_type="bar"
                ),
                ExtractedPropertyPre(
                    property_value="bar", property_type=PropertyType.STRING_TYPE
                ),
                does_not_raise(),
                id="EXP PASS: Correct assignment",
            ),
            pytest.param(
                WiggleGraphPropertyPre(
                    property_name="foo",
                    property_value="bar",
                    string_type="bar",
                    bool_type="bar",
                ),
                None,
                pytest.raises(PropertyTypeAssignmentError),
                id="EXP EXEC: Two proprieties",
            ),
        ],
    )
    def test_emit_nodes(
        self,
        test_make_property: WiggleGraphPropertyPre,
        expected_extracted_property: ExtractedPropertyPre,
        exception,
    ):
        with exception:
            test = test_make_property.yield_extracted_property()

            assert test == expected_extracted_property
