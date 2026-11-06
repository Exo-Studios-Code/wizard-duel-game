import random
import sys
import time
import os
from colorama import init, Fore, Back, Style
import game_ui as ui  # Tento import je v pořádku
from game_ui import draw_health_bar, draw_spells, draw_boxed_text, draw_stamina_bar
import anticheat
from spell_combos import SPELL_COMBINATIONS
from sounds import play_background_music
import json
from qte import quick_time_event
from playsound import playsound





STATS_FILE = "wizard_duel_stats.json"

def load_stats():
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "wins": 0,
            "losses": 0,
            "total_matches": 0,
            "max_level": 1,
            "total_xp": 0,
            "defeated_enemies": 0
        }

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

stats = load_stats()
# Funkce pro start různých módů

def play_spell_sound(spell_name):
    # Cesta ke zvukům - uprav si podle sebe
    sounds_dir = "sounds/spells"
    file_mp3 = os.path.join(sounds_dir, f"{spell_name}.mp3")
    file_wav = os.path.join(sounds_dir, f"{spell_name}.wav")

    if os.path.isfile(file_mp3):
        playsound(file_mp3, block=False)
    elif os.path.isfile(file_wav):
        playsound(file_wav, block=False)
    else:
        # Zvuk nenalezen, nemusí se nic dít nebo výpis
        pass



def start_fight(character):
    print(f"⚔️ Zahajuji souboj s postavou: {state['player_name']}")

def start_survival(character):
    print(f"🧟‍♂️ Spouštím survival mód pro: {state['player_name']}")

def start_story(character):
    print(f"📖 Spouštím příběhový mód pro: {state['player_name']}")






# Místní slovník pro mapování ID postavy na jméno a atributy
# Filtrování kouzel – jen ta, která nejsou tajná

SPELLS = {
    "expelliarmus": {"effect": "disarm", "power": 10, "chance": 0.9, "stamina_cost": 10},
    "stupefy": {"effect": "stun", "power": 10, "chance": 0.85, "stamina_cost": 10},
    "sectumsempra": {"effect": "damage", "power": 30, "chance": 0.75, "stamina_cost": 25},
    "petrificus totalus": {"effect": "paralyze", "power": 0, "chance": 0.8, "stamina_cost": 15},
    "avada kedavra": {"effect": "instant_kill", "power": 1000, "chance": 0.10, "stamina_cost": 50},
    "protego": {"effect": "shield", "power": 0, "chance": 1.0, "stamina_cost": -10},  # doplní staminu
    "protego maxima": {"effect": "big_shield", "power": 0, "chance": 1.0, "stamina_cost": -15},
    "impedimenta": {"effect": "slow", "power": 0, "chance": 0.7, "stamina_cost": 10},
    "rictusempra": {"effect": "stun", "power": 5, "chance": 0.9, "stamina_cost": 8},
    "crucio": {"effect": "damage", "power": 50, "chance": 0.2, "stamina_cost": 40},
    "incendio": {"effect": "fire", "power": 20, "chance": 0.8, "stamina_cost": 20},
    "expulso": {"effect": "explosion", "power": 40, "chance": 0.35, "stamina_cost": 35},
    "reducto": {"effect": "damage", "power": 30, "chance": 0.7, "stamina_cost": 25},
    "illusion": {"effect": "dodge_next", "power": 0, "chance": 0.5, "secret": True, "stamina_cost": -20},
    "dark curse": {"effect": "damage", "power": 60, "chance": 0.3, "secret": True, "stamina_cost": 45}
}


available_spells = [spell for spell, data in SPELLS.items() if not data.get("secret", False)]

CHARACTERS = {
    1: {
        "name": "Harry Potter",
        "hp": 100,
        "advantage": "Chance to succeed",
        "disadvantage": "Low defense",
        "spells": available_spells
    },
    2: {
        "name": "Hermione Granger",
        "hp": 100,
        "advantage": "Chance",
        "disadvantage": "Low damage",
        "spells": available_spells
    },
    3: {
        "name": "Ron Weasley",
        "hp": 110,
        "advantage": "High damage",
        "disadvantage": "Low accuracy",
        "spells": available_spells
    },
    4: {
        "name": "Ginny Weasleyová",
        "hp": 90,
        "advantage": "Regeneration",
        "disadvantage": "Low HP",
        "spells": available_spells
    }
}


ENEMIES = {
    "Lucius Malfoy": {
        "hp": 140,
        "advantage": "strategy",
        "disadvantage": "arrogance",
        "quotes": {
            "start_fight": [
                "Malfoyové se nikdy neskloní!",
                "Jak se opovažuješ postavit se mi?"
            ],
            "cast_spell": [
                "Pocítíš mou moc!",
                "Toto bude tvůj konec!"
            ],
            "take_damage_light": [
                "To nic nebylo.",
                "Jen škrábnutí."
            ],
            "take_damage_heavy": [
                "Aargh!",
                "To tě bude mrzet!"
            ],
            "shield_block": [
                "Tvůj útok je slabý!",
                "Za takové kouzlo by ses styděl!"
            ],
            "player_miss": [
                "Minul jsi, ubožáku!",
                "Ani se netrefíš?"
            ],
            "defeat": [
                "Nemožné... já... Malfoy... jsem poražen?"
            ]
        }
    },
    "Bellatrix Lestrange": {
        "hp": 120,
        "advantage": "crazy strong",
        "disadvantage": "reckless",
        "quotes": {
            "start_fight": [
                "Jsem nejděsivější smrtijedka!",
                "Tvé utrpení právě začíná!"
            ],
            "cast_spell": [
                "Obětuj se temnotě!",
                "Užij si tenhle oheň!"
            ],
            "take_damage_light": [
                "Hahaha, to mě nerozhodí.",
                "Tak málo?!"
            ],
            "take_damage_heavy": [
                "Agh! Budeš za to platit!",
                "Ty blázne!"
            ],
            "shield_block": [
                "Za takovou hračku si nezasloužíš život!",
                "Tvé čáry jsou slabé!"
            ],
            "player_miss": [
                "Haha, chybil jsi!",
                "Nedokážeš mě zasáhnout!"
            ],
            "defeat": [
                "Není možné, že padnu..."
            ]
        }
    },
    "Draco Malfoy": {
        "hp": 100,
        "advantage": "fast",
        "disadvantage": "weak",
        "quotes": {
            "start_fight": [
                "Nebudeš mě porazit tak snadno!",
                "Jsem rychlejší, než si myslíš!"
            ],
            "cast_spell": [
                "Pokusím se tě zaskočit!",
                "Kouzelník Malfoy nikdy neprohrává!"
            ],
            "take_damage_light": [
                "To nic není.",
                "Můžeš víc!"
            ],
            "take_damage_heavy": [
                "Ááá!",
                "To bolelo!"
            ],
            "shield_block": [
                "Tvůj útok mě nezastaví!",
                "Můj štít je silnější!"
            ],
            "player_miss": [
                "Haha, minul jsi!",
                "Nedokážeš mě zasáhnout!"
            ],
            "defeat": [
                "Tohle nemůže být konec..."
            ]
        }
    },
    "Voldemort": {
        "hp": 200,
        "advantage": "powerful",
        "disadvantage": "ego",
        "quotes": {
            "start_fight": [
                "Ty jsi jen prach proti mé moci!",
                "Tvé šance jsou nulové!"
            ],
            "cast_spell": [
                "Smrt přijde rychle!",
                "Ničím tě!"
            ],
            "take_damage_light": [
                "To je jen zpoždění mého vítězství.",
                "Nemáš šanci mě porazit!"
            ],
            "take_damage_heavy": [
                "Ty darebáku!",
                "Toto ještě nekončí!"
            ],
            "shield_block": [
                "Tvé čáry jsou slabé jako tvá vůle!",
                "Nezastavíš mě!"
            ],
            "player_miss": [
                "Slabý pokus!",
                "Marný pokus mě zasáhnout!"
            ],
            "defeat": [
                "Tohle není konec... Budu se vracet..."
            ]
        }
    }
}


