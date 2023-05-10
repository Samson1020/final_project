from argparse import ArgumentParser
import json
import random
import csv
import sys
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
        return next((pkmn for pkmn in self.pokemon if pkmn.name['english'].lower() == name.lower()), None)
    
    #Works
    def search_by_type(self, p_type, num_results):
        matching_pokemon = [pkmn for pkmn in self.pokemon if p_type.lower() in [t.lower() for t in pkmn.type]]
        matching_pokemon = random.sample(matching_pokemon, min(num_results, len(matching_pokemon)))
        return matching_pokemon


    
    #Works
    def search_by_stats(self, stat_name, stat_min, stat_max):
        # Find all Pokemon that meet the criteria
        matching_pokemon = [pkmn for pkmn in self.pokemon if stat_min <= getattr(pkmn, stat_name.lower()) <= stat_max]
        
        if not matching_pokemon:
            print("No Pokemon found.")
            return None
        
        # Return the Pokemon with the highest stat value for the specified stat name
        return max(matching_pokemon, key=lambda pkmn: getattr(pkmn, stat_name.lower()))
    
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
    def pokemon_visualize(pokedex, name):
        pokedex_df = pd.read_csv("pokedex.csv")
        pokemon = pokedex.search_by_name(name)
        if not pokemon:
            print('Pokemon not found.')
            return
        pokemon_df = pokedex_df.loc[pokedex_df["name/english"] == name]
        cols = ["base/HP", "base/Attack", "base/Defense", "base/Sp. Attack", "base/Sp. Defense", "base/Speed"]
        attribute_values = pokemon_df[cols].values[0].tolist()
        figure, ax = plt.subplots(figsize=(12, 7))
        ax.bar(cols, attribute_values)
        ax.set_xlabel("Attribute")
        ax.set_ylabel("Value")
        ax.set_title(pokemon.name["english"])
        for i, v in enumerate(attribute_values):
            ax.text(i, v+1, str(v), ha='center', fontsize=10)
        plt.show()
    #works
    def add_pokemon(self, poke_info):
        with open('pokedex.csv', 'a+', encoding="utf-8", newline='') as csvfile:
            csvfile.seek(0)
            read = csv.reader(csvfile)
            write = csv.writer(csvfile)
            last_row = None
            for row in read:
                last_row = row
            if last_row is None:
                id = 1
            else:
                id = int(last_row[0]) + 1
            poke_info[0] = str(id)
            write.writerow(poke_info)

    #Works
    def remove_pokemon(pkm):
        df = pd.read_csv("pokedex.csv")
        df = df[df["name/english"] != pkm]
        df.to_csv("pokemon.csv", index=False)
    #Works    
    def get_pokemon_name(self, name):
        for pokemon in self.pokemon:
            if pokemon.name['english'].lower() == name.lower():
                return {
                    'english': pokemon.name['english'],
                    'japanese': pokemon.name['japanese'],
                    'chinese': pokemon.name['chinese'],
                    'french': pokemon.name['french']
                }
        return None
    
        
def main(filename):
    # Create a Pokedex object
    pokedex = Pokedex(filename)

    # Prompt the user to search for a Pokemon by various criteria
    while True:
        print('\nSearch for a Pokemon by:')
        print('  1. Name')
        print('  2. Type')
        print('  3. Stats')
        print('  4. Compare two Pokemon')
        print('  5. Visualize Pokemon attributes')
        print('  6. Add Pokemon to Pokedex')
        print('  7. Remove Pokemon from Pokedex')
        print('  8. Pokemon name diffrent langauge')
        print('  9. Exit')
        search_type = input('Enter the number of your selection: ')

        if search_type == '9':
            break
        elif search_type == '1':
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
        elif search_type == '2':
            # Search by type code
            search_type = input('Enter a type: ')
            limit = int(input('Enter the maximum number of Pokemon to return: '))
            pokemon_list = pokedex.search_by_type(search_type, limit)
            for pokemon in pokemon_list:
                print(f'ID: {pokemon.id}')
                print(f'Name: {pokemon.name["english"]}')
                print(f'Type: {", ".join(pokemon.type)}')
        elif search_type == '3':
            # Search by stats code
            stat_name = input('Enter a stat name (HP, Attack, Defense, Sp. Attack, Sp. Defense, Speed): ')
            stat_min = int(input('Enter a minimum value: '))
            stat_max = int(input('Enter a maximum value: '))
            pokemon = pokedex.search_by_stats(stat_name, stat_min, stat_max)
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
        elif search_type == '4':
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
        elif search_type == '5':
            # Visualize a Pokemon's attributes code
            search_name = input('Enter name of Pokemon to visualize: ')
            pokedex.pokemon_visualize(search_name)
        elif search_type == '6':
            search_name3 = input('Enter pokemon attributes in a list [] with (id (empty string),name/english, name other language optional (japanese,chinese,french),type/0,type/1,base/HP,base/Attack,base/Defense,base/Sp. Attack,base/Sp. Defense,base/Speed)')
            pokedex.add_pokemon(search_name3)
        elif search_type == '7':
            search_name4 = input('Enter pokemon name for delection')
            pokedex.remove_pokemon(search_name4)
        elif search_type == '8':
            name = input('Enter a Pokemon name in English: ')
            pokemon_data = pokedex.get_pokemon_name(name)
            if pokemon_data is not None:
                print(f"Japanese: {pokemon_data['japanese']}")
                print(f"Chinese: {pokemon_data['chinese']}")
                print(f"French: {pokemon_data['french']}")
            else:
                print(f"{name} not found in the data.")

def parse_args(arglist):
    parser = ArgumentParser()
    parser.add_argument("file", help="file of Pokemon")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)