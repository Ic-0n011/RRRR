import os
from random import randint, choice

first_names = ("Жран", "Дрын", "Брысь", "Жлыг")
last_names = ("Ужасный", "Зловонный", "Борзый", "Кровавый")


def make_hero(
        name=None,
        hp_now=None,
        hp_max=None,
        lvl=1,
        xp_now=0,
        attack=1,
        defence=1,
        luck=1,
        money=None,
        inventory=None,
) -> list:
    """
    Персонаж - это список
    [0] name - имя
    [1] hp_now - здоровье текущее
    [2] hp_max - здоровье максимальное
    [3] lvl - уровень
    [4] xp_now - опыт текущий
    [5] xp_next - опыт до следующего уровня
    [6] attack - сила атаки, применяется в бою
    [7] defence - защита, применяется в бою
    [8] luck - удача
    [9] money - деньги
    [10] inventory - список предметов
    """
    if not name:
        name = choice(first_names) + " " + choice(last_names)

    if not hp_now:
        hp_now = randint(1, 100)
    
    if not hp_max:
        hp_max = hp_now

    xp_next = lvl * 100

    if money is None:
        money = randint(0, 100)

    if not inventory:
        inventory = []
    
    return [
        name,
        hp_now,
        hp_max,
        lvl,
        xp_now,
        xp_next,
        attack,
        defence,
        luck,
        money,
        inventory
    ]



def show_hero(hero:list) -> None:
    print("имя:", hero[0])
    print("здоровье:", hero[1], "/", hero[2])
    print("уровень:", hero[3])
    print("опыт:", hero[4], "/", hero[5])
    print("атака:", hero[6])
    print("защита:", hero[7])
    print("удача:", hero[8])
    print("деньги:", hero[9])
    print("инвентарь:", hero[10])  # TODO: показать предметы и их количество
    print("")


def levelup(hero: list) -> None:
    """
    TODO: что растет с уровнем?
    """
    while hero[4] >= hero[5]:
        hero[3] += 1
        hero[5] = hero[3] * 100
        print(f"{hero[0]} получил {hero[3]} уровень\n")


def buy_item(hero: list, price: int, item: str) -> None:
    """
    Покупает предмет item за price монет и кладет его в инвентарь героя
    """
    os.system("cls")
    if hero[9] >= price:
        hero[9] -= price
        hero[10].append(item)
        print(f"{hero[0]} купил {item} за {price} монет!")
    else:
        print(f"У {hero[0]} нет столько монет! Не хватило {price - hero[9]}")
    input("\nНажмите ENTER чтобы продолжить ")


def consume_item(hero: list, idx: str) -> None:
    """
    Удаляет предмет из инвентаря по индексу и дает герою эффект этого предмета
    """
    if idx <= len(hero[10]) - 1 and idx > -1:
        print(f"{hero[0]} употребил {hero[10][idx]}")
        if hero[10][idx] == "зелье":
            hero[1] += 10
            if hero[1] > hero[2]:
                hero[1] = hero[2]
        elif hero[10][idx] == "яблоко":
            pass
        else:
            print("Никакого эффекта")
        hero[10].pop(idx)
    else:
        print("Нет такого индекса!")
    print("")


def play_dice(hero: list, bet: str) -> None:
    """
    Ставка от 1 монеты до количества монет героя
    Игрок и казино бросаю кости, кто больше, то забирает ставку
    TODO: Как удача влияет на кости?
    """
    try:
        bet = int(bet)
        except ValueError:
        print("Ставка недопустима")
    else:
        if bet > 0:
            if hero[9] >= bet:
                hero_score = randint(2, 12)
                casino_score = randint(2, 12)
                print(f"{hero[0]} выбросил {hero_score}")
                print(f"Трактирщик выбросил {casino_score}")
                if hero_score > casino_score:
                    hero[9] += bet
                    print(f"{hero[0]} выиграл {bet} монет")
                elif hero_score < casino_score:
                    hero[9] -= bet
                    print(f"{hero[0]} проиграл {bet} монет")
                else:
                    print("Ничья!")
            else:
                print(f"У {hero[0]} нет денег на такую ставку!")
        else:
            print("Ставки начинаются от 1 монеты!")



    input("\nНажмите ENTER чтобы продолжить")


