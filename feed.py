import feedparser as fp
import moment
import json
import requests
import time
smsMap={}
d = fp.parse('https://control.textlocal.in/feeds/inbox/?id=691202&inbox=10&hash=de6b03cce5c8f8e30dbfedc224a80d5faba6a658ffd507640ea8ffd5e6625b68')
spaceUrl = 'https://xyz.api.here.com/hub/spaces/F8PJrIcl/features?access_token=1XQiD54VN0pmWWuccdLi_w'

while(1):
		
	for entry in d['entries']:
		msg = entry['summary_detail']['value']
		date = entry['published']
		
		latitude = None
		if(msg.find(';q=')!= -1):
			longLat = msg.split(';q=')[1].split(',')
			latitude = float(longLat[0].replace('(',''))
			longitude = float(longLat[1].replace(')',''))
		if(len(msg.split(' '))==3):
			latitude = float(msg.split(' ')[1])
			longitude = float(msg.split(' ')[2])

		if latitude != None:
			number = 'title_detail'
			
			m = moment.date(date, '%Y-%m-%dT%H:%M:%SZ').timezone("Asia/Kolkata")
			dateArray = m.format('DDMMM HH mm').split(' ')	
			
			properties={}
			properties['Date_time']=m.format('DD/MM/YY HH:mm');
			properties['Day_Month']=m.format('DD-MMM');
			properties['Disater_Event']= 'Earthquake in Italy';
			properties['Mobile_Number']= entry['title_detail']['value'];
			properties['Day_Month_hour']=m.format('DD-MMMHH:mm');

			tagsMap = {}
			tagsMap['tags']=['disaster_rescueme_here_xyz_hackethon']
			for key in properties:
				tagsMap['tags'].append(properties[key])
				tagsMap['tags'].append(key.lower()+'@'+properties[key])
			
			properties["@ns:com:here:xyz"] = tagsMap

			geometry={}

			geometry['type']='Point'
			coordinates = [longitude,latitude]
			geometry['coordinates'] = coordinates;
			
			feature={}
			feature['type']='Feature'
			feature['properties']=properties;
			feature['geometry']=geometry;
			mykey = properties['Mobile_Number']+properties['Date_time']
			
			if mykey not in smsMap:
				smsMap[mykey]= mykey
				y = json.dumps(feature)
				print '\n processing : ' + y

				r = requests.put(spaceUrl,data=y, headers={"content-type":"application/geo+json"})
				print(r.status_code, r.reason)
				
			else:
				print '\n Already processed:  ' + msg 
	time.sleep(10)
			




	
	
