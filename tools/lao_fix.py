#!/usr/bin/env python3
"""
lao_fix.py — post-process / correct Lao text (Unicode normalization & Thai mapping).
"""

from __future__ import annotations

import unicodedata
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

THAI_TO_LAO_MAP = {
    'ภาคธุรกิจ': 'ພາກທຸລະກິດ',
    'ก': 'ກ', 'ຂ': 'ຂ', 'ຄ': 'ຄ', 'ງ': 'ງ', 'ຈ': 'ຈ', 'ຊ': 'ຊ', 'ຍ': 'ຍ', 'ດ': 'ດ',
    'ຕ': 'ຕ', 'ຖ': 'ຖ', 'ທ': 'ທ', 'ນ': 'ນ', 'ບ': 'ບ', 'ປ': 'ປ', 'ຜ': 'ຜ', 'ຝ': 'ຝ',
    'ພ': 'ພ', 'ຟ': 'ຟ', 'ມ': 'ມ', 'ຢ': 'ຢ', 'ຣ': 'ຣ', 'ລ': 'ລ', 'ວ': 'ວ', 'ສ': 'ສ',
    'ຫ': 'ຫ', 'ອ': 'ອ', 'ຮ': 'ຮ', 'ะ': 'ະ', 'ັ': 'ັ', 'າ': 'າ', 'ຳ': 'ຳ', 'ິ': 'ິ',
    'ີ': 'ີ', 'ຶ': 'ຶ', 'ື': 'ື', 'ຸ': 'ຸ', 'ູ': 'ູ', 'ເ': 'ເ', 'ແ': 'ແ', 'ໂ': 'ໂ',
    'ໃ': 'ໃ', 'ໄ': 'ໄ', '່': '່', '້': '້', '໊': '໊', '໋': '໋', '໌': '໌', 'ໍ': 'ໍ'
}

@dataclass
class Options:
    use_dict: bool = True
    map_thai: bool = True
    am_mode: str = "compose"
    keep_digits: bool = True
    strip_intra_space: bool = False
    dict_path: Optional[str] = None

@dataclass
class Stats:
    junk_removed: int = 0
    orphans_dropped: int = 0
    clusters_reordered: int = 0
    dup_marks_dropped: int = 0
    am_composed: int = 0
    spaces_fixed: int = 0
    dict_corrections: int = 0

def normalize_lao(text: str, opts: Optional[Options] = None) -> Tuple[str, Stats]:
    if opts is None:
        opts = Options()
    
    st = Stats()
    if not text:
        return text, st
    
    # 1. NFC normalization
    norm_text = unicodedata.normalize("NFC", text)
    
    # 2. Fix Thai script leaks if map_thai enabled
    if opts.map_thai:
        for k, v in THAI_TO_LAO_MAP.items():
            if k in norm_text:
                norm_text = norm_text.replace(k, v)
                st.dict_corrections += 1

    # 3. Clean zero-width junk / misplaced standalone tone mark spaces
    cleaned = []
    for ch in norm_text:
        if ch in ('\ufeff', '\u200b', '\u200c', '\u200d'):
            st.junk_removed += 1
            continue
        cleaned.append(ch)
    res = "".join(cleaned)
    
    # 4. Compose Sara AM (0ECD + 0EB2 -> 0EB3)
    if '\u0ecd\u0eb2' in res:
        st.am_composed += res.count('\u0ecd\u0eb2')
        res = res.replace('\u0ecd\u0eb2', '\u0eb3')
    
    # 5. Fix duplicate adjacent identical tone marks (e.g. ້້ -> ້)
    for mark in ['\u0ec8', '\u0ec9', '\u0eca', '\u0ecb', '\u0ecc']:
        double_mark = mark + mark
        if double_mark in res:
            st.dup_marks_dropped += res.count(double_mark)
            res = res.replace(double_mark, mark)

    return res, st

if __name__ == "__main__":
    print("lao_fix loaded successfully")
