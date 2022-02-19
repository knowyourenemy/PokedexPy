from urllib.error import HTTPError
import requests

POKEMON_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_SPECIES_URL = "https://pokeapi.co/api/v2/species/"

pokemon_dict = {"name": "unknown", "height": "unknown", "types": ["unknown"]}
pokemon_past_searches = set()

pokemon_species_dict = {}
pokemon_species_past_searches = set()



def get_pokemon(pokemon_name):
    try: 
        data = requests.get(POKEMON_URL + pokemon_name, timeout = 5)
        data.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

    data_json = data.json()
    pokemon_past_searches.add(pokemon_name)


        
    pokemon_dict["name"] = data_json["name"]
    
    if data_json["height"]:
        pokemon_dict["height"] = data_json["height"]

    if data_json["types"]:
        pokemon_dict["types"] = data_json["types"]

running = True

search_pokemon = input("Enter pokemon:")
get_pokemon(search_pokemon)
print("name: ", pokemon_dict["name"])
print("height: ", pokemon_dict["height"])
print("types: ", pokemon_dict["types"])


while running:
    input = input("next: ")
    if input == "quit":
        running = False









