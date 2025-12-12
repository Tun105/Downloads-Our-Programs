import os
import platform
import socket
import time
import requests
import sys
import random
from datetime import datetime
from colorama import Fore, Style, init

# Initialise colorama et configure l'auto-reset.
# NOTE: Cette fonction tente d'assurer la compatibilité des couleurs ANSI, 
# mais leur affichage correct dépend toujours du terminal utilisé.
init(autoreset=True)

# ---------------------------
# CONFIGURATION DES COULEURS ET DONNÉES
# ---------------------------

# Couleurs pour le Mode Standard (Réseau & Système)
MAIN_COLOR = Fore.BLUE 
# Couleur pour le Sous-Menu Launcher et les options "spéciales"
LAUNCHER_COLOR = Fore.RED 
# Couleur pour les messages d'erreur/avertissements
WARNING_COLOR = Fore.YELLOW
# Couleur pour le succès/l'accès
SUCCESS_COLOR = Fore.GREEN
WHITE_COLOR = Fore.WHITE 

# CODE PIN SECRET pour le démarrage
SECRET_PIN = "319>"
MAX_ATTEMPTS = 3

# 12 applications de lancement rapide (pour le sous-menu Admin)
QUICK_LAUNCH_ITEMS = {
    '1': ('💨 Launch Steam', 'steam://open/main'),
    '2': ('💎 Launch Epic Games Launcher', 'com.epicgames.launcher://'),
    '3': ('🎧 Launch Discord', 'discord://'),
    '4': ('💜 Launch Twitch', 'https://www.twitch.tv/'),
    '5': ('📺 Launch YouTube', 'https://www.youtube.com/'),
    '6': ('🕹️ Launch Roblox', 'roblox://'),
    '7': ('🤖 Launch ChatGPT (Web)', 'https://chat.openai.com/'),
    '8': ('📦 Launch Microsoft Store', 'ms-windows-store:'),
    '9': ('⚙️ Launch Windows Settings', 'ms-settings:'),
    '10': ('🗺️️ Launch Maps', 'bingmaps:'),
    '11': ('📧 Launch Email App', 'mailto:'),
    '12': ('🧮 Launch Calculator', 'calculator:'),
}

# ---------------------------
# Helpers
# ---------------------------

def clear_console():
    """Efface la console (compatible Windows et Unix)."""
    os.system("cls" if os.name == "nt" else "clear")

def print_color(text, color=MAIN_COLOR, delay=0.00):
    """Affiche du texte avec une couleur et un délai (style 'Matrix')."""
    text = str(text)
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        if delay:
            time.sleep(delay)
    print(Style.RESET_ALL)

def get_prompt(text, color=MAIN_COLOR):
    """Formate le texte de l'invite de commande avec la couleur appropriée."""
    return color + text + Style.RESET_ALL

def user_input(prompt_text, color=MAIN_COLOR):
    """Prend une entrée utilisateur."""
    sys.stdout.write(get_prompt(prompt_text, color))
    sys.stdout.flush()
    
    # L'entrée utilisateur est affichée en blanc
    sys.stdout.write(Fore.WHITE)
    val = sys.stdin.readline().strip()
    sys.stdout.write(Style.RESET_ALL)
    
    if val.lower() == "menu":
        raise KeyboardInterrupt
    return val

# ---------------------------
# Fonctions de SÉCURITÉ
# ---------------------------

def lock_screen():
    """Demande le code PIN (319>) avant de lancer la boucle principale."""
    clear_console()
    color = MAIN_COLOR # Utilise la couleur principale (Bleu) pour l'écran de verrouillage
    
    # BANNIÈRE DE VERROUILLAGE SIMPLE
    print_color("==========================================================================", color)
    print_color("          🔒 T U N LAUNCHER VERROUILLÉ 🔒                                ", color)
    print_color("==========================================================================", color)
    print_color("\n")
    
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            # Utilisation de input() pour assurer la compatibilité
            pin = input(get_prompt(f"Entrez le PIN ({MAX_ATTEMPTS - attempts} tentatives restantes) > ", color=WHITE_COLOR)).strip()
        except EOFError:
            pin = "" # Évite les erreurs si l'entrée est fermée
        except KeyboardInterrupt:
            print_color("\nFermeture.", Fore.RED)
            return False

        if pin == SECRET_PIN:
            print_color(f"\n✅ Accès Accordé ! Démarrage du système...", SUCCESS_COLOR)
            time.sleep(1)
            return True # Succès
        else:
            attempts += 1
            remaining = MAX_ATTEMPTS - attempts
            print_color(f"❌ PIN incorrect. {remaining} tentatives restantes.", Fore.RED)
            time.sleep(0.5)
            
    # Échec après le nombre maximal de tentatives
    clear_console()
    print_color("🔒 [LAUNCHER VERROUILLÉ] Trop de tentatives échouées. Fermeture.", Fore.RED)
    time.sleep(3)
    return False # Échec

