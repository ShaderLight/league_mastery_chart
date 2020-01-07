import requests
import json
import pygal

from champion_data import get_id_to_name_dict

api_file = "api_key.json"
with open(api_file) as f: #importing api key from a seperate json file
    data = json.load(f)

api_token = data["api"]
summ_name = input("Name: ")
url = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summ_name

r = requests.get(url, headers={"X-Riot-Token": api_token}) #getting detailed summoner info in order to request specific info

if r.status_code != 200:
    print ("Error with status code: " + str(r.status_code))
    exit()

print("Status code: " + str(r.status_code))

summ_info = r.json()

summ_name = summ_info['name']
summ_id = summ_info['id'] #important for next step

url = 'https://eun1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + str(summ_id)
r = requests.get(url, headers={"X-Riot-Token": api_token}) #getting summoner's mastery score json

if r.status_code != 200:
    print ("Error with status code: " + str(r.status_code))
    exit()

print("Status code: " + str(r.status_code))

masteries = r.json()

x_champs, y_points = [],[]
for champ in masteries:
    x_champs.append(champ['championId'])
    y_points.append(champ['championPoints'])

champ_dict = get_id_to_name_dict() #getting an up to date dict with (id - champion name) pairs

for i in range(len(x_champs)):
    aidi = x_champs[i-1]
    c = champ_dict.get(aidi)
    x_champs[i-1] = c

#simple pygal chart with x and y axis as champion names and mastery points

chart = pygal.Bar()
chart.force_uri_protocol = 'http'
chart.title = 'Masteries for: ' + str(summ_name)
chart.x_labels = x_champs
chart.add('',y_points)

chart.render_to_file('league_masteries_' + summ_name + '.svg')
