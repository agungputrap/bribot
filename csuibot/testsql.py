from pysimplesoap.client import SoapClient

client = SoapClient(wsdl='http://hackathon.bri.co.id/BRIHackathon.asmx?WSDL')
response = client.InfoMerchant(kodeMerchant='dodo',password="haha")
print(response['InfoMerchantResult'])