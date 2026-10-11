from dataclasses import dataclass, field, asdict
from typing import Dict, Any

@dataclass
class AppConfig:
    mode: str = "horda"
    total_encounters: int = 0
    discord_webhook: str = ""
    webhook_jwt: str = ""
    ocr_retries: int = 6
    horde_size: int = 5
    mode_zorua: bool = False
    zorua_wait: float = 3.0
    horde_key_sweet_scent: str = "5"
    horde_key_leppa: str = "4"
    horde_slot_sweet_scent: str = "1"
    pp_max_sweet_scent: str = "32"
    ditto_patrol_time: float = 2.5
    ditto_key_attack: str = "2"
    ditto_name_attack: str = "False Swipe"
    pp_max_swipe: str = "40"
    ditto_key_sleep: str = "1"
    ditto_name_sleep: str = "Spore"
    pp_max_spore: str = "15"
    ditto_key_ball: str = "5"
    ditto_key_potion: str = "6"
    ditto_key_leppa: str = "4"
    auto_heal_hp: bool = True
    auto_heal_pp: bool = True
    timing_ball_wait: float = 0.5
    timing_capture_settle: float = 2.5
    timing_leppa_wait: float = 1.5
    timing_ball_press_wait: float = 0.7

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        valid_keys = cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
