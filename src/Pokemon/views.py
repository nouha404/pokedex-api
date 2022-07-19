from pprint import pprint

from django.shortcuts import render
import requests
from pathlib import Path

ROOT = Path(__file__).parent
Pokemon_images = ROOT / 'templates/images.txt'
Pokemon_names = ROOT / 'templates/name.txt'

if not Path.exists(Pokemon_images) and Path.exists(Pokemon_names):
    Pokemon_images.touch()
    Pokemon_names.touch()


def myPokemon(request):
    # Pour eviter de trop excecuter la requete
    compteur = False
    context = {}
    if compteur:
        # recuperer les 149 pokemons
        for pokemon_id in range(1, 150):
            print(f'image n° {pokemon_id}')
            r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
            response = r.json().get('sprites').get('front_shiny')
            poke_name = r.json().get('forms')[0].get('name')
            # Sauvegarder les donner dans un fichier pour ne pas executer la requete a chaque fois
            with open(Pokemon_images, 'a') as f:
                f.write(f'{response}\n')
            with open(Pokemon_names, 'a') as f:
                f.write(f'{poke_name}\n')
    # Ouvrir les fichier pour envoyer des contexts dans la page index.html
    with open(Pokemon_images, 'r') as f:
        images = [image for image in f]
        context['images'] = images

    with open(Pokemon_names, 'r') as f:
        names = [name for name in f]
        context['names'] = names

    # Partie recherche pour les relier avec le noms des pokemons

    return render(request, 'index.html', {'items': context['images'], 'items2': context['names']})
