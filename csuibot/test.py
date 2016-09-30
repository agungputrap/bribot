import re
import requests
import shlex

text = "/mregister Toko Cantik-jalan raya sanja citeureup bogor"
text2 = '/zodiac 1994-08-06'
text3 = "/ballance"
pattern = re.search(r'^/mregister .*$', text)
pattern2 = re.search(r'^/zodiac \d{4}\-\d{2}\-\d{2}$', text2)
pattern3 = re.search(r'^/ballance$', text2)
if pattern:
	_, value = text.split('/mregister')
	processed = value[1:len(value)]
	namatokoold, alamatold = processed.split('-')
	namatoko = '_'.join(namatokoold.split(' '))
	alamat = '_'.join(alamatold.split(' '))
	print alamat
	idtel = '1235'
	#print namabaru
	r = requests.get('http://portfolio.hnymnky.com/mregister.php?id_telegram='+idtel+'&nama_toko='+namatoko+'&alamat='+alamat)
	#json = r.json()
	print r.json()
	#if(json['statusId'] == 0 ):
	#	print json
else:
	print "error"