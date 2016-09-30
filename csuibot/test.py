import re
import requests
import shlex

text = "/register hafiyyan kunkun fadhlillah-haha-087877319065"
text2 = '/zodiac 1994-08-06'

pattern = re.search(r'^/register .*$', text)
pattern2 = re.search(r'^/zodiac \d{4}\-\d{2}\-\d{2}$', text2)
if pattern:
	_, value = text.split('/register')
	processed = value[2:len(value)]
	nama, password, nope = processed.partition('-')
	namabaru = '_'.join(nama.split(' '))
	idtel = '1235'
	#print namabaru
	r = requests.get('http://portfolio.hnymnky.com/register.php?username='+namabaru+'&password='+password+'&phone='+nope+'&id_telegram='+idtel)
	json = r.json()
	print r.status_code
	if(json['statusId'] == 0 ):
		print json
else:
	print "error"