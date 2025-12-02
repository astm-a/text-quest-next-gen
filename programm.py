import random;
import os;

clear = lambda: os.system('cls');

class Player:
    def __init__(self,money: int = 1000):
        self.money = money;
        self.sanity = 100;
        self.tilt = False;

    def change_sanity(self, delta):
        self.sanity = max(0, min(100, self.sanity + delta));
        self.tilt = self.sanity < 30;

    def can_bet(self, amount):
        return 0 < amount <= self.money;

class Game:
    def __init__(self):
        self.player = Player();

    def run(self):
        while True:
            clear();
            if self.player.money <= 0:
                print("Деньги кончились. Вас выставили.");
                break;
            if self.player.sanity <= 0:
                print("Вы теряете рассудок окончательно. Охрана уводит вас.");
                break;
            print("Гуляя по улице, вам в глаза бросается вывеска казино. Хотите ли вы войти?");
            print("1. Да");
            print("2. Нет");
            choice = input("> ").strip();
            if choice == "1":
                self.lobby();
            elif choice == "2":
                print("Вы прошли мимо.");
                break;
            else:
                print("Неверный выбор.");

    def lobby(self):
        while True:
            clear();
            if self.player.money <= 0 or self.player.sanity <= 0:
                break;
            print(f"Деньги: {self.player.money}  Рассудок: {self.player.sanity}{' (ТИЛЬТ)' if self.player.tilt else ''}");
            print("1. Рулетка");
            print("2. Покер (недоступно)");
            print("3. Однорукий бандит (в ремонте)");
            print("4. Выйти из казино");
            choice = input("> ").strip();
            if choice == "1":
                if self.player.money <= 0:
                    print("Вас не пускают, так как у вас кончились деньги");
                else:
                    self.roulette();
            elif choice == "4":
                return;
            else:
                print("Пока не работает.");

    def roulette(self):
        while True:
            clear();
            if self.player.money <= 0:
                print("Деньги кончились. Вас выставили.");
                break;
            print("Рулетка: 0-32");
            if self.player.tilt:
                bet = random.randint(1, min(self.player.money, 100));
                guess = random.randint(0, 32);
                print(f"Тильт: ставка {bet} на {guess}");
            else:
                try:
                    bet = int(input(f"Ставка (1-{self.player.money}): "));
                    if bet <= self.player.money:
                        guess = int(input("Число 0-32: "));
                        if not self.player.can_bet(bet) or not 0 <= guess <= 32:
                            print("Неверные данные.");
                            input("Enter...");
                            return self.roulette();
                    else:
                        print("У вас недостаточно денег для такой ставки! попробуйте ещё раз");
                        input("Enter...");
                        return self.roulette();
                except ValueError:
                    print("Введите число.");
                    input("Enter...");
                    return self.roulette();

            result = random.randint(0, 32);
            print(f"Выпало: {result}");
            if guess == result:
                win = bet * 32;
                self.player.money += win;
                self.player.change_sanity(10);
                print(f"Выигрыш: {win}");
                input("Enter...");
                break;

            else:
                self.player.money -= bet;
                self.player.change_sanity(-15);
                print("Проигрыш.");
                input("Enter...");
                break;

if __name__ == "__main__":
    try:
        Game().run();
    except KeyboardInterrupt:
        print("\nИгра прервана пользователем.");
    except Exception as e:
        print(f"\nНепредвиденная ошибка: {e}");
    finally:
        print("\nСпасибо за игру!");
