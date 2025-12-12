import time
import webbrowser
import os
import platform

# Codes d'échappement ANSI pour la couleur bleue, le jaune (pour les liens/clés) et la réinitialisation
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# --- CONFIGURATION DES LIENS ET DE LA CLÉ ---
TIKTOK_LINK = "https://www.tiktok.com/@tun_ontiktok"
YOUTUBE_LINK = "https://www.youtube.com/@tun_onyoutube"
FINAL_KEY = "319>"
# ----------------------------------------------

def print_blue(text):
    """Affiche le texte en bleu."""
    print(f"{BLUE}{text}{RESET}")

def print_yellow(text):
    """Affiche le texte en jaune (pour la clé et les liens)."""
    print(f"{YELLOW}{text}{RESET}")

def clear_screen():
    """Efface l'écran de la console (compatible Windows/Linux/macOS)."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def wait_for_start(step_name):
    """Attend que l'utilisateur appuie sur ENTRÉE pour lancer le timer."""
    input(f"{BLUE}🔔 Appuyez sur ENTRÉE pour confirmer l'abonnement {step_name} et lancer le timer...{RESET}")

def countdown(seconds, message):
    """Gère un compte à rebours générique."""
    temps_restant = seconds
    while temps_restant > 0:
        print(f"{BLUE}\r⏳ {message} {temps_restant} secondes...{RESET}", end="", flush=True)
        time.sleep(1)
        temps_restant -= 1
    # Efface la ligne du compte à rebours
    print("\r" + " " * 80, end="", flush=True)

def etapes_code():
    """Gère les étapes successives d'obtention de la clé T.U.N."""
    clear_screen()
    print_blue("🔑 Obtention de la clé T.U.N (2 Étapes) ✨")
    print_blue("-------------------------------------------------")
    
    # --- ÉTAPE 1 : TikTok (5 secondes) ---
    print_blue("▶️ ÉTAPE 1 : S'abonner au TikTok (5 secondes de timer)")
    print_blue("1. Copiez et visitez le lien TikTok :")
    print_yellow(f"   {TIKTOK_LINK}")
    print_blue("2. Abonnez-vous à la chaîne.")
    
    wait_for_start("TikTok") # L'utilisateur appuie sur ENTRÉE ici
    
    countdown(5, "Temps restant avant de passer à l'étape 2 :")
    print_blue("\r✅ Étape 1 complétée. Passage à l'étape 2.")
    print_blue("-------------------------------------------------")
    
    # --- ÉTAPE 2 : YouTube (15 secondes) ---
    print_blue("▶️ ÉTAPE 2 : S'abonner au YouTube (15 secondes de timer pour la clé)")
    print_blue("1. Copiez et visitez le lien YouTube :")
    print_yellow(f"   {YOUTUBE_LINK}")
    print_blue("2. Abonnez-vous à la chaîne.")
    
    wait_for_start("YouTube") # L'utilisateur appuie sur ENTRÉE ici
    
    countdown(15, "Temps restant avant l'affichage de la Clé T.U.N :")
    
    # --- Clé Finale ---
    print_blue("\r🎉 FÉLICITATIONS ! Les deux étapes sont terminées.")
    print_blue("-------------------------------------------------")
    print_blue("✅ Clé T.U.N Obtenue : ")
    print_yellow(f"   {FINAL_KEY}")

    input(f"{BLUE}\nAppuyez sur ENTRÉE pour revenir au menu...{RESET}")
    menu_principal()

def menu_principal():
    """Affiche le menu principal et gère les choix de l'utilisateur."""
    while True:
        clear_screen()
        print_blue("💻 Menu Principal 🚀")
        print_blue("--------------------")
        print_blue("1] Obtention de la clé T.U.N")
        print_blue("2] Quitter")
        print_blue("--------------------")

        # Laisse la zone de saisie non colorée pour l'utilisateur, mais affiche le prompt en bleu
        choix = input(f"{BLUE}Entrez votre choix (1 ou 2) : {RESET}").strip()

        if choix == '1':
            etapes_code()
        elif choix == '2':
            clear_screen()
            print_blue("👋 Merci d'avoir utilisé le programme. Au revoir !")
            break
        else:
            print_blue("\nChoix invalide. Veuillez entrer '1' ou '2'.")
            time.sleep(1.5)

# Lancement du programme
if __name__ == "__main__":
    menu_principal()