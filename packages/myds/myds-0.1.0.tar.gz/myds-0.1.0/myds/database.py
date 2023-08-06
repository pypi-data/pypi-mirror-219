import requests
from urllib.parse import urlencode
def getDb(dbName,port=5149,charset='UTF-8'):
	params = {"dbName": dbName, "charset": charset};
	url = f'http://localhost:{port}/query?'+urlencode(params)
	res = requests.get(url).text
	return res