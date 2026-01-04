from __future__ import annotations

import re


def chunk_markdown(md: str, *, max_chars: int = 2_000, overlap: int = 200) -> list[str]:
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    if not md:
        return []
    out: list[str] = []
    i = 0
    while i < len(md):
        j = min(len(md), i + max_chars)
        out.append(md[i:j].strip())
        if j == len(md):
            break
        i = max(0, j - overlap)
    return [c for c in out if c]