LOCATIONS = {
    "Zakázaný les": ["Bellatrix Lestrange", "Lucius Malfoy"],
    "Bradavice": ["Draco Malfoy"],
    "Azkaban": ["Voldemort"]
}

STORY = {
    "intro": {
        "text": "Byl jsi povolán do Bradavic, kde tě čeká velké dobrodružství. Temné síly se znovu probouzejí a jen ty můžeš najít tři relikvie a zastavit Voldemorta.",
        "choices": [
            {"text": "Vydat se do Zakázaného lesa", "next": "forest_1"},
            {"text": "Navštívit Bradavice", "next": "hogwarts_1"},
            {"text": "Vydat se do Azkabanu", "next": "azkaban_1"}
        ]
    },

    "forest_1": {
        "text": "V Zakázaném lese je tma a hustá mlha. Z lesa vystupuje Bellatrix Lestrange s šíleným smíchem.",
        "choices": [
            {
                "text": "Postavit se jí v souboji",
                "fight": "Bellatrix Lestrange",
                "success_next": "forest_2",
                "relic": "Meč Godrika Nebelvíra"
            },
            {
                "text": "Zkusit uniknout tiše pryč",
                "success_next": "forest_2",
                "fail_fight": "Bellatrix Lestrange",
                "fail_next": "fight_result"
            }
        ]
    },

    "forest_2": {
        "text": "Zbavil ses Bellatrix. Cesta se ti otevírá dál do hlubin lesa.",
        "next": "forest_relic"
    },

    "forest_relic": {
        "text": "Našel jsi starý oltář s nápisem. Pod ním leží Meč Godrika Nebelvíra!",
        "relic": "Meč Godrika Nebelvíra",
        "choices": [
            {"text": "Vrátit se do Bradavic", "next": "hub"}
        ]
    },

    "hogwarts_1": {
        "text": "V Bradavicích je nezvyklé ticho. Potkáváš Draca Malfoye, který tě chce zastavit.",
        "choices": [
            {
                "text": "Přesvědčit ho, že vám jde o stejnou věc",
                "success_next": "hogwarts_2",
                "fail_fight": "Draco Malfoy",
                "fail_next": "fight_result"
            },
            {
                "text": "Zaútočit přímo",
                "fight": "Draco Malfoy",
                "success_next": "hogwarts_2"
            }
        ]
    },

    "hogwarts_2": {
        "text": "Draco je z cesty. Pokračuješ do Velké síně.",
        "next": "hogwarts_relic"
    },

    "hogwarts_relic": {
        "text": "Ve Velké síni pod starým portrétem nacházíš Kámen vzkříšení!",
        "relic": "Kámen vzkříšení",
        "choices": [
            {"text": "Vrátit se do Bradavic", "next": "hub"}
        ]
    },

    "azkaban_1": {
        "text": "V Azkabanu je zlověstné ticho a mrazivý vzduch. Z mlhy vystupuje Lucius Malfoy.",
        "choices": [
            {
                "text": "Zkusit ho uplatit",
                "success_next": "azkaban_2",
                "fail_fight": "Lucius Malfoy",
                "fail_next": "fight_result"
            },
            {
                "text": "Připravit se na duel",
                "fight": "Lucius Malfoy",
                "success_next": "azkaban_2"
            }
        ]
    },

    "azkaban_2": {
        "text": "Lucius zmizel v temnotě. Pokračuješ dál kobkami.",
        "next": "azkaban_relic"
    },

    "azkaban_relic": {
        "text": "Na dně jedné z kobek objevuješ Plášť neviditelnosti!",
        "relic": "Plášť neviditelnosti",
        "choices": [
            {"text": "Vrátit se do Bradavic", "next": "hub"}
        ]
    },

    "hub": {
        "text": "Jsi zpět v Bradavicích. Kam se vydáš dál?",
        "choices": [
            {"text": "Do Zakázaného lesa", "next": "forest_1"},
            {"text": "Do Bradavic", "next": "hogwarts_1"},
            {"text": "Do Azkabanu", "next": "azkaban_1"}
        ]
    },

    "fight_result": {
        "text": "Souboj skončil.",
        "choices": [
            {"text": "Pokračovat dál", "next": "hub"}
        ]
    },

    "final_battle": {
        "text": "Máš všechny tři relikvie. Voldemort se objevil a čeká tě poslední souboj!",
        "fight": "Voldemort",
        "win_text": "Porazil jsi Voldemorta a zachránil svět čar a kouzel!",
        "lose_text": "Voldemort tě porazil. Temnota ovládla svět..."
    }
}






RELICS_NEEDED = {
    "Zakázaný les": "Meč Godrika Nebelvíra",
    "Bradavice": "Kámen vzkříšení",
    "Azkaban": "Plášť neviditelnosti"
}

