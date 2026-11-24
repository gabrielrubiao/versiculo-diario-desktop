import json
from pathlib import Path
from typing import Any
from src.config import DEFAULT_SETTINGS, STATE_FILE, VERSES_FILE


class VerseRepository:
    def __init__(self, verses_path: Path = VERSES_FILE, state_path: Path = STATE_FILE) -> None:
        self.verses_path = verses_path
        self.state_path = state_path

    def load_verses(self) -> list[dict[str, Any]]:
        if not self.verses_path.exists():
            raise FileNotFoundError(f"Arquivo de versículos não encontrado: {self.verses_path}")

        with self.verses_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list) or not data:
            raise ValueError("A base de versículos deve conter uma lista não vazia.")

        return data

    def default_state(self) -> dict[str, Any]:
        return {
            "last_date": None,
            "current_verse_id": None,
            "used_ids": [],
            "settings": dict(DEFAULT_SETTINGS),
        }

    def load_state(self) -> dict[str, Any]:
        state = self.default_state()
        if not self.state_path.exists():
            return state

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                saved = json.load(file)

            if isinstance(saved, dict):
                state["last_date"] = saved.get("last_date")
                state["current_verse_id"] = saved.get("current_verse_id")
                state["used_ids"] = saved.get("used_ids", []) if isinstance(saved.get("used_ids"), list) else []

                saved_settings = saved.get("settings")
                if isinstance(saved_settings, dict):
                    state["settings"].update(saved_settings)
        except (json.JSONDecodeError, OSError):
            return self.default_state()

        return state

    def save_state(self, state: dict[str, Any]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with self.state_path.open("w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=2)