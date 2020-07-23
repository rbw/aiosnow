# Examples

The `run.py` script can be used to easily testing out the example code.

```bash
$ python3 examples/run.py table.read.nested
```

Read
----

| path               | description |
|--------------------|-------------|
|table.read.nested   |Query Incident records with nested AssignmentGroup|
|table.read.stream   |Fetch Incident records using a Pagestream|
|table.read.one      |Fetch a single Incident by number|
|table.read.selective|Fetch records with a subset of fields of the default IncidentSchema schema|

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
