import json
import os.path
import unittest

from tests import DATA_SET_PATH

from pyspark.sql import SparkSession
from superannotate_databricks_connector.vector import (
    process_bounding_box,
    process_vector_object,
    process_vector_tag,
    get_boxes,
    get_vector_dataframe
)


class TestVectorInstances(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        with open(os.path.join(DATA_SET_PATH,
                               "vector/example_annotation.json"), "r") as f:
            data = json.load(f)
        self.test_data = data
        self.spark = SparkSession.builder.appName('test').getOrCreate()

    def __get_test_pair(self, instance_type):
        test = [data for data in self.test_data["instances"]
                if data["type"] == instance_type][0]
        with open(os.path.join(DATA_SET_PATH,
                               f'vector/expected_{instance_type}.json'),
                  "r") as f:
            target = json.load(f)
        return test, target

    def __assert_equal(self, instance_type):
        test, target = self.__get_test_pair(instance_type)
        self.assertEqual(process_vector_object(test), target)

    def test_bounding_box(self):
        self.__assert_equal("bbox")

    def test_polygon(self):
        self.__assert_equal("polygon")

    def test_point(self):
        self.__assert_equal("point")

    def test_rotated_bbox(self):
        self.__assert_equal("rbbox")

    def test_ellipse(self):
        self.__assert_equal("ellipse")

    def test_polyline(self):
        self.__assert_equal("polyline")

    def test_cuboid(self):
        self.__assert_equal("cuboid")

    def test_tag(self):
        test, target = self.__get_test_pair("tag")
        self.assertEqual(process_vector_tag(test), target)


class TestVectorBoundingBoxes(unittest.TestCase):

    def test_bounding_box(self):
        bbox = {"points": {
            "x1": 2.27,
            "x2": 12.99,
            "y1": 1.1,
            "y2": 22
        },
            "classId": 10228}

        result = [2, 1, 13, 22, 10228]

        self.assertEqual(process_bounding_box(bbox), result)

    def test_get_boxes(self):
        instances = [{"type": "bbox",
                      "points": {
                          "x1": 2.27,
                          "x2": 12.99,
                          "y1": 1.1,
                          "y2": 22
                      },
                      "classId": 10228},
                     {"type": "bbox", "points": {
                         "x1": 3.19,
                         "x2": 4.23,
                         "y1": 2.1,
                         "y2": 18.9
                     },
            "classId": 10229}]
        target = [2, 1, 13, 22, 10228, 3, 2, 4, 19, 10229]
        self.assertEqual(get_boxes(instances), target)


class TestVectorDataFrame(unittest.TestCase):
    def test_vector_dataframe(self):
        spark = SparkSession.builder.master("local").getOrCreate()
        with open(os.path.join(DATA_SET_PATH,
                               "vector/example_annotation.json"), "r") as f:
            data = json.load(f)

        actual_df = get_vector_dataframe([data], spark)

        expected_df = spark.read.parquet(os.path.join(
            DATA_SET_PATH, "vector/expected_df.parquet"))
        self.assertEqual(sorted(actual_df.collect()),
                         sorted(expected_df.collect()))


if __name__ == '__main__':
    unittest.main()
