import requests

POKEMON_URL = "https://pokeapi.co/api/v2/pokemon/"

# Initialise dictionaries that will store current search results with default values
pokemon_dict = {"name": "unknown", "height": "unknown",
                "types": [], "species": "unknown"}
pokemon_species_dict = {"name": "unknown", "description": "unknown",
                        "legendary": "unknown", "habitat": "unknown"}

# Initialise dictionaries that will store past search results
pokemon_past_searches = {}
pokemon_species_past_searches = {}

# Calls API and populates pokemon_dict
def get_pokemon(pokemon_name):

    # Ensure that this function modifies global variables
    global pokemon_dict, pokemon_past_searches

    # If current search item has already been searched before, retrieve data from pokemon_past_searches
    if pokemon_name in pokemon_past_searches:
        pokemon_dict = pokemon_past_searches[pokemon_name]
        return

    # Call API
    try:
        data = requests.get(POKEMON_URL + pokemon_name, timeout=5)
        data.raise_for_status()

    # Catch different exceptions, which indicate different issues
    except requests.exceptions.HTTPError as errh:
        print("\nSorry, we were unable to find that Pokemon")
        print("Please ensure you spelled it correctly")
        return 0
    except requests.exceptions.ConnectionError as errc:
        print("\nSorry, we are having issues connecting")
        return 0
    except requests.exceptions.Timeout as errt:
        print("\nSorry, your request took too long")
        return 0
    except requests.exceptions.RequestException as err:
        print("\nSorry, something went wrong")
        return 0

    # Convert API JSON data to a dictionary
    data_json = data.json()

    # Populate pokemon_dict, while ensuring each property exists
    if "name" in data_json:
        pokemon_dict["name"] = data_json["name"]

    if "height" in data_json:
        pokemon_dict["height"] = data_json["height"]

    if "types" in data_json:
        types_data = data_json["types"]
        types_list = list(
            map(lambda typeObj: typeObj["type"]["name"], types_data))
        types = ", ".join(types_list)
        pokemon_dict["types"] = types

    if "species" in data_json:
        pokemon_dict["species"] = data_json["species"]["url"]

    # Add a copy of this search result to pokemon_past_searches
    pokemon_past_searches[pokemon_name] = pokemon_dict.copy()

# Calls API and populates pokemon_species_dict
def get_pokemon_species(pokemon_species_url):

    # Ensure that this function modifies global variables
    global pokemon_species_dict, pokemon_species_past_searches

    # If current search item has already been searched before, retrieve data from pokemon_past_searches
    if pokemon_species_url in pokemon_species_past_searches:
        pokemon_species_dict = pokemon_species_past_searches[pokemon_species_url]
        return

    # Call API
    try:
        data = requests.get(pokemon_species_url, timeout=5)
        data.raise_for_status()

    # Catch different exceptions, which indicate different issues
    except requests.exceptions.HTTPError as errh:
        print("\nSorry, we were unable to find more information.")
        return 0
    except requests.exceptions.ConnectionError as errc:
        print("\nSorry, we are having issues connecting")
        return 0
    except requests.exceptions.Timeout as errt:
        print("\nSorry, your request took too long")
        return 0
    except requests.exceptions.RequestException as err:
        print("\nSorry, something went wrong")
        return 0

    # Convert API JSON data to a dictionary
    data_json = data.json()

    # Populate pokemon_species_dict, while ensuring each property exists
    if "habitat" in data_json:
        pokemon_species_dict["habitat"] = data_json["habitat"]["name"]

    if "is_legendary" in data_json:
        if data_json["is_legendary"]:
            pokemon_species_dict["legendary"] = "yes"
        else:
            pokemon_species_dict["legendary"] = "no"

    if "name" in data_json:
        pokemon_species_dict["name"] = data_json["name"]

    if "flavor_text_entries" in data_json:
        text_entries = data_json["flavor_text_entries"]
        descriptions = list(
            filter(lambda desc: desc["language"]["name"] == "en", text_entries))
        description = descriptions[0]["flavor_text"].replace(
            "\n", " ").replace("\f", " ")
        pokemon_species_dict["description"] = description

    # Add a copy of this search result to pokemon_species_past_searches
    pokemon_species_past_searches[pokemon_species_url] = pokemon_species_dict.copy(
    )

# This function is called whenever the user wants to search for a new pokemon
def user_wants_pokemon():

    # Prompt user
    print("\nWhich Pokemon would you like to search for?\n")
    search_pokemon = input("Enter pokemon: ").lower()

    # Terminate program if user wishes to quit
    if search_pokemon == "quit":
        quit()

    # Call API, terminate function if error is raised
    call_api = get_pokemon(search_pokemon)
    if call_api == 0:
        return

    # Print info
    print("\n==================================")
    print("\nPokemon Name: ", pokemon_dict["name"])
    print("Height: ", pokemon_dict["height"])
    print("Types: ", pokemon_dict["types"])
    print("\n==================================")

    # Prompt user
    print("\nDo you want more information?")
    print("\nType \"yes\" or \"no\"\n")
    more_info = input().lower()

    # Terminate program if user wants to quit
    if more_info == "quit":
        quit()

    # User wants more information
    if more_info == "yes":

        # Call API, terminate if an error is raised
        call_api = get_pokemon_species(pokemon_dict["species"])
        if call_api == 0:
            return

        # Print details
        print("\n==================================")
        print("\nSpecies Name: ", pokemon_species_dict["name"])
        print("Habitat: ", pokemon_species_dict["habitat"])
        print("Legendary: ", pokemon_species_dict["legendary"])
        print("Description: ", pokemon_species_dict["description"])
        print("\n==================================")

    # User does not want more information
    else:
        return


# Welcome message
print("\nWelcome!\n")
print("`;-.          ___,")
print("  `.`\_...._/`.-\"`")
print("    \        /      ,")
print("    /()   () \    .' `-._")
print("   |)  .    ()\  /   _.'")
print("   \  -'-     ,; '. <")
print("    ;.__     ,;|   > \\")
print("   / ,    / ,  |.-'.-'")
print("  (_/    (_/ ,;|.<`")
print("    \    ,     ;-`")
print("    \    ,     ;-`")
print("    (_,-'`> .'")
print("jgs      (_,'")

# Prompt user for first search
user_wants_pokemon()

# Main loop
running = True
while running:

    # Prompt user
    print("\nWhat would you like to do next?\n")
    print("type \"another\" to search for another pokemon")
    print("type \"quit\" to exit\n")
    next = input().lower()

    # Search for another pokemon
    if next == "another":
        user_wants_pokemon()

    # Quit program
    if next == "quit":
        running = False
