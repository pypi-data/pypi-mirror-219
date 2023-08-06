from pyspark.sql.types import (
    StructType,
    StructField,
    FloatType,
    ArrayType
)


def get_bbox_schema():
    """
    Defines the schema of a bounding box

    Args:
        None

    Returns:
        StructType: Schema of a bbox
    """
    return StructType([
        StructField("x1", FloatType(), True),
        StructField("y1", FloatType(), True),
        StructField("x2", FloatType(), True),
        StructField("y2", FloatType(), True)
    ])


def get_rbbox_schema():
    """
    Defines the schema of a rotated bounding box
    this contains one point for each corned

    Args:
        None

    Returns:
        StructType: Schema of a bbox
    """
    return StructType([
        StructField("x1", FloatType(), True),
        StructField("y1", FloatType(), True),
        StructField("x2", FloatType(), True),
        StructField("y2", FloatType(), True),
        StructField("x3", FloatType(), True),
        StructField("y3", FloatType(), True),
        StructField("x4", FloatType(), True),
        StructField("y4", FloatType(), True)
    ])


def get_point_schema():
    """
    Defines the schema of a point

    Args:
        None

    Returns:
        StructType: Schema of a point
    """
    return StructType([
        StructField("x", FloatType(), True),
        StructField("y", FloatType(), True)
    ])


def get_cuboid_schema():
    """
    Defines the schema of a cuboid (3d bounding box)

    Args:
        None

    Returns:
        StructType: Schema of a cuboid
    """
    return StructType([
        StructField("f1", get_point_schema(), True),
        StructField("f2", get_point_schema(), True),
        StructField("r1", get_point_schema(), True),
        StructField("r2", get_point_schema(), True)
    ])


def get_ellipse_schema():
    """
    Defines the schema of an ellipse

    Args:
        None

    Returns:
        StructType: Schema of an ellipse
    """
    return StructType([
        StructField("cx", FloatType(), True),
        StructField("cy", FloatType(), True),
        StructField("rx", FloatType(), True),
        StructField("ry", FloatType(), True),
        StructField("angle", FloatType(), True)
    ])


def get_polygon_schema():
    """
    Defines the schema of a polygon. It contains a shell as well
    as excluded points

    Args: 
        None

    Returns:
        StructType: Schema of a polygon with holes
    """
    return StructType([
        StructField("points", ArrayType(FloatType()), True),
        StructField("exclude", ArrayType(ArrayType(FloatType())), True)
    ])


def get_polyline_schema():
    """
    Defines the schema of a polyline
    A simple array of float

    Args:
        None

    Returns:
        ArrayType: Schema of a polygon with holes
    """
    return ArrayType(FloatType())
