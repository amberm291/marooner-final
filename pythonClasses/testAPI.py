import urllib
import urllib2
import base64
import sys
import json

url = 'http://10.0.2.90:8000/imageUpload'
with open(sys.argv[1]) as infile:
	img = base64.b64encode(infile.read())


values = {'userImString' : img,
          'topX' : 10,
          'topY' : 10,
          'bottomX' : 700,
          'bottomY' : 700}

#data = json.dumps(values)
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()