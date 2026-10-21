import random
import time
from abc import ABC, abstractmethod

class Character(ABC):
    def __init__(self, name, health, armor, damage):
        self.name = name
        self._health = health
        self._max_health = health
        self._armor = armor
        self._damage = damage

    def take_damage(self, incoming_damage):
        actual_damage = max(1, incoming_damage - self._armor)
        self._health -= actual_damage
        if self._health < 0:
            self._health = 0
        print(f"{self.name} получает {actual_damage} урона! (Осталось HP: {self._health}/{self._max_health})")

    def is_alive(self):
        return self._health > 0

    @abstractmethod
    def attack(self, target):
        pass

class Knight(Character):
    def __init__(self, name, health, armor, damage, weapon):
        super().__init__(name, health, armor, damage)
        self.weapon = weapon
        self.potions = 2

    def take_damage(self, incoming_damage):
        if self._armor > 0:
            absorbed_damage = incoming_damage * 0.5
            damage_to_health = incoming_damage * 0.5
            
            if self._armor >= absorbed_damage:
                self._armor -= absorbed_damage
                print(f"Броня {self.name} поглотила 50% урона ({absorbed_damage:.1f} ед.). (Прочность брони: {self._armor:.1f})")
            else:
                overflow_damage = absorbed_damage - self._armor
                damage_to_health += overflow_damage
                print(f"Броня {self.name} сломалась! Остатки урона прошли в здоровье.")
                self._armor = 0
                
            self._health -= damage_to_health
            if self._health < 0:
                self._health = 0
            print(f"{self.name} получает {damage_to_health:.1f} урона в здоровье! (Осталось HP: {self._health:.1f}/{self._max_health})")
        else:
            self._health -= incoming_damage
            if self._health < 0:
                self._health = 0
            print(f"У {self.name} нет брони! Весь урон ({incoming_damage}) прошел в здоровье! (HP: {self._health}/{self._max_health})")

    def attack(self, target):
        print(f"{self.name} бьет {self.weapon} по {target.name}!")
        target.take_damage(self._damage)

    def heal(self):
        if self.potions > 0:
            self.potions -= 1
            self._health = min(self._max_health, self._health + 30)
            print(f"{self.name} выпил зелье. Восстановлено 30 HP. (Осталось зелий: {self.potions})")
        else:
            print("Зелья закончились!")

    def inspect(self):
        print(f"{self.name}: HP {self._health:.1f}/{self._max_health}, Броня {self._armor:.1f}, Оружие: {self.weapon}, Зелья: {self.potions}")

class Dragon(Character):
    def __init__(self, name, health, armor, damage):
        super().__init__(name, health, armor, damage)
        self.fire_damage = 12
        self.is_enraged = False

    def attack(self, target):
        if self.is_enraged:
            print(f"{self.name} в ярости дышит огнем на {target.name}!")
            target.take_damage(self.fire_damage) 
        else:
            print(f"{self.name} бьет когтями {target.name}!")
            target.take_damage(self._damage)

    def roar(self):
        self.is_enraged = True
        print("Дракон издает ужасающий рев! Его атаки становятся сильнее!")

    def fly_away(self):
        print(f"{self.name} улетает в закат.")

class Location:
    def __init__(self, name, description, loot):
        self.name = name
        self.description = description
        self.loot = loot
        self.visited = False

    def describe(self):
        print(f"\nВы находитесь: {self.name}")
        print(self.description)

    def search(self):
        self.visited = True
        if self.loot:
            print(f"Вы нашли: {self.loot}!")
            found_loot = self.loot
            self.loot = None
            return found_loot
        else:
            print("Здесь больше ничего нет.")

def main():
    print("=== ТЕКСТОВАЯ ИГРА: РЫЦАРЬ И ДРАКОН ===\n")
    player = Knight(name="Сэр Вадим", health=100, armor=30, damage=15, weapon="Длинный меч")
    boss = Dragon(name="Алый Ужас", health=150, armor=5, damage=12)

    locations = [
        Location("Деревня", "Тихое место, откуда вы начали свой путь.", "Старое зелье"),
        Location("Темный лес", "Здесь пахнет гарью и серой.", "Старый щит (+10 к броне)"),
        Location("Логово дракона", "Пещера, полная золота и костей.", None)
    ]

    game_over = False
    current_loc_index = 0

    while not game_over:
        current_loc = locations[current_loc_index]
        current_loc.describe()

        if current_loc.name == "Логово дракона":
            print("\n Внезапно из темноты вылетает дракон! Бой неизбежен!")
            boss.attack(player)
            
            while player.is_alive() and boss.is_alive():
                player.inspect()
                print("\nВаши действия:")
                print("1. Атаковать")
                print("2. Выпить зелье")
                print("3. Попытаться сбежать")
                
                choice = input("Выберите действие (1-3): ")
                
                if choice == '1':
                    player.attack(boss)
                    if boss.is_alive():
                        if random.random() < 0.3 and not boss.is_enraged:
                            boss.roar()
                        boss.attack(player)
                elif choice == '2':
                    player.heal()
                    boss.attack(player)
                elif choice == '3':
                    print("\n🏃 Вы пытаетесь сбежать...")
                    if random.random() < 0.5:
                        print("Вам удалось сбежать из пещеры!")
                        current_loc_index = 0 
                        break
                    else:
                        print("Дракон преградил вам путь!")
                        boss.attack(player)
                
                time.sleep(1)

            if not player.is_alive():
                print("\n КОНЦОВКА 1 (ПОРАЖЕНИЕ): Дракон одержал победу. Ваши кости останутся в этой пещере навсегда.")
                game_over = True
            elif not boss.is_alive():
                print("\n КОНЦОВКА 2 (ПОБЕДА В БОЮ): Вы сразили Алого Ужаса! Деревня спасена, а вы стали легендой!")
                game_over = True
            elif current_loc_index == 0:
                 print("\n КОНЦОВКА 3 (МИРНАЯ / ПОБЕГ): Вы сбежали из логова. Возможно, вы не герой, но вы живы, чтобы рассказать эту историю.")
                 game_over = True

        else:
            print("\nЧто будете делать?")
            print("1. Идти дальше")
            print("2. Обыскать местность")
            
            choice = input("Выбор: ")
            
            if choice == '1':
                current_loc_index += 1
            elif choice == '2':
                loot = current_loc.search()
                if loot:
                    if "зелье" in loot.lower():
                        player.potions += 1
                        print("Вы положили зелье в сумку.")
                    elif "щит" in loot.lower():
                        player._armor += 10
                        print("Вы надели щит. Прочность брони увеличена!")

if __name__ == "__main__":
    main()

