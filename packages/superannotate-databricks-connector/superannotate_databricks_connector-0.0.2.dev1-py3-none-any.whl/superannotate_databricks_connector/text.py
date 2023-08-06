from datetime import datetime
from superannotate_databricks_connector.schemas.text_schema import (
    get_text_schema
)


def convert_dates(instance):
    """
    Parses the date columns createdAt and updatedAt
    in instances to datetime format

    Args:
        instance (dict): One annotation instance

    Returns:
        instance: The instance with date columns converted to
                  datetime format.
    """
    instance["createdAt"] = datetime.strptime(
        instance["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
    instance["updatedAt"] = datetime.strptime(
        instance["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
    return instance


def get_text_dataframe(annotations, spark):
    """
    Transforms a list of SuperAnnotate annotations from a text
    project into a spark dataframe

    Args:
        annotations (list[dict]): The annotations in the SuperAnnotate format
        spark (sparkContext): The spark context

    Returns:
        spark_df: A spark dataframe containing the annotations.

    }
    """
    rows = []
    for item in annotations:
        flattened_item = {
            "name": item["metadata"]["name"],
            "url": item["metadata"]["url"],
            "projecId": item["metadata"]["projectId"],
            "status": item["metadata"]["status"],
            "annotatorEmail": item["metadata"]["annotatorEmail"],
            "qaEmail": item["metadata"]["qaEmail"],
            "entities": [convert_dates(instance) for instance
                         in item["instances"] if instance["type"] == "entity"],
            "tags": [convert_dates(instance) for instance in item["instances"]
                     if instance["type"] == "tag"]
        }
        rows.append(flattened_item)
    schema = get_text_schema()
    spark_df = spark.createDataFrame(rows, schema=schema)
    return spark_df
