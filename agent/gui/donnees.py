from pathlib import Path
import sys

RACINE = Path(__file__).resolve().parents[1]
REPERTOIRE_DONNEES = RACINE / "data"
REPERTOIRE_BUILD = RACINE / "build"

sys.path.insert(0, str(REPERTOIRE_BUILD))

PYTHON_VENV = RACINE / "gui" / ".venv" / "bin" / "python"

COMMANDE_COMPILATION = (
    f'cmake -S "{RACINE}" -B "{REPERTOIRE_BUILD}" -DBUILD_PYTHON_MODULE=ON '
    f'-DPython_EXECUTABLE="{PYTHON_VENV}" '
    f'&& cmake --build "{REPERTOIRE_BUILD}" -j'
)


def charger_bibliotheque():
    import bibliotheque_py

    return bibliotheque_py.load_library(str(REPERTOIRE_DONNEES))