# ---------------------------
# Fonctions outils (Couleur BLEUE)
# ---------------------------
# NOTE: Ces fonctions utilisent implicitement MAIN_COLOR (BLEU)

def ping_host():
    """Effectue un ping vers une adresse IP ou un hôte."""
    try:
        target = user_input("Hôte ou IP à pinguer : ")
    except KeyboardInterrupt: return
    if not target: print_color("❌ Cible vide.", Fore.RED); time.sleep(1); return
    count = 4
    print_color(f"\n--- Ping {target} ({count} paquets) ---\n", MAIN_COLOR)
    param = "-n" if platform.system().lower() == "windows" else "-c"
    os.system(f"ping {param} {count} {target}")
    input(get_prompt("\nAppuie sur Entrée pour revenir au menu..."))

def ip_lookup():
    """Recherche des informations géolocalisées pour une adresse IP donnée."""
    try:
        ip = user_input("Adresse IP à rechercher : ")
    except KeyboardInterrupt: return
    if not ip: print_color("❌ IP vide.", Fore.RED); time.sleep(1); return
    print_color(f"\nRecherche d'informations sur {ip}...\n", MAIN_COLOR)
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=8).json()
        if response.get("status") == "success":
            print_color(f"📍 Pays : {response.get('country')}", MAIN_COLOR)
            print_color(f"🗺️ Région : {response.get('regionName')}", MAIN_COLOR)
            print_color(f"🏙️ Ville : {response.get('city')}", MAIN_COLOR)
            print_color(f"📡 Fournisseur : {response.get('isp')}", MAIN_COLOR)
            print_color(f"🧭 Lat/Lon : {response.get('lat')} / {response.get('lon')}", MAIN_COLOR)
        else:
            print_color(f"❌ IP introuvable : {response.get('message', 'Erreur inconnue')}", Fore.RED)
    except Exception as e:
        print_color(f"⚠️ Erreur de connexion ou d'API : {e}", Fore.RED)
    input(get_prompt("\nAppuie sur Entrée pour revenir au menu..."))

def get_ip_address():
    """Affiche le nom d'hôte et l'adresse IP locale de l'appareil."""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print_color(f"\n💻 Nom de l'appareil : {hostname}", MAIN_COLOR)
        print_color(f"🌐 Adresse IP locale : {ip_address}", MAIN_COLOR)
    except Exception as e:
        print_color(f"⚠️ Erreur lors de la récupération de l'IP : {e}", Fore.RED)
    input(get_prompt("\nAppuie sur Entrée pour revenir au menu..."))

def system_info():
    """Affiche des informations basiques sur le système d'exploitation."""
    print_color("\n--- Informations système ---\n", MAIN_COLOR)
    print_color(f"⚙️ Système : {platform.system()}", MAIN_COLOR)
    print_color(f"🔢 Version : {platform.version()}", MAIN_COLOR)
    print_color(f"🏗️ Architecture : {platform.architecture()[0]}", MAIN_COLOR)
    print_color(f"🧠 Machine : {platform.machine()}", MAIN_COLOR)
    print_color(f"⏰ Date et heure : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", MAIN_COLOR)
    input(get_prompt("\nAppuie sur Entrée pour revenir au menu..."))

