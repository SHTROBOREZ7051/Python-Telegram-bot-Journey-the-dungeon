import json
import os


class BotPhrases():
    
    """
    Класс читате из файла responses.json фразы бота и возвращает их
    с игровым значением (где это надо)
    
    """
    
    def __init__(self, path="data/"):
        with open(path + "responses.json", "r", encoding='utf-8') as file:
            phrases = json.load(file)[0]
        self.greeting = phrases["start"]
        self.help = phrases["help"]
        self.start_game = phrases["start_game"]
        self.beginning_fight = phrases["room_with_enemy"]
        self.post_fight_results = phrases["post_fight_results"]
        self.need_get_kit = phrases["need_get_kit"]
        self.get_kit_phrase = phrases["get_kit"]
        self.not_get_kit_phrase = phrases["not_get_kit"]
        self.choice_path = phrases["choice_path"]
        self.exit_text = phrases["exit"]
        self.next_game_text = phrases["next_game"]
        self.hero_lost_text = phrases["hero_lost"]
        self.weapon_names = {element: phrases[element] for element in ["sword", "bow", "potion"]}
        self.get_weapon_phrase = phrases["get_weapon"]
        self.arsenal_phrase = phrases["get_arsenal"]
        self.arsenal_with_health = phrases["arsenal_with_health"]
        self.rules = phrases["rules"]
        
    
    def get_greeting(self):
        return self.greeting
    
    def get_help(self):
        return self.help
    
    def get_start_game_phras(self):
        return self.start_game
    
    def get_beginning_fight(self, enemy):
        return self.beginning_fight.format(enemy.kind, enemy.health, enemy.power)
    
    def get_post_fight_results(self, data: list):
        return self.post_fight_results.format(data[0], data[1], data[2], data[3], data[4])
    
    def get_need_kit(self):
        return self.need_get_kit
    
    def get_kit(self, count_get_health: int):
        return self.get_kit_phrase.format(count_get_health)
    
    def not_get_kit(self):
        return self.not_get_kit_phrase
    
    def get_choice_path(self):
        return self.choice_path
    
    def get_exit_text(self):
        return self.exit_text
    
    def get_next_game_text(self):
        return self.next_game_text
    
    def get_hero_lost_text(self):
        return self.hero_lost_text
    
    def get_rules(self):
        return self.rules
    
    def get_weapon_name(self, name_weapon:str):
        return self.weapon_names[name_weapon]
    
    def get_weapon(self, name_weapon:str, count_weapon:int):
        return self.get_weapon_phrase.format(self.get_weapon_name(name_weapon), count_weapon)
    
    def get_arsenal_phrases(self, count_bow:int, count_potion:int):
        return self.arsenal_phrase.format(count_bow, count_potion)
    
    def get_arsenal_with_health_phrases(self, health:int, count_bow:int, count_potion:int):
        return self.arsenal_with_health.format(health, count_bow, count_potion)
    
    
class BotMap():
    
    """
    Класс читает из файла map.txt строение карты и возвращает её
    в виде матрици
    
    """
    
    def __init__(self, path="data/"):
        self.map = []
        with open(path + "map.txt", "r") as file:
            line = file.readline()
            while line:
                sublist = []
                for element in line:
                    if element != "\n":
                        sublist.append(element)
                self.map.append(sublist)
                line = file.readline()
            
    def get_map(self):
        return self.map
            
            
if __name__ == "__main__":
    botResp = BotResponses(path="")
    print(botResp.get_greeting())
    print(botResp.get_help())
    print(botResp.get_start_game_phras())
    botMap = BotMap("")
    print(botMap.map)
    