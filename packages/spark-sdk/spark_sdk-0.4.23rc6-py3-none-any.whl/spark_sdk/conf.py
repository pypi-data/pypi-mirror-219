HADOOP_HOST = "hdfs://hdfs-cluster.datalake.bigdata.local"
HADOOP_PORT = 8020
HIVE_IP_NODES1 = "master01-dc9c14u40.bigdata.local:9083"
HIVE_IP_NODES2 = "master02-dc9c14u41.bigdata.local:9083"

GMS_AUTH_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImR1eXZuYyIsInR5cGUiOiJQRVJTT05BTCIsInZlcnNpb24iOiIyIiwianRpIjoiZTdhZWUxM2MtYzI1Yi00MjUzLWE1Y2MtZTkxNWZiMDNiYTBmIiwic3ViIjoiZHV5dm5jIiwiZXhwIjoxNjkwOTQzMDYxLCJpc3MiOiJkYXRhaHViLW1ldGFkYXRhLXNlcnZpY2UifQ.RG6K8bh-oZtEOZ6xXkY-4jxQtMY89F8THvfcL1qVpWk"
GMS_URL_KEY = "http://ccatalog-gms.cads.live"
# GMS_URL_KEY = "http://staging-ccatalog-gms.cads.live"

import os
from urllib.parse import urlparse
domain = urlparse(GMS_URL_KEY).netloc
os.environ['no_proxy'] = domain+","+"git.cads.live,vault.cads.live"