def internet_speed_test():
    """Effectue un test de vitesse de téléchargement simple."""
    print_color("\n--- ⚡ Test de vitesse Internet en cours... ---", MAIN_COLOR)
    try:
        test_url = "https://speed.hetzner.de/100MB.bin"
        print_color(f"(Téléchargement d'un fichier de test depuis {test_url.split('/')[2]})", WARNING_COLOR)
        
        response = requests.get(test_url, stream=True, timeout=10)
        start = time.time()
        size = 0
        max_time = 5
        
        for chunk in response.iter_content(chunk_size=8192):
            if not chunk: break
            size += len(chunk)
            if time.time() - start > max_time: break
        
        elapsed = time.time() - start
        
        if elapsed < 0.1:
             print_color("⚠️ Test trop rapide, résultat imprécis.", WARNING_COLOR)
             input(get_prompt("\nAppuie sur Entrée pour revenir au menu..."))
             return

        mbps = (size / elapsed) / (1024 * 1024)
        print_color(f"\n✅ Vitesse estimée : {mbps:.2f} Mo/s", MAIN_COLOR)
    except Exception as e:
        print_color(f"⚠️ Erreur lors du test de vitesse : {e}", Fore.RED)
    input(get_prompt("\nAppuie sur Entrée pour revenir au menu..."))

def port_scan():
    """Scan simple des ports courants sur une cible donnée."""
    try:
        target = user_input("Adresse IP ou nom d’hôte à scanner : ")
    except KeyboardInterrupt: return
    if not target: print_color("❌ Cible vide.", Fore.RED); time.sleep(1); return
    print_color(f"\n--- 🔍 Scan des ports courants sur {target}... ---\n", MAIN_COLOR)
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080]
    
    try:
        ip_target = socket.gethostbyname(target)
    except Exception:
        print_color(f"❌ Impossible de résoudre l'hôte : {target}", Fore.RED)
        input(get_prompt("\nAppuie sur Entrée pour revenir au menu...")); return
        
    try:
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            result = s.connect_ex((ip_target, port))
            
            if result == 0:
                print_color(f"✅ Port {port} ouvert", MAIN_COLOR)
            else:
                print_color(f"❌ Port {port} fermé/filtré", WARNING_COLOR)
            s.close()
    except Exception as e:
        print_color(f"⚠️ Erreur lors du scan : {e}", Fore.RED)
    
    input(get_prompt("\nAppuie sur Entrée pour revenir au menu..."))

def generate_random_ip():
    """Génère un nombre spécifié d'adresses IP aléatoires."""
    clear_console()
    print_color("\n--- 🎲 Générateur d’adresses IP aléatoires ---\n", MAIN_COLOR)
    try:
        count = int(user_input("Combien d’IP veux-tu générer ? : "))
    except KeyboardInterrupt: return
    except ValueError: print_color("❌ Nombre invalide.", Fore.RED); time.sleep(0.5); return

    for i in range(count):
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        print_color(f"💡 IP générée : {ip}", MAIN_COLOR)
        time.sleep(0.05)
    input(get_prompt("\nAppuie sur Entrée pour revenir au menu..."))

# ---------------------------
# FONCTIONS DE GÉNÉRATION DE CODES (Couleur ROUGE)
# ---------------------------

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
CHARS_UPPER_DIGITS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' # Pour Roblox/Fortnite
MAX_CODES = 3000

def get_generation_count():
    """Demande le nombre de codes à générer avec la limite MAX_CODES."""
    try:
        count_str = user_input(f"Combien de codes générer (max {MAX_CODES}) ? : ", color=LAUNCHER_COLOR)
        if not count_str.isdigit():
            print_color("❌ Saisir un nombre valide.", Fore.RED); time.sleep(1); return 0
        count = min(int(count_str), MAX_CODES)
        return count
    except KeyboardInterrupt: 
        return 0
    except ValueError: 
        print_color("❌ Nombre invalide.", Fore.RED); time.sleep(0.5); return 0