# Výchozí stav hry (state)
state = {
    "player": {
        "name": None,
        "character_id": None,
        "hp": 100,
        "max_hp": 100,
        "stamina": 100,           # 🔋 Aktuální stamina hráče
        "max_stamina": 100,       # 🔋 Maximální stamina
        "advantage": "",
        "disadvantage": "",
        "xp": 0,
        "level": 1,
        "unlocked_spells": {spell for spell in SPELLS if not SPELLS[spell].get("secret", False)},
        "shield": False,
        "dodge_next": False
    },
    "bot": {
        "name": None,
        "hp": 100,
        "max_hp": 100,
        "stamina": 100,           # 🔋 Aktuální stamina bota
        "max_stamina": 100,       # 🔋 Maximální stamina bota
        "advantage": "",
        "disadvantage": "",
        "shield": False,
        "dodge_next": False
    },
    "last_command_time": None,
    "mode_id": None
}


def ascii_effect(spell):
    effects = {
        "expelliarmus": """
**


                                                                                                      
-__ /\\                                ,,                |\       ,,                                  
  ||  \\   _                           ||                 \\      ||                 '        '       
 /||__||  < \, -_-_  ,._-_  _-_,  _-_  ||/\        /'\\  / \\ /\\ ||/|, ,._-_  /'\\ \\ \\ \\ \\  _-_  
 \||__||  /-|| || \\  ||   ||_.  || \\ ||_<       || || || ||  /  || ||  ||   || || || || || || || \\ 
  ||  |, (( || || ||  ||    ~ || ||/   || |       || || || || /\\ || |'  ||   || || || || || || ||/   
_-||-_/   \/\\ ||-'   \\,  ,-_-  \\,/  \\,\       \\,/   \\/   || \\/    \\,  \\,/  || \\/\\ || \\,/  
  ||           |/                                              /                    |;       |;       
               '                                              (,                    /        /        


**
""",
        "stupefy":  r"""
        ** 


    __                                                                                     
  ,-||-,                                                                                   
 ('|||  )                   _                                                    _    '  ' 
(( |||--)) \\/\\/\\ ,._-_  < \,  _-_  _-_  \\/\\        _-_  \\/\\  _-_  ,._-_  / \\ \\ \\ 
(( |||--)) || || ||  ||    /-|| ||   || \\ || ||       || \\ || || || \\  ||   || || || || 
 ( / |  )  || || ||  ||   (( || ||   ||/   || ||       ||/   || || ||/    ||   || || || || 
  -____-   \\ \\ \\  \\,   \/\\ \\,/ \\,/  \\ \\       \\,/  \\ \\ \\,/   \\,  \\_-| \\ \\ 
                                                                                /  \       
                                                                               '----`      


 **
        """,
        "sectumsempra":  r"""
        ** 


                                                                                                                                    
                                  ,,   ,,         ,  ,,                            ,,                         |\              ,,    
                        _         ||   ||        ||  ||      _                     ||     _         ;          \\             ||    
,._-_  _-_  /\\ \\/\\  < \,       ||/\ ||  _-_  =||= ||/|,  < \,        _-_,  _-_  ||/\  < \,       \\/\ /\\  / \\ \\ \\  _-_ ||/\\ 
 ||   || \\  /  || ||  /-||       ||_< || || \\  ||  || ||  /-||       ||_.  || \\ ||_<  /-||       || |  /  || || || || ||   || || 
 ||   ||/   /\\ || || (( ||       || | || ||/    ||  || |' (( ||        ~ || ||/   || | (( ||       || | /\\ || || || || ||   || || 
 \\,  \\,/   || \\ \\  \/\\       \\,\ \\ \\,/   \\, \\/    \/\\       ,-_-  \\,/  \\,\  \/\\       \\/   ||  \\/  \\/\\ \\,/ \\ |/ 
             /                                                                                            /                     _/  
            (,                                                                                           (,                         


 **
        """,
        "avada kedavra":  r"""
        ** 



                                                                                                                  
          ,,                                                              ,,                                ,     
          ||                                  _                           ||                               ||   ' 
/\\  _-_  ||  _-_  \\/\\ '\\/\\       -_-_   < \, -_-_  ,._-_  _-_,  _-_  ||/\        _-_, \\/\\/\\ ,._-_ =||= \\ 
 /  || \\ || || \\ || ||  || ;'       || \\  /-|| || \\  ||   ||_.  || \\ ||_<       ||_.  || || ||  ||    ||  || 
/\\ ||/   || ||/   || ||  ||/         || || (( || || ||  ||    ~ || ||/   || |        ~ || || || ||  ||    ||  || 
 || \\,/  \\ \\,/  \\ \\  |/          ||-'   \/\\ ||-'   \\,  ,-_-  \\,/  \\,\       ,-_-  \\ \\ \\  \\,   \\, \\ 
 /                       (            |/          |/                                                              
(,                        -_-         '           '                                                               


 **
        """,
        "protego":  r"""
        ** 



                                                                                       
        ,       ,          ,                    ,,                         ,,       /\ 
       ||   '  ||         ||                    ||            _          ' ||       \/ 
 _-_, =||= \\ =||=       =||=  _-_         /'\\ ||/|, ,._-_  < \, \\/\\ \\ ||       }{ 
||_.   ||  ||  ||         ||  || \\       || || || ||  ||    /-|| || || || ||       \/ 
 ~ ||  ||  ||  ||         ||  ||/         || || || |'  ||   (( || || || || ||          
,-_-   \\, \\  \\,        \\, \\,/        \\,/  \\/    \\,   \/\\ \\ \\ \\ \\       <> 
                                                                                       
                                                                                       


 **
        """,
        "protego maxima": r"""
        ** 



                                                                                                                                
      ,,                           ,,                                             ,,                        ,       ,        /\ 
      ||                ;          ||                           _     _    '      ||                       ||   '  ||        \/ 
 /'\\ ||/|, ,._-_  /'\\ \\/\  _-_, ||/\ '\\/\\       \\/\\/\\  < \,  / \\ \\  _-_ ||/\ '\\/\\        _-_, =||= \\ =||=       }{ 
|| || || ||  ||   || || || | ||_.  ||_<  || ;'       || || ||  /-|| || || || ||   ||_<  || ;'       ||_.   ||  ||  ||        \/ 
|| || || |'  ||   || || || |  ~ || || |  ||/         || || || (( || || || || ||   || |  ||/          ~ ||  ||  ||  ||           
\\,/  \\/    \\,  \\,/  \\/  ,-_-  \\,\  |/          \\ \\ \\  \/\\ \\_-| \\ \\,/ \\,\  |/          ,-_-   \\, \\  \\,       <> 
                                        (                            /  \              (                                        
                                         -_-                        '----`              -_-                                     


 **
        """,
        "incendio":  r"""
        ** 


                                                                                                                   
      ,,                                        ,,       ,,                          ,,          ,, ,,          /\ 
      ||   _                                    ||       ||      _                   ||          || ||          \/ 
-_-_  ||  < \, \\/\\/\\  _-_  \\/\\        _-_, ||  _-_  ||/\\  < \,       /\\       ||/\\ \\ \\ || ||/\ '\\/\\ }{ 
|| \\ ||  /-|| || || || || \\ || ||       ||_.  || || \\ || ||  /-||        /        || || || || || ||_<  || ;' \/ 
|| || || (( || || || || ||/   || ||        ~ || || ||/   || || (( ||       /\\       || || || || || || |  ||/      
||-'  \\  \/\\ \\ \\ \\ \\,/  \\ \\       ,-_-  \\ \\,/  \\ |/  \/\\        ||       \\ |/ \\/\\ \\ \\,\  |/    <> 
|/                                                         _/               /          _/                (         
'                                                                          (,                             -_-      

 

 **
        """,
        "expulso":  r"""
        ** 


                                                                                                
                  ,,                                   ,,               ,,                   /\ 
      ,           ||                       ;           ||               ||           '       \/ 
 _-_  \\ /` -_-_  ||  /'\\ /\\  _-_        \\/\ '\\/\\ ||/|, \\ \\  _-_ ||/\\ \\ \\ \\  _-_  }{ 
|| \\  \\   || \\ || || ||  /  || \\       || |  || ;' || || || || ||   || || || || || || \\ \/ 
||/    /\\  || || || || || /\\ ||/         || |  ||/   || |' || || ||   || || || || || ||/      
\\,/  /  \; ||-'  \\ \\,/   || \\,/        \\/   |/    \\/   \\/\\ \\,/ \\ |/ \\/\\ || \\,/  <> 
            |/              /                   (                         _/        |;          
            '              (,                    -_-                                /           



 **
        """,
        "reducto":  r"""
        ** 

 

                                                                                             
             |\              ,,                              ,,               ,,          /\ 
              \\             ||          '       ;           ||               ||          \/ 
,._-_  _-_   / \\ \\ \\  _-_ ||/\ \\/\\ \\       \\/\ '\\/\\ ||/|, \\ \\  _-_ ||/\\       }{ 
 ||   || \\ || || || || ||   ||_< || || ||       || |  || ;' || || || || ||   || ||       \/ 
 ||   ||/   || || || || ||   || | || || ||       || |  ||/   || |' || || ||   || ||          
 \\,  \\,/   \\/  \\/\\ \\,/ \\,\ \\ \\ \\       \\/   |/    \\/   \\/\\ \\,/ \\ |/       <> 
                                                      (                         _/           
                                                       -_-                                   


 **
        """,
        "rictusempra":  r"""
        ** 


                                                                                                   
  -_-/                   ,,                                  ,,                                 /\ 
 (_ /             '      ||                  _           _   ||                   '             \/ 
(_ --_  \\/\\/\\ \\  _-_ ||/\\       -_-_   < \, ,._-_  < \, || '\\/\\ /\\ \\ \\ \\  _-_        }{ 
  --_ ) || || || || ||   || ||       || \\  /-||  ||    /-|| ||  || ;'  /  || || || || \\       \/ 
 _/  )) || || || || ||   || ||       || || (( ||  ||   (( || ||  ||/   /\\ || || || ||/            
(_-_-   \\ \\ \\ \\ \\,/ \\ |/       ||-'   \/\\  \\,   \/\\ \\  |/     || \\/\\ || \\,/        <> 
                           _/        |/                         (       /        |;                
                                     '                           -_-   (,        /                 


 **
        """,
        "crucio":  r"""
        ** 

                                                                                                                                               
      _-_ _,,         ,,               ,                    ,,   ,,         ,  ,,                                      ,,                   /\ 
         -/  )        ||              ||          _         ||   ||        ||  ||      _               _           _   ||           '       \/ 
        ~||_<    /'\\ ||  _-_   _-_, =||= \\/\\  < \,       ||/\ ||  _-_  =||= ||/|,  < \,       /\\  < \,  _-_,  < \, ||/\\ \\ \\ \\  _-_  }{ 
         || \\  || || || || \\ ||_.   ||  || ||  /-||       ||_< || || \\  ||  || ||  /-||        /   /-|| ||_.   /-|| || || || || || || \\ \/ 
         ,/--|| || || || ||/    ~ ||  ||  || || (( ||       || | || ||/    ||  || |' (( ||       /\\ (( ||  ~ || (( || || || || || || ||/      
        _--_-'  \\,/  \\ \\,/  ,-_-   \\, \\ \\  \/\\       \\,\ \\ \\,/   \\, \\/    \/\\        ||  \/\\ ,-_-   \/\\ \\ |/ \\/\\ || \\,/  <> 
       (                                                                                          /                      _/        |;          
                                                                                                 (,                                /           

 **
        """,
        "illusion": "** 🌫️ Iluze zmátla nepřítele! **",
        "dark curse": "** 🌑 Temná kletba udeřila! **"
    }
    print(effects.get(spell, f"** {spell.capitalize()}! **"))

