# Make

INSERT MAKE PIC HERE:

The MAKE clause of WQL.

## Introduction
* The MAKE clause is how data is loaded onto the graph.
* The user creates Nodes and Edges by expressing a pattern in the terminal.

## Aims
* To be simple and intuitive to use, the language itself is declarative in nature.
* To be informative to the User and provide helpful feed back to the User in the case of an Error.
* Flexable schema, add and remove as and when.
* Multiple Noe and Relationship creation at once.

## Node and Relationship

### Data types Supported
* Float
* Integer
* String

### Sub Node or Rel structures
* A List of any combination of the above.
* Dictionary and object are not supported. In my view if your resorting to a dict/obj then its own node, change my mind!

## Representation:
* The two basic units of the graph and Node and Edges.
* To create these follow this pattern.

### Nodes
* Nodes are represented in parentheses.
* Where the main data is stored.
* Within the parentheses there are three areas of interest:
  * NodelHandle, NodeLabel, and NodeProperties.
  * This takes the form of:
    * (  **NodelHandle**  :  **NodeLabel** **{NodeProperties}**  )
    * In plain English: Create node with a node with node label of NodeLabel, the properties of NodeLabel are NodeProperties. NodeHandle the is how you can reference it later on with a USING.
    * **NodeHandle**: This is the node I care about. Optional.
    * **NodeLabel**: the type of node I want to create. Required
    * **NodeProperties**: The data associated with this node type. Optional.

### Edges
* Edges in square brackets, note a direction must be specified.
* How is the main data connected?
* Within the square brackets there are three areas of interest:
  * NodelHandle, NodeLabel, and NodeProperties.
  * This takes the form of:
    * (`foo`)-\[  **RelHandle**  :  **RELLABEL** **{RelProperties}**  \]->(`bar`)
    * In plain English: Create relationship between `foo` and `bar` with a relationship label of RelLabel the properties of RelLabel are RelProperties. RelHandle the is how you can reference it later on a with a USING.
    * **RelHandle**: This is the Rel I care about. Optional.
    * **RelLabel**: the type of Rel I want to create, must be uppercase. Optional
    * **RelProperties**: The data associated with this Rel type. Optional.
    * n.b notice a direction of the relationship, in this case left to right.

## Examples

1. Creation of a single node with no properties
   - Use case: INSERT HERE
    ```
    MAKE (:NodeLabel);
    ```
2. Creation of a two node with no properties
   - Use case: INSERT HERE
    ```
    MAKE (:NodeLabel), (:NodeLabel);
    ```
3. Creation of a single node with a node handle
   - Use case: INSERT HERE
    ```
    MAKE (node:NodeLabel);
    ```
4. Creation of a single node with properties
   - Use case: INSERT HERE
    ```
    MAKE (node:NodeLabel {int: 1, str: '2', str2:"2_4", float: 3.14, list: [1, '2', "2_4", "3 4", 3.14]});
    ```
5. Creation of two nodes, without a named relationship.
   - Use case: INSERT HERE
    ```
    MAKE (:NodeLabel)-[]->(:NodeLabel);
    ```
6. Creation of two nodes with a named relationship.
    ```
    MAKE (:NodeLabel)-[:REL]->(:NodeLabel);
    ```
   n.b note upper case RelLabel
7. Creation of two nodes with a named relationship, all have properties.
    ```
    MAKE (:NodeLabel{int: 1})-[rel1:REL{str: '2'}]->(:NodeLabel{str2:"2_4"});
    ```
   n.b note upper case RelLabel
8. Creation of three nodes with two named relationship, all have properties.
    ```
    MAKE (:NodeLabel{int: 1})-[rel1:REL{str: '2'}]->(:NodeLabel{str2:"2_4"})<-[rel2:REL2{float: 3.14}]-(:NodeLabel2{list: [1, '2', "2_4", "3 4", 3.14]}});
    ```
   n.b note upper case RelLabel
