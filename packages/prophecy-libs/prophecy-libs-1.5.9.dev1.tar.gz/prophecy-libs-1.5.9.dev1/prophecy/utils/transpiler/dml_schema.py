# This contains wrappers over dml_schema implemented in scala

from prophecy.utils.transpiler.abi_base import ScalaUtil

def parse(schema, keepConditions=False, keepIncludes=False, keepFunctionColumns=False):
    spark = ScalaUtil.getAbiLib().spark
    jvm = spark.sparkContext._jvm
    return jvm.io.prophecy.abinitio.dml.DMLSchema.parse(schema, keepConditions, keepIncludes, keepFunctionColumns)

