from datetime import date
import random
from typing import Any, Optional
from src.repository import VerseRepository


class DailyVerseService:
    def __init__(self, repository: VerseRepository) -> None:
        self.repository = repository
        self.verses: list[dict[str, Any]] = self.repository.load_verses()
        self.state: dict[str, Any] = self.repository.load_state()

    def _find_verse_by_id(self, verse_id: Optional[int]) -> Optional[dict[str, Any]]:
        if verse_id is None:
            return None
        for verse in self.verses:
            if verse.get("id") == verse_id:
                return verse
        return None

    def _pick_next_verse(self, exclude_id: Optional[int] = None) -> dict[str, Any]:
        used_ids: list[int] = list(self.state.get("used_ids", []))
        all_ids = [v["id"] for v in self.verses]

        available_ids = [vid for vid in all_ids if vid not in used_ids and vid != exclude_id]

        # Se já usamos quase todos os versículos, reinicia o ciclo mantendo o atual fora da lista imediata
        if not available_ids:
            used_ids = [exclude_id] if exclude_id is not None else []
            available_ids = [vid for vid in all_ids if vid not in used_ids] or all_ids

        chosen_id = random.choice(available_ids)
        used_ids.append(chosen_id)

        self.state["used_ids"] = used_ids
        self.state["current_verse_id"] = chosen_id
        self.state["last_date"] = date.today().isoformat()
        self.repository.save_state(self.state)

        chosen = self._find_verse_by_id(chosen_id)
        return chosen if chosen is not None else self.verses[0]

    def get_today_verse(self) -> dict[str, Any]:
        today_str = date.today().isoformat()
        current = self._find_verse_by_id(self.state.get("current_verse_id"))

        if self.state.get("last_date") == today_str and current is not None:
            return current

        return self._pick_next_verse(exclude_id=current["id"] if current else None)

    def next_verse(self) -> dict[str, Any]:
        current = self._find_verse_by_id(self.state.get("current_verse_id"))
        current_id = current["id"] if current else None
        return self._pick_next_verse(exclude_id=current_id)

    @staticmethod
    def format_reference(verse: dict[str, Any]) -> str:
        return f"{verse['livro']} {verse['capitulo']}:{verse['versiculo']}"

    def format_for_copy(self, verse: dict[str, Any]) -> str:
        ref = self.format_reference(verse)
        return f"\"{verse['texto']}\" — {ref}"