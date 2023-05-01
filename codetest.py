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
        """
        Searches for a Pokemon by name.

        Parameters:
            name (str): The name of the Pokemon to search for.

        Returns:
            (Pokemon) The Pokemon object if found, otherwise None.
        """

        return next((pkmn for pkmn in self.pokemon if pkmn.name['english'].lower() == name.lower()), None)

    
    #Works
    def search_by_type(self, type1, type2, limit):
        matching_pokemon = []
        for pkmn in self.pokemon:
            if type1.lower() in [t.lower() for t in pkmn.type] and type2.lower() in [t.lower() for t in pkmn.type]:
                matching_pokemon.append(pkmn)
        random.shuffle(matching_pokemon)
        return random.sample(matching_pokemon, min(limit, len(matching_pokemon)))
    
    #Works
    def search_by_stats(self, stat_name, stat_min, stat_max):
        
        # Find all Pokemon that meet the criteria
        matching_pokemon = []
        for pkmn in self.pokemon:
            stat_value = getattr(pkmn, stat_name.lower())
            if stat_min <= stat_value <= stat_max:
                matching_pokemon.append(pkmn)
        if not matching_pokemon:
            print('No Pokemon found.')
            return None
        # Return a random Pokemon from the list of matching Pokemon
        return random.choice(matching_pokemon)
    
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
        figure, ax = plt.subplots(figsize=(12, 7))
        ax.bar(cols, attribute_values)
        ax.set_xlabel("Attribute")
        ax.set_ylabel("Value")
        ax.set_title(pokemon.name["english"])
        for i, v in enumerate(attribute_values):
            ax.text(i, v+1, str(v), ha='center', fontsize=10)
        plt.show()

    def get_all_types(self):
        all_types = set()
        for pkmn in self.pokemon:
            all_types.update(pkmn.type)
        return sorted(all_types)
            
if __name__ == "__main__":
    # Create a Pokedex object
    pokedex = Pokedex('pokedex.json')

    # Prompt the user to search for a Pokemon by various criteria
    while True:
        print('\nSearch for a Pokemon by:')
        print('  1. Name')
        print('  2. Type')
        print('  3. Stats')
        print('  4. Compare two Pokemon')
        print('  5. Visualize Pokemon attributes')
        print('  6. Exit')
        search_type = input('Enter the number of your selection: ')

        if search_type == '6':
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
            print('Search by type:')
            print('1. Search for a specific type')
            print('2. Search for a Pokemon with multiple types')
            search_type_option = input('Enter your choice: ')
            if search_type_option == '1':
                print('Available types:', ', '.join(pokedex.get_all_types()))
                search_type = input('Enter a type: ')
                limit = int(input('Enter the maximum number of results to show: '))
                matching_pokemon = pokedex.search_by_type(search_type, limit)
                print(f'{len(matching_pokemon)} Pokemon found:')
                for pkmn in matching_pokemon:
                    print(f'{pkmn.name["english"]} ({" / ".join(pkmn.type)})')
            elif search_type_option == '2':
                all_types = pokedex.get_all_types()
                print('Choose two types to search for Pokemon with both types:')
                print('Available types:', ', '.join(all_types))
                type1 = input('Enter the first type: ')
                type2 = input('Enter the second type: ')
                limit = int(input('Enter the maximum number of results to show: '))
                matching_pokemon = pokedex.search_by_type(type1, type2, limit)
                print(f'{len(matching_pokemon)} Pokemon found:')
                for pkmn in matching_pokemon:
                    print(f'{pkmn.name["english"]} ({" / ".join(pkmn.type)})')
            else:
                print('Invalid choice. Please enter 1 or 2.')    
     
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