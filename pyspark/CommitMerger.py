import sys, json
from urllib.request import urlopen
from random import random
from operator import add

from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext


if __name__ == "__main__":
    sc = SparkContext(conf=SparkConf())
    jsonDirPath = sc.getConf().get("spark.cs.jsonDirPath")
    outputDir = sc.getConf().get("spark.cs.outputDir")

    RDD = sc.textFile(jsonDirPath)
    RDD = RDD.filter(lambda l: json.loads(l)['type'] == 'PushEvent').flatMap(lambda l: [(json.loads(l)['repo']['name'],commit['message']) for commit in json.loads(l)['payload']['commits']])
    RDD.saveAsTextFile(outputDir)
