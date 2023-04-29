import json
import random
import pandas as pd
import matplotlib.pyplot as plt 

class Pokemon:
    #Works
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.hp = data['base']['HP']
        self.attack = data['base']['Attack']
        self.defense = data['base']['Defense']
        self.sp_attack = data['base']['Sp. Attack']
        self.sp_defense = data['base']['Sp. Defense']
        self.speed = data['base']['Speed']

class Pokedex:
    #Works
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            pokemon_data = json.load(f)
        self.pokemon = [Pokemon(data) for data in pokemon_data]
        
    #Works
    def search_by_name(self, name):
        for pkmn in self.pokemon:
            if pkmn.name['english'].lower() == name.lower():
                return pkmn
        return None
    
    #Works
    def search_by_type(self, p_type, limit):
        matching_pokemon = []
        for pkmn in self.pokemon:
            if p_type.lower() in [t.lower() for t in pkmn.type]:
                matching_pokemon.append(pkmn)
        random.shuffle(matching_pokemon)
        return random.sample(matching_pokemon, min(limit, len(matching_pokemon)))
    #Works
    def compare_pokemon(self, pokemon1, pokemon2):
        print(f"Comparing {pokemon1.name['english']} and {pokemon2.name['english']}...\n")
        stats_to_compare = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        for stat in stats_to_compare:
            if getattr(pokemon1, stat) > getattr(pokemon2, stat):
                print(f"{pokemon1.name['english']} has higher {stat}: {getattr(pokemon1, stat)} vs {getattr(pokemon2, stat)}")
            elif getattr(pokemon1, stat) < getattr(pokemon2, stat):
                print(f"{pokemon2.name['english']} has higher {stat}: {getattr(pokemon2, stat)} vs {getattr(pokemon1, stat)}")
            else:
                print(f"{pokemon1.name['english']} and {pokemon2.name['english']} have the same {stat}: {getattr(pokemon1, stat)}")
    #Works
    def pokemon_visualize(self, name):
        pokedex_df = pd.read_csv("pokedex.csv")
        pokemon = pokedex.search_by_name(name)
        if not pokemon:
            print('Pokemon not found.')
            return
        pokemon_df = pokedex_df.loc[pokedex_df["name/english"] == name]
        cols = ["base/HP", "base/Attack", "base/Defense", "base/Sp. Attack", "base/Sp. Defense", "base/Speed"]
        attribute_values = pokemon_df[cols].values[0].tolist()
        figure, ax = plt.subplots(figsize=(8, 6))
        ax.bar(cols, attribute_values)
        ax.set_xlabel("Attribute")
        ax.set_ylabel("Value")
        ax.set_title(pokemon.name["english"])
        for i, v in enumerate(attribute_values):
            ax.text(i, v+1, str(v), ha='center', fontsize=10)
        plt.show()

if __name__ == "__main__":
    # Create a Pokedex object
    pokedex = Pokedex('pokedex.json')

    # Get all Pokemon types
    all_types = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']

    # Prompt the user to search for a Pokemon by name, type, or compare two Pokemon
    while True:
        search_type = input('Search by name, type, compare, or visualize (enter "exit" to quit): ')
        if search_type.lower() == 'exit':
            break
        elif search_type.lower() == 'name':
            # Search by name code
            search_name = input('Enter a name: ')
            pokemon = pokedex.search_by_name(search_name)
            if pokemon:
                print(f'ID: {pokemon.id}')
                print(f'Name: {pokemon.name["english"]}')
                print(f'Type: {", ".join(pokemon.type)}')
                print(f'HP: {pokemon.hp}')
                print(f'Attack: {pokemon.attack}')
                print(f'Defense: {pokemon.defense}')
                print(f'Special Attack: {pokemon.sp_attack}')
                print(f'Special Defense: {pokemon.sp_defense}')
                print(f'Speed: {pokemon.speed}')
            else:
                print('Pokemon not found.')
        elif search_type.lower() == 'type':
            # Search by type code
            search_type = input('Enter a type: ')
            limit = int(input('Enter the maximum number of Pokemon to return: '))
            pokemon_list = pokedex.search_by_type(search_type, limit)
            for pokemon in pokemon_list:
                print(f'ID: {pokemon.id}')
                print(f'Name: {pokemon.name["english"]}')
                print(f'Type: {", ".join(pokemon.type)}')
        elif search_type.lower() == 'compare':
            # Compare two Pokemon code
            search_name1 = input('Enter name of first Pokemon: ')
            pokemon1 = pokedex.search_by_name(search_name1)
            if not pokemon1:
                print('Pokemon not found.')
                continue
            search_name2 = input('Enter name of second Pokemon: ')
            pokemon2 = pokedex.search_by_name(search_name2)
            if not pokemon2:
                print('Pokemon not found.')
                continue
            pokedex.compare_pokemon(pokemon1, pokemon2)     
        elif search_type.lower() == 'visualize':
            # Visualize a Pokemon's attributes code
            search_name = input('Enter name of Pokemon to visualize: ')
            pokedex.pokemon_visualize(search_name)    
        else:
            print('Invalid search type.')
        