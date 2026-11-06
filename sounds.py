import os
import sys
import threading
import pygame

# Bezpečná cesta i pro .exe
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath("."))

# Přehrávání hudby na pozadí
def play_background_music(file_name="background.mp3"):
    def loop_music():
        pygame.mixer.init()
        path = os.path.join(BASE_DIR, file_name)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.3)  # Nastaví hlasitost na 30 %
        pygame.mixer.music.play(-1)  # -1 = smyčka

    threading.Thread(target=loop_music, daemon=True).start()


# Zvukový efekt (např. zásah kouzlem)
def play_sound_effect(file_name):
    path = os.path.join(BASE_DIR, file_name)
    pygame.mixer.Sound(path).play()


# Funkce pro přehrání zvuku zásahu kouzlem
def play_spell_hit_sound():
    playsound("spell_hit_sound.mp3")  # Cesta k souboru se zvukem

# Funkce pro speciální zvuk Avada Kedavra
def play_avada_kedavra_sound():
    playsound("avada_kedavra_sound.mp3")  # Cesta k souboru se zvukem

# Funkce pro přehrání zvuku při kliknutí v menu
def play_menu_sound():
    playsound("menu_click_sound.mp3")  # Cesta k souboru se zvukem
