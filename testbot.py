import random

class BattleBot:
    def __init__(self):
        # superficial
        self.name = 'testbot'
        self.color = 'red' # or blue, green, purple

        self.health = 200

        # 6 pts to allocate here
        self.attack_damage = 2
        self.armor = 2
        self.action_speed = 2 

        self.special_attack = 'screwdriver' # can choose one of (however many I make)

    def get_action(self):
        # up to 90 to allocate, must leave last 10 for breaking down

        decision_val = random.randint(0, 100)

        if decision_val <= 30: # must be 30
            return 'attack'
        elif decision_val <= 40:
            return 'build armor'
        elif decision_val <= 60:
            return 'build action speed'
        elif decision_val <= 90:
            return 'build attack'
        else:
            return 'break down'

    # for these three, they have four points to allocate any way they like
    def build_attack(self):
        self.attack_damage += 2

    def build_action_speed(self):
        if self.action_speed < 10:
            self.action_speed += 1
    
    def build_armor(self):
        if self.armor < 7:
            self.armor += 1

    def get_attack_damage(self):
        return self.attack_damage
    
    def get_action_speed(self):
        return self.attack_speed
    
    def take_damage(self, enemy_damage):
        self.health -= enemy_damage * ((10 - self.armor) / 10)

        if self.health < 0:
            self.health = 0 

    def still_functional():
        if self.health > 0:
            return True
        else:
            return False



