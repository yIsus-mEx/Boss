import requests
import json

def importYisus():

    try:
        response = requests.get('https://pastebin.com/raw/36jGppfm')
        response.raise_for_status()
        yisus_dict = response.json()
        print('importYisus: INFO: yisus se ha importado')
        with open('yisusBase', 'w', encoding='utf-8') as json_file:
            json.dump(yisus_dict, json_file, indent=2)
        return yisus_dict

    except requests.exceptions.RequestException as e:
        print("importYisus : ERROR :", e)
        return None


if __name__ == "__main__":
    importYisus()