def dev_mode_menu():
    while True:
        print("\n🧪 Vývojářské nástroje:")
        print("1. 💥 Přidat 1000 XP")
        print("2. 📜 Odemknout všechna kouzla")
        print("3. 🔁 Teleport do příběhového módu")
        print("4. ❌ Deaktivovat vývojářský režim")
        print("5. 🔙 Zpět do hlavního menu")

        choice = input("Zvol možnost: ").strip()

        if choice == "1":
            global player_xp
            player_xp += 1000
            print("✅ Přidáno 1000 XP.")
        elif choice == "2":
            global unlocked_spells
            unlocked_spells = set(SPELLS.keys())
            print("✅ Všechna kouzla odemčena.")
        elif choice == "3":
            print("🌀 Teleportuji do příběhového módu...")
            start_story("Vývojář")  # nebo získej postavu od hráče
            break
        elif choice == "4":
            if os.path.exists("devmode.flag"):
                os.remove("devmode.flag")
                print("❌ Vývojářský režim deaktivován.")
            else:
                print("⚠️ Vývojářský režim už není aktivní.")
            break
        elif choice == "5":
            break
        else:
            print("❗ Neplatná volba.")

def enemy_say(state, event):
    enemy_name = state["bot"]["name"]
    if enemy_name in ENEMIES:
        quotes = ENEMIES[enemy_name].get("quotes", {})
        lines = quotes.get(event, [])
        if lines:
            chosen_line = random.choice(lines)
            print(f"⚡ {enemy_name} říká: \"{chosen_line}\"")

            base_path = "enemy_voices"
            idx = lines.index(chosen_line) + 1  # např. 1.mp3, 2.mp3...
            filename = f"{enemy_name}_{event}_{idx}.mp3"
            filepath = os.path.join(base_path, filename)
            if os.path.isfile(filepath):
                try:
                    playsound(filepath)
                except Exception as e:
                    print(f"🎧 Chyba při přehrávání: {e}")
            else:
                print(f"⚠️ Audio soubor nenalezen: {filepath}")

