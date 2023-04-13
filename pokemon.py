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
    
    def search_by_type(self, p_type):
        matching_pokemon = []
        for pkmn in self.pokemon:
            if p_type.lower() in [t.lower() for t in pkmn.type]:
                matching_pokemon.append(pkmn)
        return matching_pokemon

# Create a Pokedex object
pokedex = Pokedex('pokedex.json')

# Prompt the user to search for a Pokemon by name or type
while True:
    search_type = input('Search by name or type? (enter "exit" to quit): ')
    if search_type.lower() == 'exit':
        break
    elif search_type.lower() == 'name':
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
        search_p_type = input('Enter a type: ')
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
        print('Invalid search type. Please try again.')