def generate_nitro_placeholder_code():
    """Génère des codes Discord Nitro de 19 caractères (placeholder)."""
    clear_console()
    print_color("\n--- 🎁 Générateur de Code Nitro (Placeholder) ---", LAUNCHER_COLOR)
    print_color(f"{Style.BRIGHT}{Fore.RED}⚠️ PLACEHOLDER : Codes aléatoires de 19 caractères.", Fore.RED)

    count = get_generation_count()
    if count == 0: return

    print_color(f"\nCodes générés ({count} codes) :", LAUNCHER_COLOR)

    for _ in range(count):
        code = ''.join(random.choice(CHARS) for _ in range(19))
        print_color(f"🎁 https://discord.gift/{code}", LAUNCHER_COLOR)
        time.sleep(0.001)
        
    input(get_prompt("\nAppuie sur Entrée pour revenir au menu...", color=LAUNCHER_COLOR))

def generate_roblox_code():
    """Génère des codes Roblox (cartes cadeaux 18 caractères) (placeholder)."""
    clear_console()
    print_color("\n--- 🧱 Générateur de Code Roblox (Placeholder) ---", LAUNCHER_COLOR)
    print_color(f"{Style.BRIGHT}{Fore.RED}⚠️ PLACEHOLDER : Codes aléatoires de 18 caractères.", Fore.RED)

    count = get_generation_count()
    if count == 0: return

    print_color(f"\nCodes générés ({count} codes) :", LAUNCHER_COLOR)

    # Longueur définie à 18 caractères comme demandé par l'image
    ROBLOX_CODE_LENGTH = 18 
    
    for _ in range(count):
        # Utilisation de CHARS_UPPER_DIGITS pour les majuscules et les chiffres
        code = ''.join(random.choice(CHARS_UPPER_DIGITS) for _ in range(ROBLOX_CODE_LENGTH)) 
        print_color(f"🧱 Code Roblox : {code}", LAUNCHER_COLOR)
        time.sleep(0.001)
        
    input(get_prompt("\nAppuie sur Entrée pour revenir au menu...", color=LAUNCHER_COLOR))

def generate_fortnite_code():
    """Génère des codes V-Bucks Fortnite (12 caractères, formaté) (placeholder)."""
    clear_console()
    print_color("\n--- 🔫 Générateur de Code Fortnite (V-Bucks) (Placeholder) ---", LAUNCHER_COLOR)
    print_color(f"{Style.BRIGHT}{Fore.RED}⚠️ PLACEHOLDER : Codes aléatoires de 12 caractères (Formaté : XXXX-XXXX-XXXX).", Fore.RED)

    count = get_generation_count()
    if count == 0: return

    print_color(f"\nCodes générés ({count} codes) :", LAUNCHER_COLOR)

    for _ in range(count):
        # 12 caractères (4-4-4)
        raw_code = ''.join(random.choice(CHARS_UPPER_DIGITS) for _ in range(12)) # Utilisation de CHARS_UPPER_DIGITS
        formatted_code = f"{raw_code[0:4]}-{raw_code[4:8]}-{raw_code[8:12]}"
        print_color(f"🔫 Code Fortnite : {formatted_code}", LAUNCHER_COLOR)
        time.sleep(0.001)
        
    input(get_prompt("\nAppuie sur Entrée pour revenir au menu...", color=LAUNCHER_COLOR))

def code_generator_menu():
    """Sous-menu pour les différents générateurs de codes (Option 8 du menu principal)."""
    while True:
        clear_console()
        print_color("\n--- 🎁 MENU GÉNÉRATEUR DE CODES (PLACEHOLDER) ---", LAUNCHER_COLOR)
        
        # CHANGEMENT ICI : Rétablissement du Rouge Vif (Style.BRIGHT + Fore.RED) pour l'avertissement
        print_color(f"{Style.BRIGHT}{Fore.RED}⚠️ ATTENTION : CES CODES SONT UNIQUEMENT DES PLACEHOLDERS (EXEMPLES).", Style.BRIGHT + Fore.RED)
        print_color(f"{Fore.RED}Veuillez noter la limite de {MAX_CODES} codes par génération.", Fore.RED) # Ligne suivante en Rouge standard
        print_color("\n", WHITE_COLOR)
        
        print_color("1. 🎁 Code Nitro (Discord) (19 car.)", LAUNCHER_COLOR)
        print_color("2. 🧱 Code Roblox (18 car.)", LAUNCHER_COLOR)
        print_color("3. 🔫 Code Fortnite (V-Bucks) (12 car.)", LAUNCHER_COLOR)
        
        print_color("\n0. ↩ Retour au menu principal", LAUNCHER_COLOR)
        
        try:
            choice = user_input("\nChoisis un générateur (1-3) : ", color=LAUNCHER_COLOR).strip()
        except KeyboardInterrupt:
            return

        if choice == '1':
            generate_nitro_placeholder_code()
        elif choice == '2':
            generate_roblox_code()
        elif choice == '3':
            generate_fortnite_code()
        elif choice == '0':
            return
        else:
            print_color("❌ Choix invalide.", Fore.RED)
            time.sleep(1)


