from .level_map import LevelGenerator


class Weapon():
    
    """
    Класс реализует макет оружия с силой атаки и их количеством 
    
    """
    
    def __init__(self, count: int, power: int):
        self.count = count
        self.power = power
        
    def exist(self):
        if self.count <= -1:
            return True
        return self.count > 0
    
    def __str__(self):
        return f"Weapon(count={self.count=}, power={self.power=})"


class enemyClass():
    
    """
    Класс реализует противника
    
    """
    
    def __init__(self):
        self.kind = ""
        self.health = 0
        self.power = 0

    def damage(self, hero):
        hero.health -= self.power


class heroClass():
    
    """
    Класс реализует героя
    
    """
    
    def __init__(self):
        self.health = 10
        self.sword_damage = 2
        self.potion = Weapon(count=2, power=5)
        self.bow = Weapon(count=5, power=3)
        self.sword = Weapon(count=-1, power=1)
        self.current_weapon: Weapon
            
    def damage(self, enemy:enemyClass):
        self.current_weapon.count -= 1
        enemy.health -= self.current_weapon.power
          
    def change_weapon(self, weapon_name: str):
        if weapon_name == "bow":
            self.current_weapon = self.bow
        elif weapon_name == "potion":            
            self.current_weapon = self.potion
        else:
            self.current_weapon = self.sword
            
    def add_health(self, count_get_health: int):
        self.health += count_get_health
        
    def add_weapon(self, weapon, count_weapon):
        if weapon == "potion": 
            self.potion.count += count_weapon
        elif weapon == "bow":
            self.bow.count += count_weapon
        

class GameData():
    
    """
    В классе хранится состояние игры, реализовано взаимодействие
    героя с противниками и картой
    
    """
    
    def __init__(self):
        self.enemy = enemyClass()
        self.hero = heroClass()
        self.level = LevelGenerator()
        self.kind_room = ""
        self.dice = 1
        self.ownership_move = ""
        
    def change_room(self, direction: str):
        result = 0
        if direction == "roomL":
            result = self.level.move_hero((-1, 0))
        elif direction == "roomF":
            result = self.level.move_hero((0, -1))
        elif direction == "roomR":
            result = self.level.move_hero((1, 0))
        elif direction == "roomB":
            result = self.level.move_hero((0, 1))
            
        if result:
            self.set_room_characters(self.level.this_room.data)
        
        return result
        
    def set_room_characters(self, room_character: dict):
        self.kind_room = room_character["room"]
        if self.kind_room == "Комната с монстром":
            self.enemy.kind = room_character["enemy"]
            self.enemy.health = room_character["character"]["health"]
            self.enemy.power = room_character["character"]["damage"]
            
        
    def delivery_impact(self, value_dice: int):
        self.dice = value_dice
        res_fight = 0
        
        if not self.hero.current_weapon.exist():
            return 0
        
        if value_dice % 2 == 0:
            self.ownership_move = "Вы атакуете"
            res_fight = self.hero.damage(self.enemy)
            
        elif value_dice != 1:
            self.ownership_move = "Противник атакует"
            self.enemy.damage(self.hero)
                
        return 1
        
    def result_fight(self):
        result = ["", self.dice, self.enemy.health, self.hero.health, self.ownership_move]
        if self.dice == 1:
            result[0] = "Выпала 1! Ничья"
            
        elif self.hero.health <= 0:
            result[0] = "Противник победил"
            result[3] = 0
            
        elif self.enemy.health <= 0:
            result[0] = "Вы победили!"
            result[2] = 0
        
        else:
            result[0] = "Бой продолжается"
        return result