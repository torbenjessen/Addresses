#Created By Torben Jessen Januar 2022 www.tpw.dk
#Adresse via postnummer
import os
import sys
from urllib.request import urlopen
import json
from json import dumps
import uuid
guid = uuid.uuid1()

while True:
    zipcode = input("Indtast postnummer:")
    x = zipcode.isnumeric()
    if x !=True or len(str(zipcode)) != 4:
        print("Den fortod jeg ikke - indtast 4 tal f.eks 1441.")
        continue
    else:
        #zipcode was successfully parsed!
        break

url = "https://api.dataforsyningen.dk/adresser?postnr="+zipcode+"&format=json"

# store the response of URL
try:
  response=urlopen(url)
except:
  print("En undtagelse opstod ved åbning af",url)
  exit()

data_json = json.loads(response.read())
thisdict = data_json
json_string = dumps(thisdict, sort_keys=False, indent=2, ensure_ascii=False)
res = json.loads(json_string)

def makeurl(coordinates):
  url = "http://maps.google.com/maps?q="
  position = coordinates.split(',', 1)[1]+","+coordinates.split(',', 1)[0]
  position = position.replace('[', '').replace(']', '')
  url = url + position  
  return url

a = open(zipcode+".csv", "w")
a.write("Vejnavn;Husnr;Etage;Postnummer;By;Id;Koordinater"+"\n")
i = 0
while i < len(res):
  address = res[i]
  a.write(address['adgangsadresse']['vejstykke']['navn']+
  ";"+address['adgangsadresse']['husnr']+
  ";"+str(address['etage'])+
  ";"+address['adgangsadresse']['postnummer']['nr']+
  ";"+address['adgangsadresse']['postnummer']['navn']+
  ";"+address['id']+
  ";"+makeurl(str(address['adgangsadresse']['adgangspunkt']['koordinater']))+"\n")
  i = i + 1

a.close()
l = len(res)

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

print(l," adresser hentet fra:\n",url,"\nog skrevet til "+application_path+"\\"+zipcode+".csv\nTryk enter for at afslutte...")
input()