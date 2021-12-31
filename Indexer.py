import sys
from collections import Counter, OrderedDict
import itertools
from itertools import islice, count, groupby
import pandas as pd
import os
import re
from operator import itemgetter
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords
from time import time
from timeit import timeit
from pathlib import Path
import pickle
import pandas as pd
import numpy as np
from google.cloud import storage

import hashlib
def _hash(s):
    return hashlib.blake2b(bytes(s, encoding='utf8'), digest_size=5).hexdigest()

nltk.download('stopwords')

from inverted_index_colab import *

# These will already be installed in the testing environment so disregard the
# amount of time (~1 minute) it takes to install.
# !pip install -q pyspark
# !pip install -U -q PyDrive
# !apt-get update -qq
# !apt install openjdk-8-jdk-headless -qq
# !pip install -q graphframes
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
graphframes_jar = 'https://repos.spark-packages.org/graphframes/graphframes/0.8.2-spark3.2-s_2.12/graphframes-0.8.2-spark3.2-s_2.12.jar'
spark_jars = '/usr/local/lib/python3.7/dist-packages/pyspark/jars'
# !wget -N -P $spark_jars $graphframes_jar