# ---------------------------
# Fonction Launcher (Couleur ROUGE)
# ---------------------------
def launch_application():
    """Menu Launcher Admin: Affiche les options rapides et le lancement custom."""
    launcher_prompt_color = LAUNCHER_COLOR # Utilise la couleur Rouge pour le prompt du Launcher
    
    while True:
        clear_console()
        
        # Affichage de l'ADMIN MODE à droite (en Rouge)
        try:
            cols = os.get_terminal_size().columns
        except OSError:
            cols = 80
        admin_label = "ADMIN MODE"
        pad = max(0, cols - len(admin_label) - 1)
        # Utilisation directe de LAUNCHER_COLOR (Rouge) pour l'affichage statique
        sys.stdout.write(" " * pad + LAUNCHER_COLOR + admin_label + Style.RESET_ALL + "\n")
        
        print_color("\n--- 🚀 Lanceur d'applications (ADMIN) ---", LAUNCHER_COLOR)
        
        # 1. Display Quick Launch options (1-12)
        print_color("--- Applications rapides (1-12) ---", WHITE_COLOR)
        for key, (name, _) in QUICK_LAUNCH_ITEMS.items():
            print_color(f"[{key.rjust(2)}] {name}", LAUNCHER_COLOR)

        # 2. Display Custom Launch option
        print_color("-----------------------------------", WHITE_COLOR)
        print_color("[13] 💻 Lancer par Nom/Chemin (Custom)", LAUNCHER_COLOR)
        print_color("[00] ↩ Retour au menu principal", LAUNCHER_COLOR)

        try:
            # Utilisation de la fonction user_input avec la couleur du launcher
            choice = user_input("\nChoisis une option (00-13) : ", color=launcher_prompt_color).strip()
        except KeyboardInterrupt:
            print_color("↩ Retour au menu principal...", LAUNCHER_COLOR)
            time.sleep(0.4)
            return

        if choice == '00':
            return # Retour au menu principal
        
        elif choice in QUICK_LAUNCH_ITEMS:
            name, command = QUICK_LAUNCH_ITEMS[choice]
            print_color(f"\nLancement de '{name}'...", LAUNCHER_COLOR)
            
            if platform.system().lower() == "windows":
                os.system(f'start "" "{command}"')
            else:
                os.system(f'xdg-open "{command}"' if os.name == 'posix' else f'open "{command}"')
            
            print_color("✅ Lancement effectué (vérifie ton écran).", LAUNCHER_COLOR)
            time.sleep(1)
            input(get_prompt("\nAppuie sur Entrée pour revenir au launcher...", color=launcher_prompt_color))
            
        elif choice == '13':
            # Option 13: Lancement personnalisé
            clear_console()
            print_color("\n--- 💻 Lancement par Nom/Chemin ---", LAUNCHER_COLOR)
            print_color("Exemples : chrome, explorer, 'C:\\...\\app.exe'", WARNING_COLOR)

            try:
                app_name = user_input("Nom ou chemin du programme à lancer : ", color=launcher_prompt_color)
            except KeyboardInterrupt:
                continue # Retourne au sous-menu Launcher
                
            if not app_name:
                print_color("❌ Nom/chemin vide.", Fore.RED)
                time.sleep(1)
                continue
            
            try:
                print_color(f"Lancement de '{app_name}'...", LAUNCHER_COLOR)
                if platform.system().lower() == "windows":
                    os.system(f"start \"\" \"{app_name}\"")
                else:
                    os.system(app_name)
                
                print_color("✅ Lancement effectué.", LAUNCHER_COLOR)
            except Exception as e:
                print_color(f"❌ Erreur lors du lancement : {e}", Fore.RED)
                print_color("Vérifie ton chemin/nom d'application.", Fore.RED)
            
            time.sleep(1)
            input(get_prompt("\nAppuie sur Entrée pour revenir au launcher...", color=launcher_prompt_color))
            
        else:
            print_color("❌ Choix invalide.", Fore.RED)
            time.sleep(1)

