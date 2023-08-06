import json
import os.path
import unittest

from tests import DATA_SET_PATH
from pyspark.sql import SparkSession
from src.superannotate_databricks_connector.text import (
    get_text_dataframe
)


class TestVectorDataFrame(unittest.TestCase):
    def test_vector_dataframe(self):
        spark = SparkSession.builder.master("local").getOrCreate()
        with open(os.path.join(DATA_SET_PATH, "text/example_annotation.json"),
                  "r") as f:
            data = json.load(f)

        actual_df = get_text_dataframe([data], spark)

        expected_df = spark.read.parquet(os.path.join(
            DATA_SET_PATH, "text/expected_df.parquet"))
        self.assertEqual(sorted(actual_df.collect()),
                         sorted(expected_df.collect()))
