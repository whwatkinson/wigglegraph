# Wiggle Query Language, WQL

[//]: # (- Having used [NEO4J]&#40;&#41; for a few years I wanted to create a new database. Not as a replacement but rather to increase my understanding of how they work and experience first hand the design deicions made and how the initial ideas can be improved on.)
## Why another query language
1. ¿Por qué no?
2. So I Can add another language to [my project](https://github.com/whwatkinson/hello_world)...
3. Jokes aside, most importantly to keep I wanted to see if I could as well as consoidate a few things I have learnt along the way.
   - What works what and most importantly what doesn't
   - Implement some basic CRUD operations


## Design philosophy and considerations
- Match patterns with declarative language.
- Syntactically similar to the [Cypher Query Language](https://neo4j.com/developer/cypher/)
- Main clauses are case-insensitive.
- Clauses are separated by a semicolon (;), better parsing will come.
- Quick detection of errors and returning a helpful explanation.
- Support for datatypes String, Array, Integer and Float.
- For now, support for creating one relationship at a time.

## Clauses

Checkout `wiggle_query_language/sample_queries` for some examples quires


```commandline
MAKE (n:NodeLabel)-[r:REL]->(n:NodeLabel);
FIND (p:NodeLabel)-[r2:REL]->(q:NodeLabel);
CRITERIA p.name = "Bar" or q.name = "Bar;
REPORT wn(p), wn(q);
```

- Make
- Find
- Adjust
- Criteria
- Report
- BuiltIns
-