def apply_spell(caster, target, spell, caster_adv, caster_disadv, state, is_combo=False):
    from spell_combos import SPELL_COMBINATIONS
    

    # Inicializace flagů
    state.setdefault("flags", {})
    state["flags"].setdefault("dodge_next", False)
    state["flags"].setdefault("player_shield", False)
    state["flags"].setdefault("bot_shield", False)

    # Hláška nepřítele
    if caster == "bot" and not is_combo:
        enemy_say(state, "cast_spell")

    # ↓↓↓ rozdílné zpracování podle typu kouzla
    if not is_combo:
        spell = spell.strip().lower()
        if spell not in SPELLS:
            print("** Kouzlo neexistuje. **")
            return

        data = SPELLS[spell]
        chance = data['chance']
        power = data['power']
        effect = data["effect"]
        stamina_cost = data.get("stamina_cost", 0)

        # Práce se staminou
        current_stamina = state[caster].get("stamina", 100)
        max_stamina = state[caster].get("max_stamina", 100)

        if stamina_cost > 0 and current_stamina < stamina_cost:
            print("❌ Nemáš dostatek staminy k seslání tohoto kouzla!")
            return

        state[caster]["stamina"] = min(max_stamina, max(0, current_stamina - stamina_cost))
        print(f"🔋 {state[caster]['name']} má nyní {state[caster]['stamina']} staminy.")

        # Výhody a nevýhody
        if "Chance" in caster_adv or "success chance" in caster_adv.lower():
            chance += 0.1
        if "low accuracy" in caster_disadv.lower():
            chance -= 0.1
        if "high damage" in caster_adv.lower():
            power += 10
        if "low damage" in caster_disadv.lower():
            power -= 5

        if random.random() > chance:
            print(f"** Kouzlo {spell} se nepovedlo! **")
            return

        ascii_effect(spell)
    else:
        data = spell  # 'spell' je dict z kombinace
        power = data['power']
        effect = data['effect']
        stamina_cost = data.get("stamina_cost", 0)

        current_stamina = state[caster].get("stamina", 100)
        max_stamina = state[caster].get("max_stamina", 100)

        if stamina_cost > 0 and current_stamina < stamina_cost:
            print("❌ Nemáš dostatek staminy k seslání tohoto kouzla!")
            return

        state[caster]["stamina"] = min(max_stamina, max(0, current_stamina - stamina_cost))
        print(f"🔋 {state[caster]['name']} má nyní {state[caster]['stamina']} staminy.")

        if "ascii" in data:
            print(Fore.RED + data["ascii"] + Style.RESET_ALL)
        else:
            ascii_effect(effect)

    # Speciální efekty
    if effect == "dodge_next":
        if caster == "player":
            state["flags"]["dodge_next"] = True
            print("🌀 Iluze připravena, příští útok tě mine!")
        return

    if effect in ["shield", "big_shield"]:
        if caster == "player":
            state["flags"]["player_shield"] = True
            print("🛡️ Aktivoval jsi štít!")
        else:
            state["flags"]["bot_shield"] = True
            print("🛡️ Nepřítel si aktivoval štít!")
        return

    if effect == "instant_kill":
        if random.random() < 0.15:
            if target == "bot":
                state["bot"]["hp"] = 0
                print("💀 Smrtící kouzlo zasáhlo nepřítele!")
            else:
                state["player"]["hp"] = 0
                print("💀 Byl jsi zasažen smrtícím kouzlem!")
            return
        else:
            print("❌ Smrtící kouzlo selhalo!")
            return

    if effect == "reflect":
        print("🔁 Reflexní štít připraven – příští útok se vrátí zpět!")
        if caster == "player":
            state["flags"]["player_shield"] = "reflect"
        else:
            state["flags"]["bot_shield"] = "reflect"
        return

    if effect == "fake_kill":
        print("💀 Iluze smrti! Nepřítel je zmatený a na jedno kolo neútočí!")
        state["flags"]["bot_stunned"] = True
        return

    # --- Zranění ---
    if target == "player":
        if state["flags"].get("dodge_next", False):
            print("✅ Kouzlo tě netrefilo díky iluzi!")
            state["flags"]["dodge_next"] = False
            return

        # QTE – hráč může kouzlo zablokovat
        if power > 0 and state["flags"].get("player_shield") not in [True, "reflect"]:
            if quick_time_event(key="s", time_limit=3.0):
                print("🛡️ Kouzlo bylo úspěšně zablokováno včasnou reakcí!")
                return

        if state["flags"].get("player_shield") == "reflect":
            print("🔁 Odrazil jsi kouzlo zpět na nepřítele!")
            apply_spell("bot", "bot", spell, "", "", state, is_combo)
            state["flags"]["player_shield"] = False
            return
        elif state["flags"].get("player_shield", False):
            print("🛡️ Odrazil jsi kouzlo pomocí štítu!")
            state["flags"]["player_shield"] = False
            return

        state["player"]["hp"] -= power
        print(f"💥 {state['player']['name']} ztrácí {power} HP!")

    elif target == "bot":
        if state["flags"].get("bot_shield") == "reflect":
            print("🔁 Nepřítel odrazil kouzlo zpět na tebe!")
            apply_spell("player", "player", spell, "", "", state, is_combo)
            state["flags"]["bot_shield"] = False
            return
        elif state["flags"].get("bot_shield", False):
            print("🛡️ Nepřítel zablokoval tvé kouzlo štítem!")
            state["flags"]["bot_shield"] = False
            return

        state["bot"]["hp"] -= power
        print(f"💥 {state['bot']['name']} ztrácí {power} HP!")







