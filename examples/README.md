# Examples

These are fully functional examples, for developers to quickly get a feel for the Snow library API.

The `run.py` script can be used to easily execute examples.

```bash
$ python run.py table.read.nested
```

Read
----

| path               | description |
|--------------------|-------------|
|table.read.nested   |Query Incident records with nested AssignmentGroup and |
|table.read.stream   |Fetch Incident records using a Pagestream|
|table.read.one      |Fetch a single Incident by number|
|table.read.selective|Fetch records with a subset of fields of the built-in IncidentSchema schema|

Create
------

| path                 | description |
|----------------------|-------------|
|table.create|Create a new Incident record|

Update
------

| path                 | description |
|----------------------|-------------|
|table.update.by_id|Update an Incident record by ID|
|table.update.by_number|Update an Incident record by number|

Delete
------

| path                 | description |
|----------------------|-------------|
|table.delete.by_number|Delete an Incident record by number|
|table.delete.by_sysid |Delete an Incident record by ID|
