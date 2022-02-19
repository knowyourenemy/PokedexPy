import requests

POKEMON_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_SPECIES_URL = "https://pokeapi.co/api/v2/species/"

pokemon_dict = {"name": "unknown", "height": "unknown", "types": [], "species": "unknown"}
pokemon_past_searches = {}

pokemon_species_dict = {"name": "unknown", "description": "unknown", "legendary": "unknown", "habitat": "unknown"}
pokemon_species_past_searches = {}



def get_pokemon(pokemon_name):
    global pokemon_dict, pokemon_past_searches

    if pokemon_name in pokemon_past_searches:
        pokemon_dict = pokemon_past_searches[pokemon_name]
        return
    
    try: 
        data = requests.get(POKEMON_URL + pokemon_name, timeout = 5)
        print("just fetched data")
        data.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Sorry, the pokemon does not exist")
        return 0
    except requests.exceptions.ConnectionError as errc:
        print ("Sorry, we are having issues connecting:")
        return 0
    except requests.exceptions.Timeout as errt:
        print ("Sorry, your request took too long")
        return 0
    except requests.exceptions.RequestException as err:
        print ("Sorry, something went wrong")
        return 0

    data_json = data.json()
    


    if data_json["name"]:  
        pokemon_dict["name"] = data_json["name"]
    
    if data_json["height"]:
        pokemon_dict["height"] = data_json["height"]

    if data_json["types"]:
        pokemon_dict["types"] = data_json["types"]

    if data_json["species"]:
        pokemon_dict["species"] = data_json["species"]["url"]

    pokemon_past_searches[pokemon_name] = pokemon_dict.copy()

    
def get_pokemon_species(pokemon_species_url):
    global pokemon_species_dict, pokemon_species_past_searches

    if pokemon_species_url in pokemon_species_past_searches:
        pokemon_species_dict = pokemon_species_past_searches[pokemon_species_url]
        return
    
    try: 
        data = requests.get(pokemon_species_url, timeout = 5)
        print("just fetched data")
        data.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Sorry, the pokemon species does not exist")
        return 0
    except requests.exceptions.ConnectionError as errc:
        print ("Sorry, we are having issues connecting:")
        return 0
    except requests.exceptions.Timeout as errt:
        print ("Sorry, your request took too long")
        return 0
    except requests.exceptions.RequestException as err:
        print ("Sorry, something went wrong")
        return 0

    data_json = data.json()
    


    if data_json["habitat"]:  
        pokemon_species_dict["habitat"] = data_json["habitat"]["name"]
    
    if data_json["is_legendary"] == True:
        pokemon_species_dict["legendary"] = "Yes"
    else:
        pokemon_species_dict["legendary"] = "No"

    pokemon_species_dict["name"] = data_json["name"]
    description = list(filter(lambda descriptionObj: descriptionObj["language"]["name"] == "en", data_json["flavor_text_entries"]))[0]["flavor_text"].replace("\n", " ").replace("\f", " ")
    
    if data_json["description"]:
        pokemon_species_dict["description"] = description


    # if data_json["types"]:
    #     pokemon_species_dict["types"] = data_json["types"]

    pokemon_species_past_searches[pokemon_species_url] = pokemon_species_dict.copy()
    



def user_wants_pokemon():

    print("search a pokemon")
    search_pokemon = input("Enter pokemon:")
    get = get_pokemon(search_pokemon)
    if get == 0:
        return
    print("name: ", pokemon_dict["name"])
    print("height: ", pokemon_dict["height"])
    types = list(map(lambda typeObj: typeObj["type"]["name"], pokemon_dict["types"]))
    print("types: ", ", ".join(types))

    print("do you want more information?")
    more_info = input("y/n")
    if more_info == "y":
        get = get_pokemon_species(pokemon_dict["species"])
        if get == 0:
            return
        print("name: ", pokemon_species_dict["name"])
        print("habitat: ", pokemon_species_dict["habitat"])
        print("legendary: ", pokemon_species_dict["legendary"])
    else:
        return


running = True


user_wants_pokemon()

while running:
    print("What would you like to do next?")
    print("type \"another\" to search for another pokemon")
    print("type \"quit\" to exit")
    next = input()
    if next == "another":
        user_wants_pokemon()
    if next == "quit":
        running = False









