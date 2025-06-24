import os
from config import BASE_DIR
from file_manager import *
from ftp_manager import backup_to_ftp
from network_tools import scan_ports

# Utilisateurs simulés
users = {
    "superadmin": {"password": "superpass", "role": "superadmin"},
    "sonia": {"password": "123", "role": "superadmin"},
    
    "admin": {"password": "adminpass", "role": "admin"},
    "nafy": {"password": "123", "role": "admin"},
    
    "client": {"password": "clientpass", "role": "client"},
}

# Permissions par rôle
roles = {
    "superadmin": {
        "lister": True,
        "changer_dir": True,
        "ajouter": True,
        "renommer": True,
        "copier": True,
        "deplacer": True,
        "supprimer": True,
        "sauvegarder": True,
        "scanner_ports": True,
    },
    "admin": {
        "lister": True,
        "changer_dir": True,
        "ajouter": True,
        "renommer": True,
        "copier": True,
        "deplacer": True,
        "supprimer": False,  # par exemple, admin ne supprime pas
        "sauvegarder": True,
        "scanner_ports": True,
    },
    "client": {
        "lister": True,
        "changer_dir": True,
        "ajouter": False,
        "renommer": False,
        "copier": False,
        "deplacer": False,
        "supprimer": False,
        "sauvegarder": False,
        "scanner_ports": False,
    },
}

def authentifier():
    print("=== Connexion utilisateur ===")
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    user = users.get(username)
    if user and user["password"] == password:
        print(f"Connexion réussie : {username} ({user['role']})")
        return user["role"], username
    else:
        print("Nom d'utilisateur ou mot de passe incorrect.")
        return None, None

def verifier_droit(role, action):
    return roles.get(role, {}).get(action, False)

def main():
    role, username = authentifier()
    if not role:
        print("Fin du programme.")
        return

    os.makedirs(BASE_DIR, exist_ok=True)
    current_path = BASE_DIR

    while True:
        print(f"\nUtilisateur : {username} ({role}) - Répertoire actuel : {current_path}")
        print("1. Lister le contenu")
        print("2. Changer de répertoire (descendre dans un sous-répertoire)")
        print("2b. Remonter d’un niveau")
        print("3. Ajouter un dossier/fichier")
        print("4. Renommer")
        print("5. Copier")
        print("6. Déplacer")
        print("7. Supprimer")
        print("8. Sauvegarder vers FTP")
        print("9. Scanner ports réseau")
        print("0. Quitter")

        choice = input("Choix : ")

        if choice == "1":
            if verifier_droit(role, "lister"):
                print(list_directory(current_path))
            else:
                print("Accès refusé : permission refusée pour lister.")

        elif choice == "2":
            if verifier_droit(role, "changer_dir"):
                sub = input("Nom du sous-répertoire : ")
                current_path = change_directory(current_path, sub)
            else:
                print("Accès refusé : permission refusée pour changer de répertoire.")
                
        elif choice == "2b":
            if verifier_droit(role, "changer_dir"):
                parent = os.path.dirname(current_path)
                if parent.startswith(BASE_DIR):
                    current_path = parent
                else:
                    print("Déjà à la racine du projet.")
            else:
                print("Accès refusé : permission refusée pour changer de répertoire.")

        elif choice == "3":
            if verifier_droit(role, "ajouter"):
                typ = input("(d)ossier ou (f)ichier ? ")
                name = input("Nom : ")
                if typ == "d":
                    add_folder(current_path, name)
                else:
                    content = input("Contenu du fichier : ")
                    add_file(current_path, name, content)
            else:
                print("Accès refusé : permission refusée pour ajouter.")

        elif choice == "4":
            if verifier_droit(role, "renommer"):
                target = input("Nom actuel : ")
                new_name = input("Nouveau nom : ")
                rename_item(os.path.join(current_path, target), new_name)
            else:
                print("Accès refusé : permission refusée pour renommer.")

        elif choice == "5":
            if verifier_droit(role, "copier"):
                src = input("Nom à copier : ")
                dst = input("Destination : ")
                copy_item(os.path.join(current_path, src), os.path.join(current_path, dst))
            else:
                print("Accès refusé : permission refusée pour copier.")

        elif choice == "6":
            if verifier_droit(role, "deplacer"):
                src = input("Nom à déplacer : ")
                dst = input("Destination : ")
                move_item(os.path.join(current_path, src), os.path.join(current_path, dst))
            else:
                print("Accès refusé : permission refusée pour déplacer.")

        elif choice == "7":
            if verifier_droit(role, "supprimer"):
                target = input("Nom à supprimer : ")
                delete_item(os.path.join(current_path, target))
            else:
                print("Accès refusé : permission refusée pour supprimer.")

        elif choice == "8":
            if verifier_droit(role, "sauvegarder"):
                file_to_backup = input("Fichier à sauvegarder : ")
                region = input("Région : ")
                client = input("Client : ")
                backup_to_ftp(os.path.join(current_path, file_to_backup), region, client)
            else:
                print("Accès refusé : permission refusée pour sauvegarder.")

        elif choice == "9":
            if verifier_droit(role, "scanner_ports"):
                ip = input("IP à scanner : ")
                ports = range(20, 1025)
                scan_ports(ip, ports)
            else:
                print("Accès refusé : permission refusée pour scanner les ports.")

        elif choice == "0":
            print("Déconnexion. À bientôt !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
