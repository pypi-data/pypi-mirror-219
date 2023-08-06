from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    MapType,
    ArrayType,
    TimestampType
)


def get_text_entity_schema():
    return StructType([
        StructField("id", StringType(), False),
        StructField("start", IntegerType(), False),
        StructField("end", IntegerType(), False),
        StructField("classId", IntegerType(), False),
        StructField("attributes", ArrayType(MapType(StringType(),
                                                    StringType()))),
        StructField("type", StringType(), False),
        StructField("creationType", StringType(), True),
        StructField("createdAt", TimestampType(), True),
        StructField("createdBy", MapType(StringType(), StringType()), True),
        StructField("updatedAt", TimestampType(), True),
        StructField("updatedBy", MapType(StringType(), StringType()), True),
        StructField("className", StringType(), False)
    ])


def get_text_tag_schema():
    return StructType([
        StructField("type", StringType(), True),
        StructField("className", StringType(), True),
        StructField("attributes", ArrayType(MapType(StringType(),
                                                    StringType())),
                    True)

    ])


def get_text_schema():
    schema = StructType([
        StructField("name", StringType(), True),
        StructField("url", StringType(), True),
        StructField("projectId", IntegerType(), True),
        StructField("status", StringType(), True),
        StructField("annotatorEmail", StringType(), True),
        StructField("qaEmail", StringType(), True),
        StructField("entities", ArrayType(get_text_entity_schema()),
                    True),
        StructField("tags", ArrayType(get_text_tag_schema()),
                    True)
    ])
    return schema
