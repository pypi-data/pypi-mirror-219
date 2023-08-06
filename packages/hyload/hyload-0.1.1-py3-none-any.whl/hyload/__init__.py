from gevent import monkey,spawn,sleep
monkey.patch_all()
from hyload.stats import Stats
from hyload.logger import TestLogger
from hyload.httpclient import HttpsClient,HttpClient
