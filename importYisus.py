import requests
import json

def importYisus():

    try:
        response = requests.get('https://pastebin.com/raw/36jGppfm')
        response.raise_for_status()
        yisus_dict = response.json()
        print('importYisus: OK: yisus se ha importado')
        return yisus_dict

    except requests.exceptions.RequestException as e:
        print("importYisus : ERROR :", e)
        return None


if __name__ == "__main__":
    importYisus()
