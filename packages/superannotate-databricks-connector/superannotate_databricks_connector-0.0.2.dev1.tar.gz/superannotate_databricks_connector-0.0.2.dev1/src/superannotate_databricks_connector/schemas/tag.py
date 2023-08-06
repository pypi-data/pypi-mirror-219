from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    MapType,
    ArrayType,
)


def get_tag_schema():
    schema = StructType([
        StructField("instance_type", StringType(), True),
        StructField("classId", IntegerType(), True),
        StructField("probability", IntegerType(), True),
        StructField("attributes", ArrayType(MapType(StringType(),
                                                    StringType())),
                    True),
        StructField("createdAt", StringType(), True),
        StructField("createdBy", MapType(StringType(), StringType()), True),
        StructField("creationType", StringType(), True),
        StructField("updatedAt", StringType(), True),
        StructField("updatedBy", MapType(StringType(), StringType()), True),
        StructField("className", StringType(), True)])
    return schema