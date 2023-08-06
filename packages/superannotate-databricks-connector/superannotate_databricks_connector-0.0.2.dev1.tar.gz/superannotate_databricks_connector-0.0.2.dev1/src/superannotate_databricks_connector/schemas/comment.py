from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    FloatType,
    BooleanType,
    MapType,
    ArrayType,
    IntegerType
)

from .shapes import get_bbox_schema


def get_vector_comment_schema():
    return StructType([
        StructField("correspondence",
                    ArrayType(MapType(
                        StringType(),
                        StringType())),
                    True),
        StructField("x", FloatType(), True),
        StructField("y", FloatType(), True),
        StructField("resolved", BooleanType(), True),
        StructField("createdAt", StringType(), True),
        StructField("createdBy", MapType(
            StringType(),
            StringType()),
            True),
        StructField("creationType", StringType(), True),
        StructField("updatedAt", StringType(), True),
        StructField("updatedBy", MapType(
            StringType(),
            StringType()),
            True)
    ])


def get_video_timestamp_schema():
    return StructType([
        StructField("timestamp", IntegerType(), True),
        StructField("points", get_bbox_schema(), True)
    ])


def get_video_comment_parameter_schema():
    return StructType([
        StructField("start", IntegerType(), True),
        StructField("end", IntegerType, True),
        StructField("timestamps", ArrayType(
            get_video_timestamp_schema()), True)
    ])


def get_video_comment_schema():
    return StructType([
        StructField("correspondence",
                    ArrayType(MapType(
                        StringType(),
                        StringType())),
                    True),
        StructField("start", IntegerType(), True),
        StructField("end", IntegerType(), True),
        StructField("createdAt", StringType(), True),
        StructField("createdBy", MapType(
            StringType(),
            StringType()),
            True),
        StructField("creationType", StringType(), True),
        StructField("updatedAt", StringType(), True),
        StructField("updatedBy", MapType(
            StringType(),
            StringType()),
            True),
        StructField("parameters",
                    ArrayType(get_video_comment_parameter_schema()), True)

    ])
