import os
import time
import hashlib
import sys

# Hashy originálních souborů – bez stats
ORIGINAL_HASHES = {
    "5.py": "1eae6d0a0480521c3e2349ab3d259905c76d5842c81336c7c25a43fd15de7b00",
    "game_ui.py": "5163378f91da9db3eda351793717f203e42169c19ac1b64ed1b10db867fb24ae"
    # "wizard_duel_stats.txt": "..." odstraněno
}

LOG_FILE = "anticheat.log"
STATS_FILE = "wizard_duel_stats.txt"

def is_frozen():
    return getattr(sys, 'frozen', False)

# --- Pomocné funkce ---
def hash_file(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        print(f"❌ AntiCheat: Soubor {path} nenalezen.")
        log_cheat(f"Soubor nenalezen: {path}")
        sys.exit()

def log_cheat(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"[{time.ctime()}] {message}\n")

def detect_file_modifications(script_paths):
    if is_frozen():
        return  # V exe režimu nekontrolujeme fyzické soubory

    if isinstance(script_paths, str):
        script_paths = [script_paths]

    for path in script_paths:
        current_hash = hash_file(path)
        name = os.path.basename(path)

        if name not in ORIGINAL_HASHES:
            print(f"⚠️ AntiCheat: Neznámý soubor {name}!")
            time.sleep(1)
            sys.exit()

        if current_hash != ORIGINAL_HASHES[name]:
            print(f"⚠️ AntiCheat: {name} byl změněn! Ukončuji...")
            log_cheat(f"Změna souboru: {name}")
            time.sleep(2)
            sys.exit()

def detect_multi_file_modifications():
    if is_frozen():
        return
    for filename in ORIGINAL_HASHES.keys():
        detect_file_modifications(filename)

# --- Speedrun detekce ---
speedrun_strikes = 0
start_time = time.time()

def detect_speedrun(last_command_time, min_interval=0.3, max_strikes=3):
    global speedrun_strikes, start_time
    now = time.time()

    if now - start_time < 20:
        return now

    if last_command_time == 0:
        return now

    if now - last_command_time < min_interval:
        speedrun_strikes += 1
        if speedrun_strikes >= max_strikes:
            print("⚠️ AntiCheat: Opakované příliš rychlé zadávání příkazů!")
            log_cheat("Opakované rychlé příkazy (speedrun cheat)")
            time.sleep(2)
            sys.exit()
        else:
            print(f"⚠️ Upozornění: Příkaz byl zadán příliš rychle ({speedrun_strikes}/{max_strikes})")
    else:
        speedrun_strikes = 0

    return now

# --- Validace příkazů ---
def validate_command(cmd, allowed_commands):
    if cmd not in allowed_commands:
        print("⚠️ AntiCheat: Zakázaný příkaz!")
        log_cheat(f"Neplatný příkaz: {cmd}")
        time.sleep(1)
        return False
    return True

# --- Tyto dvě funkce nyní nejsou používané ---
def check_stats_integrity(stats_file):
    pass  # zakázáno

def check_stats_file():
    pass  # zakázáno



