from argparse import ArgumentParser
import json
import random
import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt


class Pokemon:
    
    """
    A class to represent a Pokemon object.
    
    Attributes:
        id (int): The unique ID of the Pokemon.
        name (str): The name of the Pokemon.
        type (str): The type of the Pokemon.
        hp (int): The hit points of the Pokemon.
        attack (int): The attack power of the Pokemon.
        defense (int): The defense power of the Pokemon.
        sp_attack (int): The special attack power of the Pokemon.
        sp_defense (int): The special defense power of the Pokemon.
        speed (int): The speed of the Pokemon.
        
    Methods:
        def __init__(self, data):
            Initializes a Pokemon object with the data obtained from the JSON file.
    """
    
    def __init__(self, data):
        
        """
        Initializes a Pokemon object with the data obtained from the JSON file.
        
        Parameters:
            data (dict): A dictionary containing the Pokemon's data.
            
        Returns:
            None
        
        Primary Author:
            Samson Mulugeta
        """
        
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
    
    """
    A class representing a collection of Pokemon.

    Attributes:
        pokemon (list): A list of Pokemon objects.

    Methods:
        __init__(self, file_path):
            Initializes a Pokedex object with the data obtained from the JSON file.

        search_by_name(self, name):
            Searches for a Pokemon by name.

        search_by_type(self, p_type, limit):
            Searches for Pokemon by type.

        search_by_stats(self, stat_name, stat_min, stat_max):
            Returns a random Pokemon whose stat value for the specified stat name is within the given range.

        compare_pokemon(self, pokemon1, pokemon2):
            Compares two Pokemon based on their stats.

        pokemon_visualize(self, name):
            Visualizes the base attributes of a given Pokémon using a bar chart.

        add_pokemon(self, poke_info):
            Adds a new Pokemon to the Pokedex with the provided information.
    """
    
    def __init__(self, file_path):
        
        """
        Initializes a Pokedex object with the data obtained from the JSON file.
        
        Parameters:
            file_path (str): The path to the JSON file containing the Pokemon data.
            
        Returns:
            None
        
        Primary Author:
            Samson Mulugeta
        
        Technique Demonstrated: 
            with statements   
            
        """
        
        with open(file_path, 'r', encoding='utf-8') as f:
            pokemon_data = json.load(f)
        self.pokemon = [Pokemon(data) for data in pokemon_data]
        
    def search_by_name(self, name):
        """
        Searches for a Pokemon by name.

        Parameters:
            name (str): The name of the Pokemon to search for.

        Returns:
            (Pokemon) The Pokemon object if found, otherwise None.
            
        Primary Author:
            Samson Mulugeta
        
        Technique Demonstrated: 
            Conditional expressions 
           
        """

        return next((pkmn for pkmn in self.pokemon if pkmn.name['english'].lower() == name.lower()), None)
    
    def search_by_type(self, p_type, num_results=None):
        """Return a list of Pokemon with a certain type.

        Args:
            p_type (str): The type of Pokemon to search for.
            num_results (int, optional): The maximum number of results to return.
                If not specified, return all matching Pokemon.

        Returns:
            list: A list of Pokemon objects that have the specified type.
                If `num_results` is specified, return at most `num_results` Pokemon.
                If no Pokemon match the type, return an empty list.
        
        Primary Author:
            Samson Mulugeta
            
        Technique Demonstrated: 
            comprehensions or generator expressions 
            
        """
        matching_pokemon = [pkmn for pkmn in self.pokemon if p_type.lower() in [t.lower() for t in pkmn.type]]
        matching_pokemon = random.sample(matching_pokemon, min(num_results, len(matching_pokemon)))
        return matching_pokemon
    
    def search_by_stats(self, stat_name, stat_min, stat_max):
        
        """
        Returns a random Pokemon whose stat value for the specified stat name is within the given range.
        
        Parameters:
            stat_name (str): the name of the stat to search by, e.g. 'attack', 'defense', etc.
            stat_min (int): the minimum value for the stat
            stat_max (int): the maximum value for the stat
        
        Returns:
            a random Pokemon object whose stat value for the specified stat name is within the given range.
            Returns None if no Pokemon are found that meet the criteria.
            
        Primary Author:
            Kyle Doung
        
        Technique Demonstrated: 
            Optional parameters and/or keyword arguments
              
        """
        
        # Find all Pokemon that meet the criteria
        matching_pokemon = [pkmn for pkmn in self.pokemon if stat_min <= getattr(pkmn, stat_name.lower()) <= stat_max]
        
        if not matching_pokemon:
            print("No Pokemon found.")
            return None
        
        # Return the Pokemon with the highest stat value for the specified stat name
        return max(matching_pokemon, key=lambda pkmn: getattr(pkmn, stat_name.lower()))
    
    def compare_pokemon(self, pokemon1, pokemon2):
        
        """
        Compares two Pokemon based on their stats.
        
        Parameters:
            pokemon1 (Pokemon): The first Pokemon to compare.
            pokemon2 (Pokemon): The second Pokemon to compare.
            
        Returns:
            None
            
        Primary Author:
            Samson Mulugeta
            
        Technique Demonstrated: 
            F-strings containing expressions      
            
        """
        
        print(f"Comparing {pokemon1.name['english']} and {pokemon2.name['english']}...\n")
        stats_to_compare = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        for stat in stats_to_compare:
            if getattr(pokemon1, stat) > getattr(pokemon2, stat):
                print(f"{pokemon1.name['english']} has higher {stat}: {getattr(pokemon1, stat)} vs {getattr(pokemon2, stat)}")
            elif getattr(pokemon1, stat) < getattr(pokemon2, stat):
                print(f"{pokemon2.name['english']} has higher {stat}: {getattr(pokemon2, stat)} vs {getattr(pokemon1, stat)}")
            else:
                print(f"{pokemon1.name['english']} and {pokemon2.name['english']} have the same {stat}: {getattr(pokemon1, stat)}")
                
    def pokemon_visualize(pokedex, name):
        
        """
        Visualizes the base attributes of a given Pokémon using a bar chart.
        
        Parameters:
            name (str): The name of the Pokémon to visualize.
        
        Returns:
            None
        
        Raises:
            None
            
            
        Primary Author:
            Peter Zheng
        
        Technique Demonstrated: 
            visualizing data with pyplot or seaborn

        """
        
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
        
    def add_pokemon(poke_string):
        
        """
        Add a new Pokemon to the pokedex.csv file.

        Parameters:
            poke_info (list): A list containing the following Pokemon information in the specified order:

        Returns:
            None
            
        Primary Author:
            Peter Zheng
            
        Techniques Demonstrated:
            Sequence unpacking
             
        """
        poke_info = poke_string.split(",")
        with open('pokedex.csv', 'a+',encoding="utf-8", newline='') as csvfile:
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
  
    def remove_pokemon(pkm):
        
        """
        Remove a Pokemon from the pokedex.csv file.

        Parameters:
            pkm (str): The name of the Pokemon to be removed.

        Returns:
            None
                      
        Primary Author:
            Peter Zheng
            
        """
        
        df = pd.read_csv("pokedex.csv")
        df = df[df["name/english"] != pkm]
        df.to_csv("pokemon.csv", index=False)

    def get_all_types(self):
        
        """
        Returns a list of all unique types of Pokémon in the collection.
        
        Returns:
            list: A sorted list of all types of Pokémon in the collection.
            
        Primary Author:
            Kyle Doung
        
        Techniques Demonstrated:
            set operations on sets or frozensets
            
        """
        
        all_types = set()
        for pkmn in self.pokemon:
            all_types.update(pkmn.type)
        return sorted(all_types)
    
    def print_all_types(self):
        
        """
        Prints a list of all types of Pokémon that can be found in the collection.
        
        Primary Author:
            Kyle Doung
        
        Techniques Demonstrated:
            use of a key function: sorted 
            
        """
        
        all_types = set()
        for pkmn in self.pokemon:
            all_types |= set(pkmn.type)
        print('All types:', ', '.join(sorted(all_types)))
            
    def get_pokemon_name(self, name):
        """
        Searches for a Pokemon by its English name in the `self.pokemon` list and returns its name in English, Japanese, Chinese, and French.

        Args:
        - name (str): The English name of the Pokemon to search for.

        Returns:
        - (dict) A dictionary containing the name of the Pokemon in English, Japanese, Chinese, and French, if the Pokemon is found.
        - (None) If the Pokemon is not found in the `self.pokemon` list.
        
        Primary Author
            Samson Mulugeta
        
        """
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
    
    """
    Main function for the Pokemon search program.

    Parameters:
        filename (str): The name of the JSON file containing the Pokemon data.

    Returns:
        None
        
    Primary Author: 
        Samson Mulugeta
    
    """
    
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
            search_name3 = input('Enter pokemon attributes: (id (empty string),name/english, name other language optional (japanese,chinese,french),type/0,type/1,base/HP,base/Attack,base/Defense,base/Sp. Attack,base/Sp. Defense,base/Speed)')
            poke_info = search_name3.split(",")
            pokedex.add_pokemon(poke_info)
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
    
    """
    Parse command-line arguments.
    
    Args:
        arglist (list of str): a list of command-line arguments to parse.
        
    Returns:
        argparse.Namespace: a namespace object with a file attribute whose value
        is a path to a text file as described above.
        
    Primary Author:
        Kyle Doung
        
    Technique Demonstrated:
        the ArgumentParser class from the argparse module
        
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file of Pokemon")
    return parser.parse_args(arglist)
    
if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)
