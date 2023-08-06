# dsmlibrary-viz

- install 
```
pip install dsmlibrary-viz
```

- use
```python
from dsmlibrary_viz.data_viz import DataViz

dataviz = DataViz(
    token="<token>",
    dataplatform_api_uri="<dataplatform_api_uri>", 
    object_storage_uri="<object_storage_uri>"
)

data = dataviz.query(
"""
    SELECT * FROM 'DISCOVERY:<FILE_ID>'
    LIMIT 10
""" 
)
print(data)
```