import random
import secrets
from .bot_files import BotMap


option_room = ["Комната с монстром", "Комната с монстром", "Комната с монстром", "Медпункт", "Кладовая"]
enemy_list = ["Гоблин", "Гоблин", "Гоблин", "Леший", "Леший", "Дракон"]
enemy_character = {"Гоблин": {"health":3, "damage":1}, "Леший": {"health":10, "damage":2}, "Дракон": {"health":15, "damage":3}}
items_storeroom = [("potion", list(range(1, 3))), ("bow", list(range(1, 5)))]

chance_exit_table = [[0.75, 0,75, 1, 0,75, 0.75],
                     [0.5, 0.25, 0, 0.25, 0.5],
                     [0.15, 0, 0, 0, 0.15],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]]


class Room():
    """
    Класс отвечает за генерацию комнат и определение событий в них.
    
    
    """
    
    def __init__(self, room_value=None):
        self.data = {}
        
        enemy = None
            
        if room_value:
            self.data = {"room": room_value, "enemy": None, "character": None}
                      
        else:
            room = random.choice(option_room)
                           
            if room == "Комната с монстром":
                enemy = random.choice(enemy_list)
                self.data = {"room": room, "enemy": enemy, "character": enemy_character[enemy]}
        
            if room == "Медпункт":
                self.data = {"room": room, "enemy": None, "character": None}
                
            if room == "Кладовая":
                item = random.choice(items_storeroom)
                count_item = random.choice(item[1])
                self.data = {"room": room, "item": item[0], "count_items": count_item}
        
        
    def __repr__(self):
        return f"Room({self.data=})"
    

# Добавляет выходы из пещеры c учётом матрици вероятностей 
def get_chance_exit_table():
    new_table = [[0] * (len(chance_exit_table) + 2)]
    for line in chance_exit_table:
        new_line = [0]
        for element in line:
            
            new_line.append(int(secrets.randbelow(100) <= (element * 100) and element != 0))
        new_line.append(0)        
        new_table.append(new_line)
    new_table.append([0] * (len(chance_exit_table) + 2))
    return new_table
    

def get_random_dice():
    return random.randint(1, 6)
        
        
if __name__ == "__main__":
    room = Room()
    print(room.data)