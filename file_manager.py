import os
import shutil
from logger import log

def list_directory(path):
    try:
        items = os.listdir(path)
        log(f"Liste de {path} : {items}")
        return items
    except Exception as e:
        log(f"Erreur de lecture {path} : {e}")
        return []

def change_directory(current_path, subfolder):
    new_path = os.path.join(current_path, subfolder)
    if os.path.isdir(new_path):
        log(f"Changement de répertoire : {new_path}")
        return new_path
    else:
        log(f"Erreur : {new_path} n'existe pas")
        return current_path

def rename_item(path, new_name):
    if os.path.exists(path):
        new_path = os.path.join(os.path.dirname(path), new_name)
        os.rename(path, new_path)
        log(f"Renommé {path} en {new_path}")
        return new_path
    else:
        log(f"Erreur : {path} introuvable")
        return None

def add_folder(path, name):
    new_dir = os.path.join(path, name)
    os.makedirs(new_dir, exist_ok=True)
    log(f"Dossier ajouté : {new_dir}")

def add_file(path, filename, content=""):
    full_path = os.path.join(path, filename)
    with open(full_path, "w") as f:
        f.write(content)
    log(f"Fichier ajouté : {full_path}")

def copy_item(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
    log(f"Copié {src} vers {dst}")

def move_item(src, dst):
    shutil.move(src, dst)
    log(f"Déplacé {src} vers {dst}")

def delete_item(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        log(f"Supprimé : {path}")
    except Exception as e:
        log(f"Erreur suppression {path} : {e}")