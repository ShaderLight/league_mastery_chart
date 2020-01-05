import requests
import json
import pygal

api_file = "api_key.json"
with open(api_file) as f:
    data = json.load(f)

api_token = data["api"]
summ_name = input("Name: ")
url = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summ_name

r = requests.get(url, headers={"X-Riot-Token": api_token})

if r.status_code != 200:
    print ("Error with status code: " + str(r.status_code))
    exit()

print("Status code: " + str(r.status_code))

summ_info = r.json()

summ_name = summ_info['name']
summ_id = summ_info['id']

url = 'https://eun1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + str(summ_id)
r = requests.get(url, headers={"X-Riot-Token": api_token})

if r.status_code != 200:
    print ("Error with status code: " + str(r.status_code))
    exit()

print("Status code: " + str(r.status_code))

masteries = r.json()

x_champs, y_points = [],[]
for champ in masteries:
    x_champs.append(champ['championId'])
    y_points.append(champ['championPoints'])

#print(x_champs)
#print(y_points)

url = 'http://ddragon.leagueoflegends.com/cdn/9.24.2/data/en_US/champion.json'

r = requests.get(url)
bigdata = r.json()

champ_list = bigdata['data']
champ_dict = {}
champs = []

for c in champ_list:
    champs.append(c)

for c in champs:
    c_dict = champ_list.get(c)
    c_id = c_dict.get('key')
    champ_dict[int(c_id)] = c
    
for i in range(len(x_champs)):
    aidi = x_champs[i-1]
    c = champ_dict.get(aidi)
    x_champs[i-1] = c

chart = pygal.Bar()
chart.force_uri_protocol = 'http'
chart.title = 'Masteries for: ' + str(summ_name)
chart.x_labels = x_champs
chart.add('',y_points)

chart.render_to_file('leg_mast.svg')
