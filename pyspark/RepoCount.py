import sys, json
from random import random
from operator import add

from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext


if __name__ == "__main__":
    sc = SparkContext(conf=SparkConf())
    jsonDirPath = sc.getConf().get("spark.cs.jsonDirPath")
    outputDir = sc.getConf().get("spark.cs.outputDir")

    RDD = sc.textFile(jsonDirPath)
    print(RDD.filter(lambda l: json.loads(l)['type'] == 'PushEvent').map(lambda l: json.loads(l)['repo']['name']).count())
    #RDD.saveAsTextFile(outputDir)