from spell_combos import SPELL_COMBINATIONS  # nezapomeň mít spell_combos.py


def fight(state, enemy_name, auto_mode=False):
    enemy_data = ENEMIES[enemy_name]
    state["bot"]["name"] = enemy_name
    state["bot"]["hp"] = enemy_data['hp']
    state["bot"]["max_hp"] = enemy_data['hp']
    state["bot"]["advantage"] = enemy_data['advantage']
    state["bot"]["disadvantage"] = enemy_data['disadvantage']
    state["bot"]["shield"] = False
    state["bot"]["stamina"] = 100
    state["bot"]["max_stamina"] = 100

    print(f"\n🧛 Narazil jsi na {enemy_name}!")
    print(f"Výhoda: {state['bot']['advantage']} | Nevýhoda: {state['bot']['disadvantage']}")

    last_command_time = time.time()
    last_player_spell = None

    while state["player"]["hp"] > 0 and state["bot"]["hp"] > 0:
        # Výpis zdraví a staminy
        print(draw_health_bar(state["player"]["hp"], state["player"]["max_hp"], is_player=True, name=state["player"]["name"]))
        print(draw_stamina_bar(state["player"]["stamina"], state["player"]["max_stamina"], is_player=True, name=state["player"]["name"]))
        
        print(draw_health_bar(state["bot"]["hp"], state["bot"]["max_hp"], is_player=False, name=enemy_name))
        print(draw_stamina_bar(state["bot"]["stamina"], state["bot"]["max_stamina"], is_player=False, name=enemy_name))

        print(draw_spells(state["player"]["unlocked_spells"], SPELLS))

        if not auto_mode:
            last_command_time = anticheat.detect_speedrun(last_command_time)

        if auto_mode:
            available_spells = [
                s for s in state["player"]["unlocked_spells"]
                if SPELLS[s].get("stamina_cost", 0) <= state["player"]["stamina"]
            ]
            if not available_spells:
                print("😵 Nemáš dost staminy na žádné kouzlo! Kolo přeskočeno.")
                state["player"]["stamina"] = min(state["player"]["max_stamina"], state["player"]["stamina"] + 10)
                continue
            chosen = random.choice(available_spells)
            print(f"\n(auto) Sesíláš kouzlo: {chosen}")
        else:
            chosen = input("\nNapiš kouzlo: ").lower()

        if not auto_mode and not anticheat.validate_command(chosen, SPELLS.keys()):
            continue
        if SPELLS[chosen].get("secret") and chosen not in state["player"]["unlocked_spells"]:
            print("** Toto kouzlo neznáš nebo neexistuje! **")
            continue

        # Kombinace
        if last_player_spell and (last_player_spell, chosen) in SPELL_COMBINATIONS:
            combo = SPELL_COMBINATIONS[(last_player_spell, chosen)]
            print(f"\n🔥 Kouzelná kombinace: {combo['name']}!")
            print(f"👉 {combo['description']}")
            apply_spell("player", "bot", combo, state["player"]["advantage"], state["player"]["disadvantage"], state, is_combo=True)
            last_player_spell = None
        else:
            apply_spell("player", "bot", chosen, state["player"]["advantage"], state["player"]["disadvantage"], state)
            last_player_spell = chosen

            if state["bot"]["hp"] <= 0:
                print(f"\n🎉 Porazil jsi {enemy_name}!")
                xp_gain = 50
                state["player"]["xp"] += xp_gain
                print(f"Získal jsi {xp_gain} XP!")

                if state["player"]["xp"] >= 100:
                    state["player"]["level"] += 1
                    state["player"]["xp"] -= 100
                    state["player"]["max_hp"] += 20
                    state["player"]["hp"] = state["player"]["max_hp"]
                    print(f"⬆️ Level UP! Úroveň {state['player']['level']}, HP: {state['player']['max_hp']}")
                    if state["player"]["level"] >= 2:
                        state["player"]["unlocked_spells"].add("illusion")
                    if state["player"]["level"] >= 3:
                        state["player"]["unlocked_spells"].add("dark curse")

                # 🧠 Uložit statistiky – výhra
                stats = load_stats()
                stats["wins"] += 1
                stats["total_matches"] += 1
                stats["max_level"] = max(stats["max_level"], state["player"]["level"])
                stats["total_xp"] += xp_gain
                stats["defeated_enemies"] += 1
                save_stats(stats)

                return True  # Ukončí fight po výhře

        print("\n--- Nepřítel sesílá kouzlo! ---")
        enemy_spell = random.choice(list(state["player"]["unlocked_spells"]))
        time.sleep(1)
        print(f"{enemy_name} sesílá: {enemy_spell}")
        apply_spell("bot", "player", enemy_spell, state["bot"]["advantage"], state["bot"]["disadvantage"], state)

        for who in ["player", "bot"]:
            state[who]["stamina"] = min(
                state[who]["max_stamina"],
                state[who]["stamina"] + 1
            )

    # 🧠 Uložit statistiky – prohra
    stats = load_stats()
    stats["losses"] += 1
    stats["total_matches"] += 1
    stats["max_level"] = max(stats["max_level"], state["player"]["level"])
    stats["total_xp"] += state["player"]["xp"]
    save_stats(stats)

    return False





def main_menu():
    # 🛡️ AntiCheat spouštění
    anticheat.detect_multi_file_modifications()
    anticheat.check_stats_integrity("wizard_duel_stats.txt")
    anticheat.check_stats_file()

    if os.path.exists("devmode.flag"):
        print("🛠️ Vývojářský režim aktivní.")
        return "dev"

    while True:
        ui.draw_main_menu()  # Zobrazí hlavní menu
        choice = input("\nZvol možnost (1-4): ").strip()

        if choice == "1":
            return "play"
        elif choice == "2":
            dev_input = input("Zadej kód: ").strip()
            if dev_input == "tournament OtzRWexD":
                with open("devmode.flag", "w") as f:
                    f.write("enabled")
                print("✅ Vývojářský režim aktivován.")
                return "dev"
            else:
                print("❌ Neplatný kód.")
        elif choice == "3":
            print("👋 Ukončuji hru.")
            exit()
        elif choice == "4":
            zobraz_statistiky()  # Zavolání funkce pro zobrazení statistik
        else:
            print("❗ Neplatná volba.")

