# REPORT

INSERT MAKE PIC HERE:

## Aims
* To be simple and intuitive to use, the language itself is declarative in nature.
* In the case of an Error providing helpful suggestions back to the User on how to fix the REPORT statement.
* If a property on a Node or Relationship does not exist then Null is returned.

## Introduction
* **A REPORT must be used in conjunction with a FIND statement.**
* The WQL REPORT clause is how data is displayed back to the user.
* Only one REPORT statement is allowed per query.
* Using * can be used to return all matches.
* Alternatively the handles provided in the FIND statement can be provided for the REPORT

## How to use REPORT

1. Display all matches.
   ```
   FIND *:
   REPORT *;
   ```

2. With a FIND and REPORT all node properties.
   ```
   FIND (foo:Node);
   REPORT foo;
   ```

3. With a FIND and REPORT a specific node property.
   ```
   FIND (foo:Node);
   REPORT foo.bar;
   ```

4. With a FIND and REPORT a multiple node properties.
   ```
   FIND (foo:Node);
   REPORT foo.bar, foo.baz, foo.qux;
   ```

5. With a FIND and REPORT all relationship properties.
   ```
   FIND (foo:Node)-[r:REL]->(foo2:Node2);
   REPORT r;
   ```

6. With a FIND and REPORT a specific relationship property.
   ```
   FIND (foo:Node)-[r:REL]->(foo2:Node2);
   REPORT r.bar;
   ```

7. With a FIND and REPORT a multiple relationship properties.
   ```
   FIND (foo:Node)-[r:REL]->(bar:Node2);
   REPORT r.bar, r.baz, r.qux;
   ```

8. With a FIND and REPORT a multiple node and relationship properties.
    ```
   FIND (foo:Node)-[r:REL]->(bar:Node2);
   REPORT foo.bar, foo.baz, foo.qux, r.bar, r.baz, r.qux;
   ```
