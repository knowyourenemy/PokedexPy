# PokedexPy
This is a Python program that allows users to retrieve information about Pokemons. It uses [This Pokemon API](https://pokeapi.co/).

## How to use
Ensure you have pip and python installed. 
```
pip install requests
python pokemon.py
```

## API Calls
This program is designed around minimising the number of API calls. The second API call is only made if the user actually needs more information. At the same time, previous search results are stored in a dictionary, so that the API does not have to be called again for a previously searched Pokemon.

## Future plans
1. Modify code to allow type-checking
2. Allow user to retrieve more information
3. Include tests

## Production
For production, I would not create a Python script but rather a React app. This app would allow users to search up a Pokemon, and choose what they would like to know about that Pokemon. The results will be displayed in a styled webpage with a clean UI, and will include images wherever possible. If time permits, a comparison feature that allows users to compare two Pokemons could also be implemented. Such an application could be useful for Pokemon fans, as the [wiki page](https://pokemon.fandom.com/wiki/Charizard) can be rather cluttered.
