from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    BooleanType,
    MapType,
    ArrayType
)
from .comment import get_vector_comment_schema
from .shapes import (
    get_point_schema,
    get_cuboid_schema,
    get_bbox_schema,
    get_ellipse_schema,
    get_polygon_schema,
    get_polyline_schema,
    get_rbbox_schema
)
from .tag import get_tag_schema


def get_vector_instance_schema():
    return StructType([
        StructField("instance_type", StringType(), True),
        StructField("classId", IntegerType(), True),
        StructField("probability", IntegerType(), True),
        StructField("bbox", get_bbox_schema(), True),
        StructField("rbbox", get_rbbox_schema(), True),
        StructField("polygon", get_polygon_schema()),
        StructField("cuboid", get_cuboid_schema(), True),
        StructField("ellipse", get_ellipse_schema(), True),
        StructField("polyline", get_polyline_schema(), True),
        StructField("point", get_point_schema(), True),
        StructField("groupId", IntegerType(), True),
        StructField("locked", BooleanType(), True),
        StructField("attributes", ArrayType(MapType(StringType(),
                                                    StringType())),
                    True),
        StructField("trackingId", StringType(), True),
        StructField("error", StringType(), True),
        StructField("createdAt", StringType(), True),
        StructField("createdBy", MapType(StringType(), StringType()), True),
        StructField("creationType", StringType(), True),
        StructField("updatedAt", StringType(), True),
        StructField("updatedBy", MapType(StringType(), StringType()), True),
        StructField("className", StringType(), True)
    ])


def get_vector_schema():
    schema = StructType([
        StructField("image_height", IntegerType(), True),
        StructField("image_width", IntegerType(), True),
        StructField("image_name", StringType(), True),
        StructField("projectId", IntegerType(), True),
        StructField("isPredicted", BooleanType(), True),
        StructField("status", StringType(), True),
        StructField("pinned", BooleanType(), True),
        StructField("annotatorEmail", StringType(), True),
        StructField("qaEmail", StringType(), True),
        StructField("instances", ArrayType(get_vector_instance_schema()),
                    True),
        StructField("bounding_boxes", ArrayType(IntegerType()), True),
        StructField("comments", ArrayType(get_vector_comment_schema()), True),
        StructField("tags", ArrayType(get_tag_schema()), True)
    ])
    return schema
