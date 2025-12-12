import os
import time

# --- Configuration et Données ---

# État global du lanceur
ADMIN_MODE = False
DEFAULT_COLOR = "\033[96m" # Cyan clair (couleur de base)
ADMIN_COLOR = "\033[91m"   # Rouge vif pour le mode Admin
RESET_COLOR = "\033[0m"    # Réinitialisation de la couleur
BLOCK_COLOR = "\033[90m"   # Gris foncé pour les options bloquées

# Menu Principal (Options quotidiennes)
MENU_ITEMS = {
    '1': ('💨 Launch Steam', 'steam://open/main'),
    '2': ('💎 Launch Epic Games Launcher', 'com.epicgames.launcher://'),
    '3': ('🎧 Launch Discord', 'discord://'),
    '4': ('💜 Launch Twitch', 'https://www.twitch.tv/'),
    '5': ('📺 Launch YouTube', 'https://www.youtube.com/'),
    '6': ('🕹️ Launch Roblox', 'roblox://'),
    '7': ('🤖 Launch ChatGPT (Web)', 'https://chat.openai.com/'),
    '8': ('📦 Launch Microsoft Store', 'ms-windows-store:'),
    '9': ('⚙️ Launch Windows Settings', 'ms-settings:'),
    '10': ('🗺️ Launch Maps', 'bingmaps:'),
    '11': ('📧 Launch Email App', 'mailto:'),
    '12': ('🧮 Launch Calculator', 'calculator:'),
    '0': ('❌ Quit Launcher', None)
}

# Menu Administrateur (Options avancées)
ADMIN_ITEMS = {
    'A': ('🛠️ Windows Services', 'services.msc'),
    'B': ('📊 Task Manager', 'taskmgr'),
    'C': ('🖥️ System Information', 'msinfo32'),
    'D': ('🧹 Disk Cleanup', 'cleanmgr'),
    'E': ('⌨️ Command Prompt (Admin)', 'cmd'),
    'R': ('↩️ Return to Main Menu', None),
    '0': ('❌ Quit Launcher', None)
}

# --- Fonctions d'Affichage et de Nettoyage ---

def clear_screen():
    """Nettoie la console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_color():
    """Retourne la couleur actuelle (Admin ou Default)."""
    return ADMIN_COLOR if ADMIN_MODE else DEFAULT_COLOR

def display_logo():
    """Affiche le logo ASCII Art et le titre du lanceur."""
    clear_screen()
    color = get_current_color()

    # Affichage du logo
    print(color) 
    print("███    ███  █████  ██ ███    ██     ███    ███ ███████ ███    ██ ██    ██")
    print("████  ████ ██  ██ ██ ████   ██     ████  ████ ██      ████   ██ ██    ██")
    print("██ ████ ██ ███████ ██ ██ ██  ██     ██ ████ ██ █████   ██ ██  ██ ██    ██")
    print("██  ██  ██ ██  ██ ██ ██  ██ ██     ██  ██  ██ ██      ██  ██ ██ ██    ██")
    print("██      ██ ██  ██ ██ ██   ████     ██      ██ ███████ ██   ████  ██████")
    print("--------------------------------------------------------------------------")
    
    # Affichage du titre avec l'indicateur Admin si nécessaire
    admin_tag = f" {color}[ADMIN]{RESET_COLOR}" if ADMIN_MODE else ""
    
    print(f"\n🚀 T U N Complete Quick Launcher{admin_tag}")
    print("--------------------------------")
    print(RESET_COLOR) 

def display_admin_menu_full():
    """Affiche le menu Admin complet (lorsque ADMIN_MODE est True)."""
    color = get_current_color()
    print(color)
    print("🛠️ ADMIN TOOLS")
    print("-----------------")
    
    # Affiche les options Admin (A, B, C, D, E, R)
    for key in ['A', 'B', 'C', 'D', 'E', 'R']:
        name, _ = ADMIN_ITEMS[key]
        print(f"[{key}] {name}")
    
    # Affiche l'option Quitter (0)
    print(f"[0] {MENU_ITEMS['0'][0]}")
    print(RESET_COLOR)
    return ADMIN_ITEMS


def display_main_menu_with_locked():
    """Affiche le menu Principal avec les options Admin listées en bas (bloquées)."""
    color = get_current_color()
    print(color)
    print("💡 QUICK LAUNCH OPTIONS")
    print("------------------------")
    
    # 1. Affichage en deux colonnes pour le menu principal
    items_list = list(MENU_ITEMS.items())
    num_items = len(items_list) - 1 
    COL_WIDTH = 38 

    for i in range(1, 10):
        if i-1 >= len(items_list): continue 
        key, (name, _) = items_list[i-1]
        line = f"[{key}] {name.ljust(COL_WIDTH - len(key) - 4)}"
        
        if i + 9 <= num_items:
            key_r, (name_r, _) = items_list[i + 9 - 1]
            line += f"[{key_r}] {name_r}"
        print(line)

    # 2. Affichage des options ADMIN bloquées
    print("\n--------------------------------")
    print(f"       {BLOCK_COLOR}[ADMIN TOOLS] (BLOCKED){RESET_COLOR}")
    print("--------------------------------")
    
    # Liste les options A, B, C, D, E en gris
    for key in ['A', 'B', 'C', 'D', 'E']:
        name, _ = ADMIN_ITEMS[key]
        print(f"{BLOCK_COLOR}[{key}] {name} (BLOCKED){RESET_COLOR}")

    print("\n")
    # Affiche l'option Quitter (0)
    print(f"[0] {MENU_ITEMS['0'][0]}")
    print(RESET_COLOR)
    
    return MENU_ITEMS


def display_menu():
    """Bascule entre l'affichage du menu Principal et du menu Admin."""
    if ADMIN_MODE:
        return display_admin_menu_full()
    else:
        return display_main_menu_with_locked()


