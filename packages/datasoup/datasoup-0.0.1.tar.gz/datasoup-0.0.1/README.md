```python
import datasoup as ds

dsdb = ds.db.connect("<connection_string>", options={})

dsdb.project.list()

dsdb.project.set("<project_name>", in_place=True)

ds_project = dsdb.project.set("<project_name>", in_place=False)

dsdb.project["<project_name>"].some_method()
```


---

### thoughts

use symlinks to distribute data
or docker-compose to mount projects

