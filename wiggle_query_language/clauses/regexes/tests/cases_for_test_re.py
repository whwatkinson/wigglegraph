import pytest

from testing.test_helpers import does_not_raise

cases_for_test_nodes_rel_pattern = [
    pytest.param(
        "MAKE (:LeftNodeLabel1);",
        [
            {
                "left_node": "(:LeftNodeLabel1)",
                "left_node_handle": "",
                "left_node_label": "LeftNodeLabel1",
                "left_node_props": None,
                "left_middle_rel": None,
                "left_middle_rel_handle": None,
                "left_middle_rel_label": None,
                "left_middle_rel_props": None,
                "middle_node": None,
                "middle_node_handle": None,
                "middle_node_label": None,
                "middle_node_props": None,
                "middle_right_rel": None,
                "middle_right_rel_handle": None,
                "middle_right_rel_label": None,
                "middle_right_rel_props": None,
                "right_node": None,
                "right_node_handle": None,
                "right_node_label": None,
                "right_node_props": None,
            }
        ],
        does_not_raise(),
        id="EXP PASS: One Node",
    ),
    pytest.param(
        "MAKE (left_node_handle1:LeftNodeLabel1{int: 1}), (left_node_handle2:LeftNodeLabel2{int: 1}), (left_node_handle3:LeftNodeLabel3{int: 1});",
        [
            {
                "left_node": "(left_node_handle1:LeftNodeLabel1{int: 1})",
                "left_node_handle": "left_node_handle1",
                "left_node_label": "LeftNodeLabel1",
                "left_node_props": "{int: 1}",
                "left_middle_rel": None,
                "left_middle_rel_handle": None,
                "left_middle_rel_label": None,
                "left_middle_rel_props": None,
                "middle_node": None,
                "middle_node_handle": None,
                "middle_node_label": None,
                "middle_node_props": None,
                "middle_right_rel": None,
                "middle_right_rel_handle": None,
                "middle_right_rel_label": None,
                "middle_right_rel_props": None,
                "right_node": None,
                "right_node_handle": None,
                "right_node_label": None,
                "right_node_props": None,
            },
            {
                "left_node": "(left_node_handle2:LeftNodeLabel2{int: 1})",
                "left_node_handle": "left_node_handle2",
                "left_node_label": "LeftNodeLabel2",
                "left_node_props": "{int: 1}",
                "left_middle_rel": None,
                "left_middle_rel_handle": None,
                "left_middle_rel_label": None,
                "left_middle_rel_props": None,
                "middle_node": None,
                "middle_node_handle": None,
                "middle_node_label": None,
                "middle_node_props": None,
                "middle_right_rel": None,
                "middle_right_rel_handle": None,
                "middle_right_rel_label": None,
                "middle_right_rel_props": None,
                "right_node": None,
                "right_node_handle": None,
                "right_node_label": None,
                "right_node_props": None,
            },
            {
                "left_node": "(left_node_handle3:LeftNodeLabel3{int: 1})",
                "left_node_handle": "left_node_handle3",
                "left_node_label": "LeftNodeLabel3",
                "left_node_props": "{int: 1}",
                "left_middle_rel": None,
                "left_middle_rel_handle": None,
                "left_middle_rel_label": None,
                "left_middle_rel_props": None,
                "middle_node": None,
                "middle_node_handle": None,
                "middle_node_label": None,
                "middle_node_props": None,
                "middle_right_rel": None,
                "middle_right_rel_handle": None,
                "middle_right_rel_label": None,
                "middle_right_rel_props": None,
                "right_node": None,
                "right_node_handle": None,
                "right_node_label": None,
                "right_node_props": None,
            },
        ],
        does_not_raise(),
        id="EXP PASS: Three Nodes separately",
    ),
    pytest.param(
        "MAKE (left_node_handle:LeftNodeLabel) -[:]-> (middle_node_label:MiddleNodeLabel);",
        [
            {
                "left_node": "(left_node_handle:LeftNodeLabel) ",
                "left_node_handle": "left_node_handle",
                "left_node_label": "LeftNodeLabel",
                "left_node_props": None,
                "left_middle_rel": "-[:]-> ",
                "left_middle_rel_handle": "",
                "left_middle_rel_label": "",
                "left_middle_rel_props": None,
                "middle_node": "(middle_node_label:MiddleNodeLabel)",
                "middle_node_handle": "middle_node_label",
                "middle_node_label": "MiddleNodeLabel",
                "middle_node_props": None,
                "middle_right_rel": None,
                "middle_right_rel_handle": None,
                "middle_right_rel_label": None,
                "middle_right_rel_props": None,
                "right_node": None,
                "right_node_handle": None,
                "right_node_label": None,
                "right_node_props": None,
            }
        ],
        does_not_raise(),
        id="EXP PASS: Double Node, no rel name",
    ),
    pytest.param(
        "MAKE (left_node_handle:LeftNodeLabel) ---[:]---> (middle_node_label:MiddleNodeLabel);",
        [
            {
                "left_node": "(left_node_handle:LeftNodeLabel) ",
                "left_node_handle": "left_node_handle",
                "left_node_label": "LeftNodeLabel",
                "left_node_props": None,
                "left_middle_rel": "---[:]---> ",
                "left_middle_rel_handle": "",
                "left_middle_rel_label": "",
                "left_middle_rel_props": None,
                "middle_node": "(middle_node_label:MiddleNodeLabel)",
                "middle_node_handle": "middle_node_label",
                "middle_node_label": "MiddleNodeLabel",
                "middle_node_props": None,
                "middle_right_rel": None,
                "middle_right_rel_handle": None,
                "middle_right_rel_label": None,
                "middle_right_rel_props": None,
                "right_node": None,
                "right_node_handle": None,
                "right_node_label": None,
                "right_node_props": None,
            }
        ],
        does_not_raise(),
        id="EXP PASS: Double Node, long rel dashes",
    ),
    pytest.param(
        """MAKE (left_node_handle:LeftNodeLabel{int: 1, str: '2', str2:"2_4")-[:]->(middle_node_label:MiddleNodeLabel { float: 3.14, list: [1, '2', "2_4", "3 4", 3.14], email: "harry@wg.net"});""",
        [
            {
                "left_node": "(left_node_handle:LeftNodeLabel{int: 1, str: '2', str2:\"2_4\")",
                "left_node_handle": "left_node_handle",
                "left_node_label": "LeftNodeLabel",
                "left_node_props": "{int: 1, str: '2', str2:\"2_4\"",
                "left_middle_rel": "-[:]->",
                "left_middle_rel_handle": "",
                "left_middle_rel_label": "",
                "left_middle_rel_props": None,
                "middle_node": '(middle_node_label:MiddleNodeLabel { float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14], email: "harry@wg.net"})',
                "middle_node_handle": "middle_node_label",
                "middle_node_label": "MiddleNodeLabel",
                "middle_node_props": '{ float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14], email: "harry@wg.net"}',
                "middle_right_rel": None,
                "middle_right_rel_handle": None,
                "middle_right_rel_label": None,
                "middle_right_rel_props": None,
                "right_node": None,
                "right_node_handle": None,
                "right_node_label": None,
                "right_node_props": None,
            }
        ],
        does_not_raise(),
        id="EXP PASS: Double Node with params",
    ),
    pytest.param(
        """MAKE (left_node_handle:LeftNodeLabel{int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, list: [1, '2', "2_4", "3 4", 3.14]})-[rlm:RELLM{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]}]->(middle_node_label:MiddleNodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]} );""",
        [
            {
                "left_node": '(left_node_handle:LeftNodeLabel{int: 1, str: \'2\', str2:"2_4", float: 3.14, bool: true, list: [1, \'2\', "2_4", "3 4", 3.14]})',
                "left_node_handle": "left_node_handle",
                "left_node_label": "LeftNodeLabel",
                "left_node_props": '{int: 1, str: \'2\', str2:"2_4", float: 3.14, bool: true, list: [1, \'2\', "2_4", "3 4", 3.14]}',
                "left_middle_rel": '-[rlm:RELLM{int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]}]->',
                "left_middle_rel_handle": "rlm",
                "left_middle_rel_label": "RELLM",
                "left_middle_rel_props": '{int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]}',
                "middle_node": '(middle_node_label:MiddleNodeLabel {int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]} )',
                "middle_node_handle": "middle_node_label",
                "middle_node_label": "MiddleNodeLabel",
                "middle_node_props": '{int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]} ',
                "middle_right_rel": None,
                "middle_right_rel_handle": None,
                "middle_right_rel_label": None,
                "middle_right_rel_props": None,
                "right_node": None,
                "right_node_handle": None,
                "right_node_label": None,
                "right_node_props": None,
            }
        ],
        does_not_raise(),
        id="EXP PASS: Double Node with Named Rel and params",
    ),
    pytest.param(
        """MAKE (left_node_handle:LeftNodeLabel{int: 1}) -[:]-> (middle_node_label:MiddleNodeLabel) -[:]->(right_node_label:RightNodeLabel);""",
        [
            {
                "left_node": "(left_node_handle:LeftNodeLabel{int: 1}) ",
                "left_node_handle": "left_node_handle",
                "left_node_label": "LeftNodeLabel",
                "left_node_props": "{int: 1}",
                "left_middle_rel": "-[:]-> ",
                "left_middle_rel_handle": "",
                "left_middle_rel_label": "",
                "left_middle_rel_props": None,
                "middle_node": "(middle_node_label:MiddleNodeLabel) ",
                "middle_node_handle": "middle_node_label",
                "middle_node_label": "MiddleNodeLabel",
                "middle_node_props": None,
                "middle_right_rel": "-[:]->",
                "middle_right_rel_handle": "",
                "middle_right_rel_label": "",
                "middle_right_rel_props": None,
                "right_node": "(right_node_label:RightNodeLabel)",
                "right_node_handle": "right_node_label",
                "right_node_label": "RightNodeLabel",
                "right_node_props": None,
            }
        ],
        does_not_raise(),
        id="EXP PASS: Three Node with rels not names",
    ),
    pytest.param(
        """MAKE (left_node_handle:LeftNodeLabel{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]})-[lm:RELLM{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]}]->(middle_node_label:MiddleNodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]})-[rmr:RELMR{int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]}]->(right_node_label:RightNodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, bool: true, list: [1, '2', "2_4", "3 4", 3.14]} );""",
        [
            {
                "left_node": '(left_node_handle:LeftNodeLabel{int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]})',
                "left_node_handle": "left_node_handle",
                "left_node_label": "LeftNodeLabel",
                "left_node_props": '{int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]}',
                "left_middle_rel": '-[lm:RELLM{int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]}]->',
                "left_middle_rel_handle": "lm",
                "left_middle_rel_label": "RELLM",
                "left_middle_rel_props": '{int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]}',
                "middle_node": '(middle_node_label:MiddleNodeLabel {int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]})',
                "middle_node_handle": "middle_node_label",
                "middle_node_label": "MiddleNodeLabel",
                "middle_node_props": '{int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]}',
                "middle_right_rel": '-[rmr:RELMR{int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]}]->',
                "middle_right_rel_handle": "rmr",
                "middle_right_rel_label": "RELMR",
                "middle_right_rel_props": '{int: 1, str: \'2\', str2:"2_4", float: 3.14, list: [1, \'2\', "2_4", "3 4", 3.14]}',
                "right_node": '(right_node_label:RightNodeLabel {int: 1, str: \'2\', str2:"2_4", float: 3.14, bool: true, list: [1, \'2\', "2_4", "3 4", 3.14]} )',
                "right_node_handle": "right_node_label",
                "right_node_label": "RightNodeLabel",
                "right_node_props": '{int: 1, str: \'2\', str2:"2_4", float: 3.14, bool: true, list: [1, \'2\', "2_4", "3 4", 3.14]} ',
            }
        ],
        does_not_raise(),
        id="EXP PASS: Three Nodes, named rels and with params",
    ),
]