# Funkce pro zobrazení statistik
def zobraz_statistiky():
    stats = load_stats()
    print("\n" + "="*30)
    print("📊 STATISTIKY HRÁČE".center(30))
    print("="*30)
    print(f"🏆 Výhry:               {stats['wins']}")
    print(f"💀 Prohry:              {stats['losses']}")
    print(f"🧙 Celkový počet zápasů: {stats['total_matches']}")
    print(f"📈 Max. dosažený level:  {stats['max_level']}")
    print(f"✨ Celkové XP:           {stats['total_xp']}")
    print(f"⚔️  Poražených nepřátel: {stats['defeated_enemies']}")
    print("="*30 + "\n")
    input("Stiskni Enter pro návrat do menu...")  # Po zobrazení statistik čekáme na Enter pro návrat zpět


play_background_music()
import time

def start_survival(state):
    wave = 1

    while state["player_hp"] > 0:
        print(f"\n🌊 Vlna #{wave}")
        if ENEMIES:
            enemy_name = random.choice(list(ENEMIES.keys()))
            if not fight(state, enemy_name):
                print(f"\n💀 Byl jsi poražen ve vlně {wave}.")
                state["losses"] += 1
                break
        else:
            print("❌ No enemies available for survival.")
            sys.exit()
        wave += 1

    if state["player_hp"] > 0:
        state["wins"] += wave - 1


def start_story(state):
    relics = []
    current_node = "intro"

    while current_node:
        node = STORY[current_node]

        if set(relics) == set(RELICS_NEEDED.values()) and current_node != "final_battle":
            current_node = "final_battle"
            continue

        print(draw_boxed_text(node["text"], Fore.YELLOW))

        if current_node == "final_battle" and "fight" in node:
            print("⚔️ Vyvolávám závěrečný souboj...")
            print(draw_spells(state["spells"], SPELL_DATA))
            if fight(state, node["fight"]):
                print(draw_boxed_text(node["win_text"], Fore.CYAN))
                state["wins"] += 1
            else:
                print(draw_boxed_text(node["lose_text"], Fore.RED))
                state["losses"] += 1
            break

        if "choices" in node:
            print(draw_boxed_text("\n📌 Možnosti:", Fore.CYAN))
            for i, choice in enumerate(node["choices"]):
                print(f"{i + 1}. {draw_boxed_text(choice['text'], Fore.MAGENTA)}")

            selected = None
            while selected is None:
                try:
                    idx = int(input("➡️ Tvá volba: ")) - 1
                    if 0 <= idx < len(node["choices"]):
                        selected = node["choices"][idx]
                except ValueError:
                    pass

            if "fail_fight" in selected:
                print(f"⚔️ Souboj s: {selected['fail_fight']} (v důsledku neúspěchu)")
                print(draw_spells(state["spells"], SPELL_DATA))
                if not fight(state, selected["fail_fight"]):
                    print(draw_boxed_text(f"\n💀 Byl jsi poražen nepřítelem {selected['fail_fight']}.", Fore.RED))
                    state["losses"] += 1
                    break
                else:
                    print(draw_boxed_text(f"💥 Přežil jsi nepříznivou volbu!", Fore.CYAN))
                    state["wins"] += 1
                    if "relic" in selected and selected["relic"] not in relics:
                        relics.append(selected["relic"])
                        print(draw_boxed_text(f"🏆 Získal jsi relikvii: {selected['relic']}!", Fore.GREEN))
                    current_node = selected.get("success_next", None)

            elif "fight" in selected:
                print(f"⚔️ Souboj s: {selected['fight']}")
                print(draw_spells(state["player"]["unlocked_spells"], SPELLS))
                if fight(state, selected["fight"]):
                    print(draw_boxed_text(f"💥 Souboj s {selected['fight']} vyhrán!", Fore.CYAN))
                    state["wins"] += 1
                    if "relic" in selected and selected["relic"] not in relics:
                        relics.append(selected["relic"])
                        print(draw_boxed_text(f"🏆 Získal jsi relikvii: {selected['relic']}!", Fore.GREEN))
                    current_node = selected.get("success_next", None)
                else:
                    print(draw_boxed_text(f"\n💀 Byl jsi poražen nepřítelem {selected['fight']}.", Fore.RED))
                    state["losses"] += 1
                    break

            elif "success_next" in selected:
                if "relic" in selected and selected["relic"] not in relics:
                    relics.append(selected["relic"])
                    print(draw_boxed_text(f"🏆 Získal jsi relikvii: {selected['relic']}!", Fore.GREEN))
                current_node = selected["success_next"]

            else:
                current_node = selected.get("next", None)

        else:
            if "relic" in node and node["relic"] not in relics:
                relics.append(node["relic"])
                print(draw_boxed_text(f"🏆 Získal jsi relikvii: {node['relic']}!", Fore.GREEN))
            current_node = node.get("next", None)

    print(draw_boxed_text("\n📚 Příběhový mód ukončen.", Fore.YELLOW))


def main():
    global mode_id, character_id
    while True:  # Smysl je mít nekonečnou smyčku pro opakovaný návrat do menu
        choice = main_menu()  # Zobrazení hlavního menu a výběr možnosti

        if choice == "dev":
            print("🛠️ Spouštím vývojářský režim...")
            print("\n🧪 Vývojářský výběr:")
            for cid, cdata in CHARACTERS.items():
                print(f"{cid}. {cdata['name']}")
            character_id = int(input("Zadej ID postavy: "))
            mode_id = int(input("Zadej mód (1=duel, 2=survival, 3=příběh): "))
        elif choice == "play":
            character_id, mode_id = ui.start_ui()  # Tady by mělo přijít UI pro výběr postavy a módu
        else:
            print("Hra ukončena.")
            return

        if mode_id is None or character_id is None:
            print("❌ Chyba při výběru módu nebo postavy.")
            continue  # V případě chyby se znovu vrátí do hlavního menu

        character_data = CHARACTERS.get(character_id)
        if not character_data:
            print("❌ Neznámá postava.")
            continue  # V případě neznámé postavy se vrátí zpět do menu

        # 🧠 Inicializace stavu podle postavy
        state["player"]["name"] = character_data["name"]
        state["player"]["character_id"] = character_id
        state["player"]["hp"] = character_data["hp"]
        state["player"]["max_hp"] = character_data["hp"]
        state["player"]["advantage"] = character_data.get("advantage", "")
        state["player"]["disadvantage"] = character_data.get("disadvantage", "")
        state["player"]["unlocked_spells"] = set(character_data["spells"])
        state["player"]["shield"] = False
        state["player"]["dodge_next"] = False

        # 🎁 Bonus – zpětně kompatibilní proměnné
        state["player_name"] = state["player"]["name"]
        state["player_hp"] = state["player"]["hp"]
        state["player_max_hp"] = state["player"]["max_hp"]
        state["player_spells"] = character_data["spells"]

        print(f"Vybraná postava: {state['player_name']}")

        # Spuštění herního módu
        if mode_id == 1:  # Duel mód
            if ENEMIES:
                state.setdefault("wins", 0)
                state.setdefault("losses", 0)

                enemy_name = random.choice(list(ENEMIES.keys()))
                print(f"⚔️ Zahajuji souboj s postavou: {enemy_name}")

                # Spuštění souboje
                if fight(state, enemy_name):
                    state["wins"] += 1
                else:
                    state["losses"] += 1
            else:
                print("❌ Žádní nepřátelé nejsou k dispozici pro duel.")
                time.sleep(2)

        elif mode_id == 2:  # Survival mód
            start_survival(state)
        elif mode_id == 3:  # Příběhový mód
            start_story(state)
        else:
            print("❌ Neplatný mód.")
            continue  # Pokud je mód neplatný, vracíme zpět do menu

        # Po dokončení módu vrátíme zpět do hlavního menu
        print("\n✔️ Mód skončil. Vracíme se do hlavního menu...")
        time.sleep(2)  # Krátká pauza před návratem zpět do menu


