"""
Library for interacting with the PokeAPI.
https://pokeapi.co/
"""

import requests
import os

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def get_pokemon_list():
    """
    Gets a list of all Pokemon names from the PokeAPI.

    Returns:
        list: A list of Pokemon names, if successful. Otherwise None.
    """
    url = POKE_API_URL + '?limit=1000'  # Adjust limit as necessary
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        pokemon_data = resp_msg.json()
        pokemon_names = [pokemon['name'].capitalize() for pokemon in pokemon_data['results']]
        return pokemon_names
    else:
        print(f'Failed to retrieve Pokemon list: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def get_pokemon_info(pokemon):
    """
    Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    pokemon = str(pokemon).strip().lower()

    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return None

    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def download_pokemon_image(pokemon_name, save_dir):
    """
    Downloads the official artwork for a specified Pokemon and saves it to a specified directory.

    Args:
        pokemon_name (str): Name of the Pokemon to download.
        save_dir (str): Directory where the image should be saved.

    Returns:
        str: File path of the saved image, or None if the download failed.
    """
    poke_info = get_pokemon_info(pokemon_name)

    if poke_info is None:
        print(f'Error: Could not find information for {pokemon_name}.')
        return None

    image_url = poke_info['sprites']['other']['official-artwork']['front_default']

    if not image_url:
        print(f'Error: No official artwork found for {pokemon_name}.')
        return None

    print(f'Downloading artwork for {pokemon_name.capitalize()}...', end='')
    image_resp = requests.get(image_url)

    if image_resp.status_code == requests.codes.ok:
        print('success')

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        file_path = os.path.join(save_dir, f"{pokemon_name.capitalize()}.png")

        with open(file_path, 'wb') as img_file:
            img_file.write(image_resp.content)
        
        return file_path
    else:
        print('failure')
        print(f'Response code: {image_resp.status_code} ({image_resp.reason})')
        return None

def main():
    # Test out the functions
    poke_info = get_pokemon_info("Rockruff")
    print(poke_info)

    pokemon_list = get_pokemon_list()
    print(pokemon_list[:10])  # Print the first 10 Pokémon names

    image_path = download_pokemon_image("Rockruff", "images")
    print(f'Image saved to: {image_path}')
    return

if __name__ == '__main__':
    main()