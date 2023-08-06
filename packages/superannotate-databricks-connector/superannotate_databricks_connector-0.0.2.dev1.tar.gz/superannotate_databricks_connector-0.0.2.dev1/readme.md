# Superannotate Databricks Connector
SuperAnnotate is the cornerstone of your data labeling pipeline. It brings you a cutting-edge annotation tool for all types of data including image, video, text, LiDAR, audio, and more.

This Python package provides a set of utilities for working with SuperAnnotate data on Databricks. It includes functionality to process SuperAnnotate data and save it to Delta tables.


### Features
Convert superannotate annotation data to Apache Spark&trade; Data Frames. 
Project types supported:
    - Vector
    - Text



### Example notebooks.
Copy the notebooks in the demo folder to your databricks workspace to get started with SuperAnnotate quickly!

### Installation
```bash
pip install superannotate_databricks_connector
``` 

### Tests

Run tests by building the Dockerfile.test file using

```bash
docker build -f Dockerfile.test -t test_package .
```

If you are running the tests for the first you first have to build the base dockerfile containing pyspark.

```bash
docker build -f Dockerfile.spark -t spark_docker_base .
```

### Build package

In the main directory, run the following to generate a .whl file. 

```bash
python -m build
```

### Usage
First import the required function

```python
from superannotate_databricks_conector.vector import get_vector_dataframe
from superannotate import SAClient
```

You can then convert your annotations to a spark dataframe

```python
sa = SAClient(token="<TOKEN>")
annotations = sa.get_annotations("<PROJECT_NAME>)
df = get_vector_dataframe(annotations, spark)
```