def combat_turn(attacker, defender):
    if attacker[1] > 0:
        damage = attacker[6]
        defender[1] -= damage
        print(f"{attacker[0]} ударил {defender[0]} на {damage} жизней!")


def start_fight(hero: list) -> None:
    """
    Зависит ли враг от уровня героя?
    Формула аткаи и защиты?
    Можно ли выпить зелье в бою?
    """
    enemy = make_hero(hp_now=30, xp_now=123, inventory=["вражеский меч", "вражеский конь"])
    while hero[1] > 0 and enemy[1] > 0:
        os.system("cls")
        combat_turn(hero, enemy)
        combat_turn(enemy, hero)
        print("")
        show_hero(hero)
        show_hero(enemy)
        input("\nНажмите ENTER чтобы сделать следующий ход")
    count_fight_result(hero, enemy)


def count_fight_result(hero, enemy):
    os.system("cls")
    if hero[1] > 0 and enemy[1] <= 0:
        print(f"{hero[0]} победил и получает в награду:")
        hero[4] += enemy[4]
        print(enemy[4], "опыта")
        hero[9] += enemy[9]
        print(enemy[9], "монет")
        print("и предметы: ", end="")
        for item in enemy[10]:
            print(item, end=", ")
        hero[10] += enemy[10]
        levelup(hero)
    elif hero[1] <= 0 and enemy[1] > 0:
        print(f"{enemy[0]} победил!")
        print("Игра должна закончиться тут!")
    else:
        print(f"{hero[0]} и {enemy[0]} пали в бою:(")
        print("Игра должна закончиться тут!")


def choose_option(hero: list, text: str, options: list) -> int:
    """
    Показывает описание ситуации
    Показывает варианты
    Получает ввод пользователя
    Проверяет ввод и возвращает его, если он есть в вариантах
    """
    os.system("cls")
    show_hero(hero)
    print(text)
    for num, option in enumerate(options):
        print(f"{num}. {option}")
    option = input("\nВведите номер варианта и нажмите ENTER: ")
    try:
        option = int(option)
    except:  # выполнится, если try не получится
        print("Ввод должен быть целым неотрицательным числом")
    else:  # выполнится, если try удался
        if option < len(options) and option > -1:
            return option
        else:
            print("Нет такого выбора")


def visit_hub(hero):
    text = f"{hero[0]} приехал к Хаб, здесь есть чем заняться:"
    options = [
        "заглянуть в лавку алхимика",
        "пойти в казино",
        "выйти в главное меню",
    ]
    option = choose_option(hero, text, options)
    os.system("cls")
    if option == 0:
        return visit_shop(hero)
    elif option == 1:
        return visit_casino(hero)
    elif option == 2:
        print("ушел в меню -почти-")
    elif option == 3:
        consume_item(hero, 0)
    input("\nНажмите ENTER чтобы продолжить")


def visit_shop(hero:list) -> None:
    text = f"{hero[0]} приехал в лавку алхимика. здесь странно пахнет и продаются зелья. "
    options = ["купить зелье лечения за 10 монет",
        "купить зелье опыта ха 30 монет",
        "выйти из лавки в хаб",
        ]
    option = choose_option(hero, text, options)
    if option == 0:
        buy_item(hero, 10, "зелье лечение")
        return visit_shop(hero)
    elif option == 1:
        buy_item(hero, 30, "зелье опыта")
        return visit_shop(hero)
    elif option == 2:
         return visit_hub(hero)
    input("\nНажмите ENTER чтобы продолжить ")


def visit_casino(hero: list) -> None:
    text = f"{hero[0]} приехал в казино. за вами следят охраники. "
    options = ["сесть за ближайший стол",
        "выйти из лавки в хаб",
        ]
    option = choose_option(hero, text, options)
    if option == 0:
        print("вы сели за стол")
        bet = input("Выберите ставку: ")
        return play_dice(hero, bet)
    elif option == 1:
        return visit_hub(hero)
        
    input("\nНажмите ENTER чтобы продолжить ")