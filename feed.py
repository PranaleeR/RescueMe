import feedparser as fp
import moment
import json
import requests
d = fp.parse('https://control.textlocal.in/feeds/inbox/?id=691202&inbox=10&hash=de6b03cce5c8f8e30dbfedc224a80d5faba6a658ffd507640ea8ffd5e6625b68')
spaceUrl = 'https://xyz.api.here.com/hub/spaces/NBLaa1gZ/features?access_token=1XQiD54VN0pmWWuccdLi_w'

for entry in d['entries']:
	msg = entry['summary_detail']['value']
	date = entry['published']
	
	if(msg.find(';q=')!= -1):
		longLat = msg.split(';q=')[1].split(',')
		latitude = float(longLat[0].replace('(',''))
		longitude = float(longLat[1].replace(')',''))
		number = 'title_detail'
		
		m = moment.date(date, '%Y-%m-%dT%H:%M:%SZ').timezone("Asia/Kolkata")
		dateArray = m.format('DDMMM HH mm').split(' ')
		#line = latitude+","+longitude+","+dateArray[0]+","+dateArray[1]
		
		
		properties={}
		properties['time']=m.format('DD/MM/YY HH:mm');
		properties['user.anon']= entry['title_detail']['value'];
		properties['disaster.event']= 'Landslide';

		tagsMap = {}
		tagsMap['tags'] = [properties['user.anon'],'user.anon@'+properties['user.anon'],dateArray[0]+dateArray[1]+':00']

		properties["@ns:com:here:xyz"] = tagsMap

		geometry={}

		geometry['type']='Point'
		coordinates = [longitude,latitude]
		geometry['coordinates'] = coordinates;
		
		feature={}
		feature['type']='Feature'
		feature['properties']=properties;
		feature['geometry']=geometry;

		y = json.dumps(feature)
		print y
		r = requests.put(spaceUrl,data=y, headers={"content-type":"application/geo+json"})
		print(r.status_code, r.reason)

	
	
