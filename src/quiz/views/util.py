from typing import Optional


def parse_bool(s: str) -> Optional[bool]:
    match s.lower():
        case 'true':
            return True
        case 'false':
            return False
        case _:
            return None
