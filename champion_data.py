import requests

def get_id_to_name_dict():


    url = 'http://ddragon.leagueoflegends.com/cdn/9.24.2/data/en_US/champion.json'

    r = requests.get(url)

    data = r.json()
    champ_list = data['data']
    champ_dict = {}
    champions = []

    for champion in champ_list:
        champions.append(champion)

    for c in champions:
        c_dict = champ_list.get(c)
        c_id = c_dict.get('key')
        champ_dict[int(c_id)] = c
    
    return champ_dict