# ---------------------------
# Menu principal (Couleur BLEUE)
# ---------------------------

BANNER = """
      ▄▄▄█████▓      █    ██        ███▄    █ 
      ▓  ██▒ ▓▒      ██  ▓██▒        ██ ▀█   █ 
      ▒ ▓██░ ▒░    ▓██  ▒██░        ▓██  ▀█ ██▒
      ░ ▓██▓ ░     ▓▓█  ░██░        ▓▓█▒  ▐▌██▒
        ▒██▒ ░  ██▓ ▒▒█████▓  ██▓ ▒██░   ▓██░
        ▒ ░░    ▒▓▒ ░▒▓▒ ▒ ▒  ▒▓▒ ░ ▒░   ▒ ▒ 
          ░     ░▒  ░░▒░ ░ ░  ░▒  ░ ░░   ░ ▒░
          ░     ░    ░░░ ░ ░  ░    ░     ░ ░ 
                                    
                                     ░ 
"""

def main_menu():
    while True:
        clear_console()
        
        # Affiche la bannière et "by 105"
        print_color(BANNER, MAIN_COLOR, delay=0.0005)
        print_color("                      by 105\n", WHITE_COLOR)

        print_color("\n--- 🛠️ Outils Réseau & Système ---\n", WHITE_COLOR)
        
        # Options principales (1 à 7) avec Emojis
        print_color("1. 📡 Ping d’un hôte", MAIN_COLOR)
        print_color("2. 🔍 Recherche d’informations IP", MAIN_COLOR)
        print_color("3. 🌐 Voir mon adresse IP locale", MAIN_COLOR)
        print_color("4. ⚙️ Informations système", MAIN_COLOR)
        print_color("5. ⚡ Test de vitesse Internet", MAIN_COLOR)
        print_color("6. 🔎 Scanner de ports", MAIN_COLOR)
        print_color("7. 🎲 Générateur d’IP aléatoires", MAIN_COLOR)
        
        # Option 8 : Reste en couleur principale (Bleu)
        print_color("8. 🎁 Générateur de Codes (Nitro, Roblox, Fortnite)", MAIN_COLOR)
        
        # Option Quitter standard
        print_color("9. 🚪 Quitter", MAIN_COLOR)
        quit_choice = "9"

        try:
            # Le prompt mentionne la commande secrète 'tun>'
            choice = user_input(f"\nChoisis une option (1-{quit_choice}) ou 'tun>' : ", color=MAIN_COLOR).strip()
        except KeyboardInterrupt:
            print_color("↩ Retour au menu principal...", MAIN_COLOR)
            time.sleep(0.9)
            continue

        # --- Gestion des commandes secrètes ---
        
        # Accès direct au Launcher (Rouge)
        if choice == "tun>":
            launch_application()
            continue # Revient au menu principal (Bleu)
            
        # --- Gestion des options de menu ---

        if choice == "1":
            ping_host()
        elif choice == "2":
            ip_lookup()
        elif choice == "3":
            get_ip_address()
        elif choice == "4":
            system_info()
        elif choice == "5":
            internet_speed_test()
        elif choice == "6":
            port_scan()
        elif choice == "7":
            generate_random_ip() 
        # NOUVEAU: Appel du sous-menu de génération
        elif choice == "8":
            code_generator_menu()
        
        # Quitter
        elif choice == "9":
            print_color("👋 Au revoir !", MAIN_COLOR)
            break
        
        else:
            print_color("❌ Choix invalide.", Fore.RED)
            time.sleep(1)

if __name__ == "__main__":
    # Étape 1: Écran de Verrouillage
    if lock_screen():
        # Étape 2: Menu Principal si le PIN est correct
        try:
            main_menu()
        except KeyboardInterrupt:
            print_color("\nInterrompu. Au revoir.", MAIN_COLOR)
            sys.exit(0)
    else:
        sys.exit(0)
