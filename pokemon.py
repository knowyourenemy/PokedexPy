from urllib.error import HTTPError
import requests

POKEMON_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_SPECIES_URL = "https://pokeapi.co/api/v2/species/"

pokemon_dict = {"name": "unknown", "height": "unknown", "types": ["unknown"]}
pokemon_past_searches = set()

pokemon_species_dict = {}
pokemon_species_past_searches = set()



def get_pokemon(pokemon_name):
    if pokemon_name in pokemon_dict:
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
    pokemon_past_searches.add(pokemon_name)


        
    pokemon_dict["name"] = data_json["name"]
    
    if data_json["height"]:
        pokemon_dict["height"] = data_json["height"]

    if data_json["types"]:
        pokemon_dict["types"] = data_json["types"]



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









