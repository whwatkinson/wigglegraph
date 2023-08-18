# FIND

INSERT FIND PIC HERE:

## Aims
* To be simple and intuitive to use, the language itself is declarative in nature.
* In the case of an Error providing helpful suggestions back to the User on how to fix the MAKE statement.
* Flexable schema, add and remove as and when.
* Multiple Noe and Relationship creation at once.

## Introduction
* The WQL FIND clause is how data is found on the graph.
* The syntax of FIND is similar to the MAKE clause and is declarative.
* By expressing the nodes and patterns
* Currently only support for patterns of a maximum of three node and two relationships per MAKE statement. However, multiple make statements can be used
    * Minimum pattern:  (**left**)
    * Maximum pattern:  (**left**)-[**REL1**]->(**middle**)-[**REL2**]->(**right**)

## How to use FIND

* FIND uses the same syntax as MAKE.

### Using just FIND

#### Single Nodes

1. Finding all nodes.
   ```
   FIND (nodes);
   ```
2. Finding all nodes with a node label of NodeLabel
   ```
   FIND (:NodeLabel);
   ```
3. Finding all nodes with a node label of NodeLabel and a node handle of NodeHandle which can be used in CRITERIA or REPORT.
   ```
   FIND (NodeHandle:NodeLabel);
   ```
4. Finding all nodes with a node label of NodeLabel, with a node property called prop1 that is foo
   ```
   FIND (:NodeLabel {prop1: "foo"});
   ```
5. Its also possible to specify more than one Node.
   ```
   FIND (:NodeLabel1), (:NodeLabel2);
   ```

#### Two Nodes with a Relationship
1. Finding all nodes that have at least one relationship.
   ```
   FIND (node)-[r]->(node2);
   ```
2. Finding all nodes that have at least one relationship with a relationship label of REL.
   ```
   FIND (node)-[:REL]->(node2);
   ```
5. Finding all nodes that have at least one relationship with a relationship label of REL and a relationship handle of RelHandle which can be used in CRITERIA or REPORT.
   ```
   FIND (node)-[RelHandle:REL]->(node2);
   ```
4. Finding all nodes that have at least one relationship with a relationship label of REL with a node property called prop1 that is foo
   ```
   FIND (node)-[:REL {prop1: "foo"}]->(node2);
   ```
5. This can then be expanded up to a maximum of three nodes and Two relationships.
   ```
   FIND (node)<-[r1:REL {relprop1: "foo"}]-(node2)-[r2:REL2 {relprop2: "bar"}]->(node3);
   ```


### In conjunction with a CRITERIA statement.
* On thew way.