# Hlavní smyčka hry
if __name__ == "__main__":
    main()











def battle_choice(state, story_step):
    """
    Zkontroluje, jestli je v příběhu volba souboje, a pokud ano, spustí souboj.
    """
    if "fight" in story_step:
        enemy_name = story_step["fight"]
        result = fight(state, enemy_name)  # Zavoláme soubojovou funkci
        if result:
            print(f"\n🎉 Porazil jsi {enemy_name}!")
            return {"success": True, "next": story_step.get("next", "hub")}
        else:
            print("\n💀 Bylo ti smutně. Zkus to znovu!")
            return {"success": False, "next": "game_over"}  # Předpokládaná obrazovka pro konec hry

    return {"success": True, "next": story_step["next"]}  # Pokračuj v příběhu, pokud není souboj



def handle_choice(state, story_step):
    """
    Zpracuje volby hráče a umožní pokračování příběhu na základě volby.
    """
    print(story_step["text"])  # Vytiskne text aktuálního kroku příběhu
    for i, choice in enumerate(story_step["choices"]):
        print(f"{i + 1}. {choice['text']}")

    try:
        choice = int(input("\nVyber možnost (1, 2, 3...): ")) - 1
        if choice < 0 or choice >= len(story_step["choices"]):
            print("Neplatná volba. Zkus to znovu.")
            return handle_choice(state, story_step)  # Znovu vyžádej volbu
    except ValueError:
        print("Neplatný vstup. Zkus to znovu.")
        return handle_choice(state, story_step)

    selected_choice = story_step["choices"][choice]
    next_step = selected_choice.get("next", None)

    # Zpracování souboje (pokud je součástí volby)
    result = battle_choice(state, selected_choice)
    
    if result["success"]:
        # Pokračuje příběh do následujícího kroku
        next_step_data = STORY[next_step]
        handle_choice(state, next_step_data)
    else:
        # Pokud je prohra, ukončíme hru nebo opakujeme
        print("Hra skončila... Zkus to znovu!")


def game_over():
    print("Hra skončila. Chceš začít znovu? (ano/ne)")
    choice = input().lower()
    if choice == "ano":
        start_game()  # Začátek hry znovu
    else:
        print("Děkujeme za hraní!")
        exit()

# ------------------ 🧪 FUNKCE DUELU ------------------

from spell_combos import SPELL_COMBINATIONS  # nezapomeň mít spell_combos.py






# Ujistíme se, že mode_id bude vždy definováno
if mode_id is None:
    print("❌ Neplatný mód. Ukončuji hru.")
    sys.exit()  # Ukončí celý program, pokud mode_id není definováno.

# Načteme statistiky
wins, losses = load_stats()

# Spuštění konkrétního módu podle mode_id
# Ověření, že character_id je platné a data existují
character_data = CHARACTERS.get(character_id)
if not character_data:
    print(f"❌ Neplatné ID postavy: {character_id}")
    sys.exit()

# Inicializace hráče do stavu
#state["player_name"] = character_data["name"]
#state["player_hp"] = character_data["hp"]
#state["player_max_hp"] = character_data["hp"]
#state["player_spells"] = character_data["spells"]
#state.setdefault("wins", 0)
#state.setdefault("losses", 0)

# Tento blok kódu již neprovádí žádný výpis do konzole.

# --- Herní módy ---

# --- Herní módy ---
if mode_id == 1:  # Duel mód
    if ENEMIES:
        state.setdefault("wins", 0)
        state.setdefault("losses", 0)

        enemy_name = random.choice(list(ENEMIES.keys()))
        print(f"⚔️ Zahajuji souboj s postavou: {enemy_name}")

        if fight(state, enemy_name):
            state["wins"] += 1
        else:
            state["losses"] += 1
    else:
        print("❌ Žádní nepřátelé nejsou k dispozici pro duel.")
        time.sleep(2)

    print("✔️ Mód skončil. Vracíme se do hlavního menu...")
    time.sleep(2)
    main_menu(state)  # místo return












# ------------------ 📊 STATISTIKY ------------------
# Načíst aktuální statistiky
# Načítání statistik na začátku hry
stats = load_stats()

# Kód zápasu...
if state["player"]["hp"] > 0:
    stats["wins"] += 1
else:
    stats["losses"] += 1

# Zvyšení celkového počtu zápasů
stats["total_matches"] += 1

# Zaznamenání maximálního levelu hráče
stats["max_level"] = max(stats["max_level"], state["player"]["level"])

# Přidání celkových zkušeností
stats["total_xp"] += state["player"]["xp"]

# Zaznamenání poraženého nepřítele
stats["defeated_enemies"] += 1

# Uložení aktualizovaných statistik
save_stats(stats)

# Výpis statistik
print(f"\n📊 Statistiky:")
print(f"Výhry: {stats['wins']}")
print(f"Prohry: {stats['losses']}")
print(f"Celkový počet zápasů: {stats['total_matches']}")
print(f"Maximální dosažený level: {stats['max_level']}")
print(f"Celkové XP: {stats['total_xp']}")
print(f"Poražených nepřátel: {stats['defeated_enemies']}")
