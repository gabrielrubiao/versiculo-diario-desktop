from pathlib import Path
import os

APP_NAME = "VersiculoDiarioDesktop"
APP_TITLE = "Versículo Diário"
STARTUP_REG_NAME = "VersiculoDiarioDesktop"

# Raiz do projeto (funciona tanto rodando via Python quanto via PyInstaller)
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
VERSES_FILE = ASSETS_DIR / "versiculos_pt.json"
ICON_FILE = ASSETS_DIR / "icon.ico"

# Pasta persistente do usuário no Windows (%APPDATA%\VersiculoDiarioDesktop)
appdata_base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
USER_DATA_DIR = appdata_base / APP_NAME
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = USER_DATA_DIR / "state.json"

# Configurações padrão do texto na área de trabalho
DEFAULT_SETTINGS = {
    "pos_x": 120,
    "pos_y": 120,
    "font_family": "Segoe UI",
    "font_size": 22,
    "text_color": "#FFFFFF",
    "shadow_color": "#000000",
    "max_width": 680,
    "visible": True,
}