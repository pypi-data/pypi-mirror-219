import json
from typing import Any, List


def load_jl(path: str) -> List[Any]:
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def save_jl(data: List[Any], path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        for d in data:
            f.write(f'{json.dumps(d, ensure_ascii=False)}\n')

