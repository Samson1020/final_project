import json

class Pokemon:
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
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            pokemon_data = json.load(f)
        self.pokemon = [Pokemon(data) for data in pokemon_data]
    
    def search_by_name(self, name):
        for pkmn in self.pokemon:
            if pkmn.name['english'].lower() == name.lower():
                return pkmn
        return None
    
    def search_by_type(self, p_type, limit=5):
        matching_pokemon = []
        for pkmn in self.pokemon:
            if p_type.lower() in [t.lower() for t in pkmn.type]:
                matching_pokemon.append(pkmn)
        matching_pokemon.sort(key=lambda pkmn: pkmn.attack, reverse=True)
        return matching_pokemon
    
    def filter_by_hp(self, min_hp=None, max_hp=None):
        filtered_pokemon = []
        for pkmn in self.pokemon:
            if min_hp is not None and pkmn.hp < min_hp:
                continue
            if max_hp is not None and pkmn.hp > max_hp:
                continue
            filtered_pokemon.append(pkmn)
        return filtered_pokemon
    
    def filter_by_attack(self, min_attack=None, max_attack=None):
        filtered_pokemon = []
        for pkmn in self.pokemon:
            if min_attack is not None and pkmn.attack < min_attack:
                continue
            if max_attack is not None and pkmn.attack > max_attack:
                continue
            filtered_pokemon.append(pkmn)
        return filtered_pokemon
    
    def filter_by_defense(self, min_defense=None, max_defense=None):
        filtered_pokemon = []
        for pkmn in self.pokemon:
            if min_defense is not None and pkmn.defense < min_defense:
                continue
            if max_defense is not None and pkmn.defense > max_defense:
                continue
            filtered_pokemon.append(pkmn)
        return filtered_pokemon
    
    def filter_by_sp_attack(self, min_sp_attack=None, max_sp_attack=None):
        filtered_pokemon = []
        for pkmn in self.pokemon:
            if min_sp_attack is not None and pkmn.sp_attack < min_sp_attack:
                continue
            if max_sp_attack is not None and pkmn.sp_attack > max_sp_attack:
                continue
            filtered_pokemon.append(pkmn)
        return filtered_pokemon
    
    def filter_by_sp_defense(self, min_sp_defense=None, max_sp_defense=None):
        filtered_pokemon = []
        for pkmn in self.pokemon:
            if min_sp_defense is not None and pkmn.sp_defense < min_sp_defense:
                continue
            if max_sp_defense is not None and pkmn.sp_defense > max_sp_defense:
                continue
            filtered_pokemon.append(pkmn)
        return filtered_pokemon
    
    def filter_by_speed(self, min_speed, max_speed):
        matching_pokemon = []
        for pkmn in self.pokemon:
            if min_speed <= pkmn.speed <= max_speed:
                matching_pokemon.append(pkmn)
        return matching_pokemon
    
    def sort_by_id(self):
        self.pokemon.sort(key=lambda pkmn: pkmn.id)
    
    def sort_by_name(self):
        self.pokemon.sort(key=lambda pkmn: pkmn.name['english'])
    
    def sort_by_type(self):
        self.pokemon.sort(key=lambda pkmn: pkmn.type[0])
    
    def sort_by_attack(self):
        self.pokemon.sort(key=lambda pkmn: pkmn.attack, reverse=True)

    def sort_by_defense(self):
        self.pokemon.sort(key=lambda pkmn: pkmn.defense, reverse=True)

    def sort_by_sp_attack(self):
        self.pokemon.sort(key=lambda pkmn: pkmn.sp_attack, reverse=True)

    def sort_by_sp_defense(self):
        self.pokemon.sort(key=lambda pkmn: pkmn.sp_defense, reverse=True)

    def sort_by_speed(self):
        self.pokemon.sort(key=lambda pkmn: pkmn.speed, reverse=True)

    def get_all_types(self):
        all_types = set()
        for pkmn in self.pokemon:
            all_types.update(pkmn.type)
        return sorted(all_types)
    
    def print_all_types(self):
        all_types = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']
        print('All types:', ', '.join(all_types))

# Create a Pokedex object
pokedex = Pokedex('pokedex.json')

# Get all Pokemon types
all_types = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']

# Prompt the user to search for a Pokemon by name or type
while True:
    search_type = input('Search by name or type? (enter "exit" to quit): ')
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
        # Prompt the user to select a type from the list of all types
        print('All types:', ', '.join(all_types))
        search_p_type = input('Enter a type: ')
        max_results = input('Enter the maximum number of results to display: ')
        try:
            max_results = int(max_results)
        except ValueError:
            print('Invalid input for maximum results. Displaying all matches.')
            max_results = None
        matching_pokemon = pokedex.search_by_type(search_p_type, limit=max_results)
        if search_p_type.lower() in [t.lower() for t in all_types]:
            matching_pokemon = pokedex.search_by_type(search_p_type)
            if matching_pokemon:
                for pkmn in matching_pokemon:
                    print(f'ID: {pkmn.id}')
                    print(f'Name: {pkmn.name["english"]}')
                    print(f'Type: {", ".join(pkmn.type)}')
                    print(f'HP: {pkmn.hp}')
                    print(f'Attack: {pkmn.attack}')
                    print(f'Defense: {pkmn.defense}')
                    print(f'Special Attack: {pkmn.sp_attack}')
                    print(f'Special Defense: {pkmn.sp_defense}')
                    print(f'Speed: {pkmn.speed}')
            else:
                print('No matching Pokemon found.')
        else:
            print('Invalid type. Please select a type from the list.')
    else:
        print('Invalid search type. Please try again.')
