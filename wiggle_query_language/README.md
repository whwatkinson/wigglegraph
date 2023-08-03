# Wiggle Query Language, WQL

### Introduction
- In a Graph database, date is represented as Nodes and Edges.
- This representation makes it easy to express and explore complex relationships between data points.

### Design philosophy and considerations
- Syntactically similar to the [Cypher Query Language](https://neo4j.com/developer/cypher/)
- Main clauses are case-insensitive.
- Clauses are separated by a semicolon (;).



### Clauses:

```commandline
MAKE (n:NodeLabel)-[:]->(n:NodeLabel);
FIND (p:NodeLabel)-[:]->(q:NodeLabel);
CRITERIA p.name = "Bar" or q.name = "Bar;
REPORT wn(p), wn(q);
```

- Make
- Find
- Criteria
- Report
