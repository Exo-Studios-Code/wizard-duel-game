# ui.py
import os
import time
from colorama import init, Fore, Back, Style

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_intro():
    clear()
    print(Fore.MAGENTA + Style.BRIGHT + '''░▒▓█▓▒░


░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓██████████████▓▒░░▒▓████████▓▒░      ░▒▓█▓▒░▒▓███████▓▒░       ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓████████▓▒░░▒▓██████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░    ░▒▓██▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░        ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓██▓▒░  ░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓██▓▒░    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█████████████▓▒░░▒▓████████▓▒░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█████████████▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  
                                                                                                                                                                                                                         
                                                                                                                                                                                                                         


        🧙‍♂️ Vítej ve světě čar a kouzel! 🧙‍♀️
 -------------------------------------------------------
             Napiš správné kouzlo a přežij!
    ⚔️  Bojuj s nepřáteli v soubojích na život a na smrt!
 -------------------------------------------------------
''')
    print(Fore.CYAN + "-" * 55)
    print("🔮 Napiš správné kouzlo a přežij!")
    print("⚔️  Bojuj s nepřáteli v soubojích na život a na smrt!")
    print("-" * 55)
    print()
# Před začátkem souboje v UI nastavíme HP hráče a další parametry
from colorama import Fore, Style

# Výběr postavy
def select_character():
    character_ids = {
        "1": 1,  # Harry
        "2": 3,  # Ron
        "3": 2,  # Hermione
        "4": 4   # Ginny
    }

    print("Choose your character:")
    print("1 - Harry Potter     ➤ +Chance to succeed | - Defense")
    print("2 - Ron Weasley      ➤ + Damage           | - Accuracy")
    print("3 - Hermione Granger ➤ + Chance           | - Damage")
    print("4 - Ginny Weasley    ➤ + Regeneration     | - Low HP")

    while True:
        choice = input("Enter character number (1-4): ").strip()
        if choice in character_ids:
            return character_ids[choice]
        else:
            print("Invalid choice. Please try again.")

# Překlad ID na jméno
def get_character_name_by_id(character_id):
    characters = {
        1: "Harry Potter",
        2: "Hermione Granger",
        3: "Ron Weasley",
        4: "Ginny Weasleyová"
    }
    return characters.get(character_id, "Neznámá postava")

# Výběr herního módu
def choose_mode():
    print("\nChoose game mode:")
    print("1 - Classic fight")
    print("2 - Survival mode (waves)")
    print("3 - Story mode")
    while True:
        mode = input("Enter mode number (1-3): ")
        if mode in ['1', '2', '3']:
            return int(mode)
        else:
            print("Invalid choice. Try again.")

# Funkce pro vytvoření rámečku kolem textu
def frame_text(text):
    width = max(len(line) for line in text.splitlines()) + 4
    top = "╔" + ("═" * width) + "╗"
    bottom = "╚" + ("═" * width) + "╝"
    body = "\n".join([f"║  {line.ljust(width - 2)}║" for line in text.splitlines()])
    return f"{top}\n{body}\n{bottom}"

# Health bar s barvami
def draw_health_bar(current_hp, max_hp, is_player=True, name=""):
    bar_length = 30
    health_percentage = current_hp / max_hp if max_hp > 0 else 0
    filled_length = int(health_percentage * bar_length)

    if is_player:
        if health_percentage > 0.6:
            color = Fore.GREEN
        elif health_percentage > 0.3:
            color = Fore.YELLOW
        else:
            color = Fore.RED
    else:
        if health_percentage > 0.6:
            color = Fore.CYAN
        elif health_percentage > 0.3:
            color = Fore.MAGENTA
        else:
            color = Fore.RED

    bar = f"{color}{name} HP: [{'#' * filled_length}{'.' * (bar_length - filled_length)}] {current_hp}/{max_hp}{Style.RESET_ALL}"
    return bar

def draw_stamina_bar(current, max_value, is_player=True, name=""):
    bar_length = 20
    filled_length = int(bar_length * current / max_value)
    empty_length = bar_length - filled_length
    bar = "█" * filled_length + "-" * empty_length

    # Vypočítáme procenta staminy
    stamina_percentage = (current / max_value) * 100

    # Určíme barvu podle procenta staminy s plynulým přechodem
    if stamina_percentage > 75:
        color = "\033[92m"  # Zelená pro 76%-100%
    elif stamina_percentage > 50:
        color = "\033[93m"  # Žlutá pro 51%-75%
    elif stamina_percentage > 25:
        color = "\033[33m"  # Oranžová pro 26%-50%
    else:
        color = "\033[91m"  # Červená pro 0%-25%

    # Pokud je hráč, použijeme "name", jinak "Nepřítel"
    label = f"{name}'s" if is_player else "Nepřítel"

    # Vracíme barvu a formátování pro výpis
    return f"🔋 {label} stamina: {color}[{bar}] {current}/{max_value}\033[0m"


# Text v rámečku
def draw_boxed_text(text, color=Fore.WHITE):
    max_length = 150
    text = f" {text} "
    padding = max_length - len(text)
    left_padding = padding // 2
    right_padding = padding - left_padding
    content_line = f"│{' ' * left_padding}{text}{' ' * right_padding}│"
    top = f"┌{'─' * max_length}┐"
    bottom = f"└{'─' * max_length}┘"
    return f"{color}{top}\n{content_line}\n{bottom}{Style.RESET_ALL}"

# Kouzla
def draw_spells(spells, spell_data):
    spell_text = "\nDostupná kouzla:"
    for spell in spells:
        data = spell_data.get(spell)
        if data and 'chance' in data:
            chance = data['chance']
            spell_text += f"\n{draw_boxed_text(f'{spell} (Šance: {chance * 100:.0f}%)', Fore.CYAN)}"
        else:
            spell_text += f"\n{draw_boxed_text(f'{spell} (Neznámé kouzlo)', Fore.RED)}"
    return spell_text

def draw_main_menu():
    print(Fore.MAGENTA + Style.BRIGHT)
    print("╔═══════════════════════════════════════╗")
    print("║        🧙‍♂️  WIZARD DUEL ARENA  🧙‍♀️    ║")
    print("╠═══════════════════════════════════════╣")
    print("║ 1. ▶️  Hrát                           ║")
    print("║ 2. 🛠️  Zadat vývojářský kód          ║")
    print("║ 3. ❌  Ukončit hru                   ║")
    print("║ 4. 📊  Zobrazit statistiky           ║")  # Přidání volby pro statistiky
    print("║ 5. 💾  Uložit hru                   ║")  # Přidání volby pro uložení hry
    print("║ 6. 📂  Načíst hru                   ║")  # Přidání volby pro načtení hry
    print("╚═══════════════════════════════════════╝")
    print(Style.RESET_ALL)



# Celkový rámeček hry
def game_frame(text):
    width = max(len(line) for line in text.splitlines()) + 4
    top = "╔" + ("═" * width) + "╗"
    bottom = "╚" + ("═" * width) + "╝"
    body = "\n".join([f"║  {line.ljust(width - 2)}║" for line in text.splitlines()])
    return f"{top}\n{body}\n{bottom}"

# Hlavní funkce UI
def start_ui():
    show_intro()  # Ujisti se, že show_intro() je definována jinde
    character_id = select_character()
    character_name = get_character_name_by_id(character_id)
    mode_id = choose_mode()
    return character_id, mode_id
