import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
import re
from pyspark.sql import functions as SqlFuncs

def sparkAggregate(glueContext, parentFrame, groups, aggs, transformation_ctx) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs) if len(groups) > 0 else parentFrame.toDF().agg(*aggsFuncs)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1749657292056 = glueContext.create_dynamic_frame.from_catalog(database="project_db", table_name="rawinput", transformation_ctx="AmazonS3_node1749657292056")

# Script generated for node Filter
Filter_node1749657489325 = Filter.apply(frame=AmazonS3_node1749657292056, f=lambda row: (row["price"] > 0), transformation_ctx="Filter_node1749657489325")

# Script generated for node Aggregate
Aggregate_node1749657678000 = sparkAggregate(glueContext, parentFrame = Filter_node1749657489325, groups = [], aggs = [["price", "avg"]], transformation_ctx = "Aggregate_node1749657678000")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=Filter_node1749657489325, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1749657285797", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1749657788503 = glueContext.write_dynamic_frame.from_options(frame=Filter_node1749657489325, connection_type="s3", format="glueparquet", connection_options={"path": "s3://glueprojects3/Output/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1749657788503")

job.commit()