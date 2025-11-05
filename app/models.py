from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import date

@dataclass
class Habit:
    id: Optional[int] = None
    name: str = ''
    periodicity: str = 'daily'  # 'daily' or 'weekly'
    created_at: str = field(default_factory=lambda: date.today().isoformat())
    active: bool = True
    notes: str = ''

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'periodicity': self.periodicity,
            'created_at': self.created_at,
            'active': int(self.active),
            'notes': self.notes
        }

    @staticmethod
    def from_dict(d: Dict) -> 'Habit':
        return Habit(
            id=d.get('id'),
            name=d.get('name', ''),
            periodicity=d.get('periodicity', 'daily'),
            created_at=d.get('created_at', date.today().isoformat()),
            active=bool(d.get('active', 1)),
            notes=d.get('notes', '')
        )

