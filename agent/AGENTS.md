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
- L'application charge et sauvegarde ces fichiers suivis par git (sauvegarde à la sortie et via le menu 12). Pour tester sans modifier le dépôt, copier `data/` dans un répertoire temporaire et passer ce chemin à `-d`.
- Le menu 13 crée des fichiers `.backup` dans le répertoire de données ; ils ne sont pas ignorés par git. `copy_file` n'écrase pas un backup existant.

## Structure

- `main.cpp` : point d'entrée, parsing de `-d`, menu interactif.
- `library.*` : possède les `Book`/`User` via `unique_ptr`, gère recherche et prêts.
- `filemanager.*` : lecture/écriture des fichiers pipe-delimited et sauvegardes.
- `book.*`, `user.*` : modèles et sérialisation.

Le `.devcontainer` fournit X11, mais l'application est uniquement console.
