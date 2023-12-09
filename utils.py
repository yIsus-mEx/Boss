import yaml
dict_canales = {}
dict_nombres ={}

preferences = open("toys/preferences.yml")
dict_preferences = yaml.safe_load(preferences)
preferences.close()

dict_nombres = dict_preferences['nombres']
dict_canales = dict_preferences['canales']

def correct_channel_name(channel_name):
    for key in dict_nombres:
        if dict_nombres[key]['name'] in channel_name:
            channel_name = channel_name.replace(dict_nombres[key]['name'], dict_nombres[key]['replace'])
            return channel_name.strip()

    return channel_name.strip()
