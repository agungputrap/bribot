import re
import requests
import shlex

text = "/mregister Toko Cantik-jalan raya sanja citeureup bogor"
text2 = '/zodiac 1994-08-06'
text3 = "/ballance"
pattern = re.search(r'^/mregister .*$', text)
pattern2 = re.search(r'^/zodiac \d{4}\-\d{2}\-\d{2}$', text2)
pattern3 = re.search(r'^/ballance$', text2)

idtel = str(251572249)
r = requests.get('http://portfolio.hnymnky.com/status.php?id_telegram='+str(idtel))
print r.json()