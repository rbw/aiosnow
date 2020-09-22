# Examples

This is a set of working examples for use with the included runner, `run.py`.

The idea is to provide something easily executed, that can be tinkered with – for new users
to get an idea of how the library works.

Simply clone this repo, modify the `run.py` script as needed and execute from the project root, e.g.:

```bash
$ python3 examples/run.py table.read.nested
```



Read
----

| path               | description | arguments    |
|--------------------|-------------|--------------|
|table.read.nested   |Query Incident records with nested AssignmentGroup|None|
|table.read.stream   |Fetch Incident records using a memory friendly Pagestream|None|
|table.read.one      |Fetch a single Incident by number|number|

Create
------

| path                 | description | arguments |
|----------------------|-------------|-----------|
|table.create|Create a new Incident record|None|

Update
------

| path                 | description | arguments |
|----------------------|-------------|-----------|
|table.update.by_id|Update an Incident record by ID|sys_id|
|table.update.by_number|Update an Incident record by number|number|

Delete
------

| path                 | description | arguments |
|----------------------|-------------|-----------|
|table.delete.by_number|Delete an Incident record by number|number|
|table.delete.by_sysid |Delete an Incident record by ID|sys_id|
