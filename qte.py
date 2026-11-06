from colorama import Fore, Style
import threading
import time
import keyboard
from decimal import Decimal, ROUND_DOWN

def quick_time_event(key="s", time_limit=3.0):
    """
    Spustí QTE výzvu – hráč musí stisknout správnou klávesu v časovém limitu.
    Vrací True pokud se to povedlo, jinak False.
    """

    # Přesný formát bez zaokrouhlení nahoru
    time_str = str(Decimal(time_limit).quantize(Decimal("0.1"), rounding=ROUND_DOWN))

    print("\n" + "=" * 60)
    print(f"{Fore.RED}{Style.BRIGHT}⚡  POZOR! NEPŘÍTEL SESLAL KOUZLO! ⚡{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}🎯  Stiskni klávesu '{key.upper()}' během {time_str} sekundy!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}🛡️  ABYS BLOKNUL ÚTOK A NEUTRPĚL ZRANĚNÍ!{Style.RESET_ALL}")
    print("=" * 60 + "\n")

    result = {"success": False}

    def wait_for_key():
        end_time = time.time() + time_limit
        while time.time() < end_time:
            if keyboard.is_pressed(key):
                result["success"] = True
                break
            time.sleep(0.01)

    thread = threading.Thread(target=wait_for_key, daemon=True)
    thread.start()
    thread.join(timeout=time_limit)

    if result["success"]:
        print(f"{Fore.GREEN}✅  Úspěšně jsi zablokoval útok!{Style.RESET_ALL}\n")
        return True
    else:
        print(f"{Fore.RED}❌  Nezareagoval jsi včas – byl jsi zasažen!{Style.RESET_ALL}\n")
        return False

