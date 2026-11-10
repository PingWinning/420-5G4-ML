# AGENTS.md

Projet C++17 `bibliotheque` : application console de gestion de bibliothèque. Le code, les commentaires et l'interface sont en français ; conserver cette langue pour les textes visibles.

## Compilation

```bash
cd agent
cmake -S . -B build
cmake --build build -j
```

- `CMakeLists.txt` utilise `file(GLOB SOURCES "*.cpp")` : relancer CMake après ajout ou suppression d'un fichier `.cpp`.
- C++17, options `-Wall -Wextra -Wpedantic` (pas de `-Werror`).
- Aucune dépendance externe hors STL.
- `build/` est ignoré par git. Aucun test, CTest, lint ou typecheck n'est configuré : vérifier en compilant puis en exerçant le menu.

## Exécution

```bash
cd agent
./build/bibliotheque -d data    # ou --data-dir data
```

- `-d` / `--data-dir` est indispensable en pratique : sans lui, `FileManager` reçoit des chemins vides et le chargement/sauvegarde échoue.
- Le chemin passé à `-d` est relatif au répertoire courant. Depuis `build/`, utiliser `./bibliotheque -d ../data`.

## Données

- `data/books.txt` : `titre|auteur|isbn|1|borrowerId` (`1` disponible, `0` emprunté).
- `data/users.txt` : `nom|userId|isbn1,isbn2`.
- `Library::removeBook` côté C++ ne vérifie pas si le livre est emprunté ; le refus de supprimer un livre emprunté est appliqué uniquement par la GUI.
- L'application charge et sauvegarde ces fichiers suivis par git (sauvegarde à la sortie et via le menu 12). Pour tester sans modifier le dépôt, copier `data/` dans un répertoire temporaire et passer ce chemin à `-d`.
- Le menu 13 crée des fichiers `.backup` dans le répertoire de données ; ils sont ignorés par git via `*.backup`. `FileManager::createBackup` lance une exception non attrapée si un backup existe déjà : `copy_file` n'écrase pas le fichier existant.

## Structure

- `main.cpp` : point d'entrée, parsing de `-d`, menu interactif.
- `library.*` : possède les `Book`/`User` via `unique_ptr`, gère recherche et prêts.
- `filemanager.*` : lecture/écriture des fichiers pipe-delimited et sauvegardes.
- `book.*`, `user.*` : modèles et sérialisation.

## Module Python pybind11

Module minimal `bibliotheque_py` : charge les données et expose `Library` / `Book`.

```bash
cd agent
cmake -S . -B build -DBUILD_PYTHON_MODULE=ON \
  -DPython_EXECUTABLE="$PWD/gui/.venv/bin/python"
cmake --build build -j
./gui/.venv/bin/python python/test_bibliotheque_py.py
```

- `python/bindings.cpp` est dans un sous-dossier : le GLOB racine `*.cpp` ne l'inclut pas et le target console reste inchangé.
- `BUILD_PYTHON_MODULE` est activé par défaut ; si Python ou pybind11 manque, un avertissement est émis et la console se construit quand même.
- pybind11 système (2.13.6) et les headers Python 3.13 suffisent ; aucune dépendance pip supplémentaire.
- Le test copie `data/` dans un répertoire temporaire et ne modifie pas les fichiers suivis.

## Test GUI Python

Test d'interface minimal avec CustomTkinter dans `gui/`.

```bash
cd agent/gui
/usr/bin/python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python main.py
```

- Ne pas réutiliser le `.venv` racine (obsolète/cassé) ; le venv local `gui/.venv/` est ignoré par git.
- `requirements.txt` fige les dépendances installées.
- L'écran Livres affiche les vraies données via `gui/donnees.py` : le module `bibliotheque_py` est importé depuis `build/` et les fichiers sont lus depuis `data/`.
- L'écran Utilisateurs charge `all_users()`. L'ID du panneau d'ajout est généré automatiquement en grisé : premier `USRxxx` libre sur 3 chiffres, recalculé après chaque ajout. L'ajout reste en mémoire, sans sauvegarde dans `data/`.
- La GUI accepte `-d` / `--data-dir` comme la console ; sans option, elle utilise `agent/data`. Le chemin est relatif au répertoire courant.
- Les boutons Sauvegarder et Créer une copie utilisent `FileManager` via `bibliotheque_py`. Un backup existant n'est jamais écrasé : le binding renvoie `False` et la GUI demande de supprimer l'ancien fichier.
- Aucune action ne sauvegarde automatiquement dans `data/`. À la fermeture, la GUI utilise `messagebox.askyesnocancel` s'il y a des modifications non sauvegardées ; Annuler garde la fenêtre ouverte.
- Si le chargement échoue, l'écran Livres affiche l'erreur et la commande cmake pour compiler le module.
- La fenêtre nécessite un serveur X11 (`DISPLAY`), fourni par le devcontainer.

Le `.devcontainer` fournit X11, utilisé par la GUI Python de test ; l'application C++ reste uniquement console.
