import utils as u
from importYisus import *
from tools import *
import yaml
import re

d = open("toys/yisus_stations.yaml")
dict_yisus_stations = yaml.safe_load(d)
d.close()


def export_messages():

    elcano = read_cached_elcano()
    cleansed_elcano = cleanse_general(elcano)
    elcano_dict = update_channel_dict(cleansed_elcano)
    transformYisus(elcano_dict)


def read_cached_elcano():
    with open('toys/cachedList.txt', 'r') as cachedlist:
        contenido = cachedlist.read()
        cachedlist.close()
        print("read_cached_elcano: OK: returning elcano cacheado")
        return (contenido)


def cleanse_general(message_content):
    cleansed_content = ""
    rows = [row for row in message_content.split("\n") if len(row.strip()) > 0]
    channel_id_regex = r'[a-zA-Z0-9]{40}'
    
    for i, row in enumerate(rows):
        if re.search(channel_id_regex, row) or row.startswith("http"):
            if i > 0:
              cleansed_content += rows[i-1] + "\n" + row + "\n"
            else:
              cleansed_content += "Canal" + "\n" + row + "\n"

    return cleansed_content

def update_channel_dict(message_content):

    channel_dict = dict()
    rows = message_content.split("\n")
    for i, row in enumerate(rows):
        if i % 2 == 1:
            channel_id = row
            channel_name = rows[i-1]
            channel_name = u.correct_channel_name(channel_name)

            channel_dict[i//2 + 1] = dict()
            channel_dict[i//2 + 1]['ch_name'] = channel_name
            channel_dict[i//2 + 1]['ch_id'] = channel_id
            channel_dict[i // 2 + 1]['control'] = 0

    return channel_dict


def transformYisus(elcano_dict):

    yisus_json = importYisus()
    if yisus_json != None:
        for group in yisus_json['groups']:
            for station in group.get("stations", []):
                station_name = station.get("name")
                if station_name in dict_yisus_stations:
                    corrected_name = dict_yisus_stations[station_name]
                    for canal, valores in elcano_dict.items():
                        if valores.get('control') == 0:
                            if corrected_name == valores.get('ch_name'):
                                valores['control'] = 1
                                ace = valores['ch_id']
                                station["url"] = 'acestream://' + ace
                                info = ace[-4:]
                                station['info'] = info
                                break

        with open('af1.txt', 'w', encoding='utf-8') as json_file:
            json.dump(yisus_json, json_file, indent=4)
            print('transformYisus: OK: yisus se ha exportado correctamente')
            json_file.close()





if __name__ == "__main__":
    scraper()
    export_messages()
