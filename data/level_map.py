from .generate_random_event import Room, get_chance_exit_table
from .bot_files import BotMap


class LevelGenerator():
    
    """
    Класс досоздает игровую карту и добавляет на неё героя
    
    """
    
    def __init__(self):
        self.hero_pos = (self.x, self.y) = 3, 5
        self.game_map = BotMap().get_map()
        self.this_room = Room("Пустая комната")
        chance_table = get_chance_exit_table()
        lenght_line = len(self.game_map)
        for line_pos in range(lenght_line):
            for room_pos in range(lenght_line):
                if self.game_map[line_pos][room_pos] != "#":
                    if chance_table[line_pos][room_pos]:
                        self.game_map[line_pos][room_pos] = Room("Выход")
                    else:
                        self.game_map[line_pos][room_pos] = Room()
                        
        self.game_map[self.y][self.x] = "@"
        
        
    def move_hero(self, end_pos: tuple):
        
        if self.game_map[self.y + end_pos[1]][self.x + end_pos[0]] != "#":
            self.this_room = self.game_map[self.y + end_pos[1]][self.x + end_pos[0]]
            self.game_map[self.y + end_pos[1]][self.x + end_pos[0]] = self.game_map[self.y][self.x]
            self.game_map[self.y][self.x] = Room("Пустая комната")
            self.x += end_pos[0]
            self.y += end_pos[1]
            return 1
        
        return 0
        
        
if __name__ == "__main__":
    level = LevelGenerator()
    level.move_hero((1, 0))
        