# --- Fonctions de Lancement et d'Animation ---

def launch_app(command):
    """Lance la commande/URI et affiche une animation."""
    display_logo()
    print("\033[93m") # Jaune pour les messages d'animation
    print("⏳ Launching application...")
    time.sleep(1.5) 
    
    if os.name == 'nt':
        os.system(f'start "" "{command}"')
    else:
        os.system(f'xdg-open "{command}"' if os.name == 'posix' else f'open "{command}"')
        
    time.sleep(0.5)
    print(RESET_COLOR) 

# --- Boucle Principale du Programme ---

def main():
    global ADMIN_MODE
    display_logo()

    while True:
        current_menu = display_menu() 
        
        # Le prompt indique les options pour les deux menus (1-12, A-R)
        choice = input("Select your choice (0-12 / A-R) > ").strip().upper()
        
        # --- EASTER EGG CHECK ---
        if choice == '105':
            ADMIN_MODE = not ADMIN_MODE
            display_logo()
            print(f"\n{get_current_color()}--- Admin Mode {'ACTIVATED' if ADMIN_MODE else 'DEACTIVATED'} ---{RESET_COLOR}")
            time.sleep(1)
            continue
        # ------------------------
        
        # --- GESTION DES CHOIX ---
        
        # Si nous sommes en mode NON-ADMIN, vérifie si l'utilisateur a tenté de choisir une option Admin bloquée.
        if not ADMIN_MODE and choice in ['A', 'B', 'C', 'D', 'E', 'R']:
            display_logo()
            print("\033[91mAccess denied. Activate Admin Mode (contact 105devving@gmail.com) to use these options.\033[0m") 
            time.sleep(1)
            continue

        # Si le choix est dans le menu actuel (Admin ou Principal)
        if choice in current_menu:
            name, command = current_menu[choice]
            
            if choice == '0': # Quitter
                clear_screen()
                print("\nClosing launcher menu...")
                time.sleep(1)
                break
            
            # Gestion du retour au Menu Principal
            elif ADMIN_MODE and choice == 'R':
                ADMIN_MODE = False
                display_logo()
                continue
                
            else:
                launch_app(command)
                display_logo()
        
        elif choice == "":
            display_logo()
            continue
            
        else:
            # Gère les choix invalides
            display_logo()
            print("\033[91mInvalid choice. Please try again.\033[0m") 
            time.sleep(1)

if __name__ == "__main__":
    main()