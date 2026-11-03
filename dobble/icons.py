"""학교사랑 도블 그림 57개 (SVG, viewBox 0 0 100 100).

모든 그림은 같은 스타일: 진한 외곽선 + 단색 채우기.
"""

K = "#2b2b2b"  # 외곽선 색
FONT = "font-family=\"'WenQuanYi Zen Hei','Noto Sans KR',sans-serif\" font-weight=\"bold\""

ICONS = {}


ICONS["조록나무"] = """
<rect x="43" y="58" width="14" height="34" rx="3" fill="#8b5a2b"/>
<path d="M50 70 L38 60 M50 76 L62 64" fill="none"/>
<circle cx="30" cy="50" r="18" fill="#2e8b3a"/>
<circle cx="70" cy="50" r="18" fill="#2e8b3a"/>
<circle cx="50" cy="32" r="24" fill="#3a9d47"/>
<circle cx="50" cy="56" r="16" fill="#2e8b3a" stroke="none"/>
<circle cx="36" cy="38" r="5" fill="#d4a86a"/>
<circle cx="62" cy="26" r="5" fill="#d4a86a"/>
<circle cx="70" cy="52" r="5" fill="#d4a86a"/>
<circle cx="45" cy="54" r="4" fill="#d4a86a"/>
"""

ICONS["동백꽃"] = """
<ellipse cx="22" cy="74" rx="18" ry="9" transform="rotate(-30 22 74)" fill="#2e7d32"/>
<ellipse cx="78" cy="74" rx="18" ry="9" transform="rotate(30 78 74)" fill="#2e7d32"/>
<g fill="#d7263d">
<circle cx="50" cy="26" r="18"/><circle cx="73" cy="43" r="18"/>
<circle cx="64" cy="70" r="18"/><circle cx="36" cy="70" r="18"/>
<circle cx="27" cy="43" r="18"/>
</g>
<circle cx="50" cy="51" r="20" fill="#d7263d" stroke="none"/>
<circle cx="50" cy="51" r="11" fill="#ffd23f"/>
<g fill="#f4a300" stroke="none"><circle cx="46" cy="47" r="2.5"/><circle cx="54" cy="48" r="2.5"/><circle cx="50" cy="55" r="2.5"/></g>
"""

ICONS["학교"] = """
<rect x="10" y="44" width="80" height="46" fill="#f6dba5"/>
<rect x="38" y="24" width="24" height="66" fill="#f0c97a"/>
<line x1="50" y1="24" x2="50" y2="6"/>
<path d="M50 7 L66 12 L50 17 Z" fill="#d7263d"/>
<circle cx="50" cy="36" r="7" fill="#fff"/>
<path d="M50 36 L50 32 M50 36 L53 37" fill="none" stroke-width="2"/>
<g fill="#7cc6f2">
<rect x="16" y="52" width="10" height="10"/><rect x="16" y="70" width="10" height="10"/>
<rect x="74" y="52" width="10" height="10"/><rect x="74" y="70" width="10" height="10"/>
</g>
<rect x="43" y="68" width="14" height="22" fill="#8b5a2b"/>
"""

ICONS["교표"] = """
<g stroke="none" fill="#b8964e">
<path d="M14 30 L51 42 L86 30 L65 55 L86 79 L50 68 L14 79 L36 56 Z"/>
<circle cx="50" cy="27" r="8.5"/>
</g>
<g fill="none" stroke="#b8964e" stroke-width="6" stroke-linecap="butt">
<path d="M54 12 A40 40 0 0 1 90 48"/><path d="M90 56 A40 40 0 0 1 54 92"/>
<path d="M46 92 A40 40 0 0 1 10 56"/><path d="M10 48 A40 40 0 0 1 46 12"/>
</g>
"""

ICONS["달력(11/9)"] = f"""
<rect x="12" y="16" width="76" height="76" rx="6" fill="#fff"/>
<path d="M12 22 Q12 16 18 16 L82 16 Q88 16 88 22 L88 44 L12 44 Z" fill="#e63946"/>
<rect x="28" y="8" width="7" height="16" rx="3" fill="#bbb"/>
<rect x="65" y="8" width="7" height="16" rx="3" fill="#bbb"/>
<text x="50" y="40" text-anchor="middle" font-size="23" fill="#fff" stroke="none" {FONT}>11월</text>
<circle cx="50" cy="68" r="19" fill="none" stroke="#e63946" stroke-width="4"/>
<text x="50" y="80" text-anchor="middle" font-size="32" fill="#2b2b2b" stroke="none" {FONT}>9</text>
"""

ICONS["연필"] = """
<g transform="rotate(-45 50 50)">
<rect x="12" y="40" width="58" height="20" fill="#ffc93c"/>
<line x1="12" y1="47" x2="70" y2="47" stroke-width="2"/><line x1="12" y1="53" x2="70" y2="53" stroke-width="2"/>
<rect x="4" y="40" width="10" height="20" rx="3" fill="#f78fb3"/>
<path d="M70 40 L92 50 L70 60 Z" fill="#f3d2a2"/>
<path d="M85 47 L92 50 L85 53 Z" fill="#2b2b2b"/>
</g>
"""

ICONS["지우개"] = f"""
<g transform="rotate(-20 50 50)">
<rect x="14" y="32" width="72" height="36" rx="5" fill="#fff"/>
<rect x="38" y="30" width="48" height="40" fill="#3a86ff"/>
<g fill="#fff" stroke="none" opacity="0.6"><rect x="44" y="36" width="36" height="4" rx="2"/></g>
</g>
"""

ICONS["가위"] = """
<path d="M38 56 L84 12" stroke-width="7" stroke="#2b2b2b"/>
<path d="M38 56 L84 12" stroke-width="3" stroke="#d9dde3"/>
<path d="M62 56 L16 12" stroke-width="7" stroke="#2b2b2b"/>
<path d="M62 56 L16 12" stroke-width="3" stroke="#d9dde3"/>
<circle cx="31" cy="73" r="15" fill="#e63946"/><circle cx="31" cy="73" r="7" fill="#fff"/>
<circle cx="69" cy="73" r="15" fill="#e63946"/><circle cx="69" cy="73" r="7" fill="#fff"/>
<circle cx="50" cy="40" r="3.5" fill="#2b2b2b"/>
"""

ICONS["가방"] = """
<path d="M38 20 Q38 6 50 6 Q62 6 62 20" fill="none" stroke-width="6"/>
<rect x="16" y="16" width="68" height="78" rx="18" fill="#e63946"/>
<path d="M16 40 Q16 16 40 16 L60 16 Q84 16 84 40 L84 48 Q50 58 16 48 Z" fill="#c1121f"/>
<rect x="28" y="58" width="44" height="28" rx="8" fill="#ff8fa3"/>
<path d="M32 66 L68 66" stroke-width="2.5"/>
<rect x="30" y="36" width="9" height="30" rx="2" fill="#ffd23f"/>
<rect x="61" y="36" width="9" height="30" rx="2" fill="#ffd23f"/>
<rect x="28" y="50" width="13" height="9" rx="2" fill="#bbb"/>
<rect x="59" y="50" width="13" height="9" rx="2" fill="#bbb"/>
"""

ICONS["국어 교과서"] = f"""
<rect x="20" y="6" width="68" height="88" rx="4" fill="#fff"/>
<rect x="14" y="6" width="68" height="88" rx="4" fill="#2a9d8f"/>
<rect x="14" y="6" width="10" height="88" fill="#21867a"/>
<rect x="27" y="16" width="51" height="34" rx="5" fill="#fff"/>
<text x="53" y="42" text-anchor="middle" font-size="21" fill="#21867a" stroke="none" {FONT}>국어</text>
<text x="53" y="80" text-anchor="middle" font-size="18" fill="#fff" stroke="none" {FONT}>가나다</text>
"""

ICONS["수학 교과서"] = f"""
<rect x="20" y="6" width="68" height="88" rx="4" fill="#fff"/>
<rect x="14" y="6" width="68" height="88" rx="4" fill="#f4a261"/>
<rect x="14" y="6" width="10" height="88" fill="#e07a2f"/>
<rect x="27" y="16" width="51" height="34" rx="5" fill="#fff"/>
<text x="53" y="42" text-anchor="middle" font-size="21" fill="#e07a2f" stroke="none" {FONT}>수학</text>
<text x="53" y="80" text-anchor="middle" font-size="18" fill="#fff" stroke="none" {FONT}>1+2</text>
"""

ICONS["칠판"] = f"""
<rect x="6" y="16" width="88" height="62" rx="3" fill="#a0703c"/>
<rect x="12" y="22" width="76" height="50" fill="#2f5d3a"/>
<path d="M20 30 L36 30" stroke="#5f8f6a" stroke-width="2" fill="none"/>
<rect x="10" y="78" width="80" height="6" fill="#8b5a2b"/>
<rect x="60" y="74" width="12" height="4" fill="#fff" stroke-width="1.5"/>
<line x1="24" y1="84" x2="20" y2="96"/><line x1="76" y1="84" x2="80" y2="96"/>
"""

ICONS["시계"] = """
<circle cx="50" cy="50" r="42" fill="#3a86ff"/>
<circle cx="50" cy="50" r="34" fill="#fff"/>
<g stroke-width="3">
<line x1="50" y1="20" x2="50" y2="26"/><line x1="50" y1="74" x2="50" y2="80"/>
<line x1="20" y1="50" x2="26" y2="50"/><line x1="74" y1="50" x2="80" y2="50"/>
</g>
<line x1="50" y1="50" x2="36" y2="38" stroke-width="5"/>
<line x1="50" y1="50" x2="66" y2="32" stroke-width="4"/>
<circle cx="50" cy="50" r="4" fill="#e63946"/>
"""

ICONS["의자"] = """
<rect x="28" y="10" width="44" height="30" rx="5" fill="#e9a35b"/>
<line x1="34" y1="40" x2="34" y2="54" stroke-width="5"/><line x1="66" y1="40" x2="66" y2="54" stroke-width="5"/>
<rect x="22" y="52" width="56" height="12" rx="4" fill="#e9a35b"/>
<line x1="28" y1="64" x2="24" y2="94" stroke-width="5" stroke="#555"/>
<line x1="72" y1="64" x2="76" y2="94" stroke-width="5" stroke="#555"/>
"""

ICONS["책상"] = """
<rect x="6" y="28" width="88" height="12" rx="3" fill="#e9a35b"/>
<rect x="14" y="40" width="72" height="18" fill="#cfd4da"/>
<line x1="14" y1="58" x2="14" y2="90" stroke-width="5" stroke="#555"/>
<line x1="86" y1="58" x2="86" y2="90" stroke-width="5" stroke="#555"/>
<line x1="8" y1="90" x2="20" y2="90" stroke-width="5" stroke="#555"/>
<line x1="80" y1="90" x2="92" y2="90" stroke-width="5" stroke="#555"/>
"""

ICONS["우유"] = """
<path d="M22 36 L34 16 L72 16 L60 36 Z" fill="#e8f2ff"/>
<path d="M60 36 L72 16 L84 36 Z" fill="#c9dcf5"/>
<rect x="34" y="8" width="38" height="9" fill="#fff"/>
<rect x="22" y="36" width="38" height="58" fill="#fff"/>
<path d="M60 36 L84 36 L84 88 L60 94 Z" fill="#dbe7f7"/>
<path d="M22 70 L60 70 L60 94 L22 94 Z" fill="#3a86ff"/>
<path d="M60 70 L84 68 L84 88 L60 94 Z" fill="#2f6fd6"/>
<g fill="#2b2b2b" stroke="none"><ellipse cx="32" cy="48" rx="5" ry="4"/><ellipse cx="48" cy="58" rx="6" ry="4"/><ellipse cx="50" cy="44" rx="3" ry="2.5"/></g>
<path d="M46 26 L52 2" stroke="#e63946" stroke-width="5"/>
"""

ICONS["버스"] = """
<rect x="6" y="20" width="88" height="56" rx="10" fill="#ffc93c"/>
<g fill="#bde0fe">
<rect x="14" y="28" width="16" height="18" rx="2"/><rect x="34" y="28" width="16" height="18" rx="2"/>
<rect x="54" y="28" width="16" height="18" rx="2"/>
</g>
<rect x="76" y="28" width="12" height="36" rx="2" fill="#bde0fe"/>
<line x1="6" y1="56" x2="74" y2="56" stroke-width="3"/>
<circle cx="26" cy="78" r="10" fill="#444"/><circle cx="26" cy="78" r="4" fill="#ccc"/>
<circle cx="72" cy="78" r="10" fill="#444"/><circle cx="72" cy="78" r="4" fill="#ccc"/>
"""

ICONS["배드민턴라켓"] = """
<g transform="rotate(-35 50 50)">
<ellipse cx="50" cy="30" rx="22" ry="26" fill="#fff" stroke="#e63946" stroke-width="5"/>
<g stroke-width="1.5" stroke="#888">
<line x1="36" y1="10" x2="36" y2="50"/><line x1="43" y1="6" x2="43" y2="55"/><line x1="50" y1="5" x2="50" y2="56"/>
<line x1="57" y1="6" x2="57" y2="55"/><line x1="64" y1="10" x2="64" y2="50"/>
<line x1="30" y1="18" x2="70" y2="18"/><line x1="28" y1="26" x2="72" y2="26"/><line x1="28" y1="34" x2="72" y2="34"/><line x1="30" y1="42" x2="70" y2="42"/>
</g>
<line x1="50" y1="56" x2="50" y2="78" stroke-width="4"/>
<rect x="45" y="76" width="10" height="20" rx="3" fill="#3a86ff"/>
</g>
<g transform="translate(70 70) rotate(20)">
<path d="M-8 -14 L8 -14 L5 4 L-5 4 Z" fill="#fff"/>
<circle cx="0" cy="8" r="6" fill="#e63946"/>
</g>
"""

ICONS["컴퓨터"] = """
<rect x="10" y="10" width="80" height="56" rx="5" fill="#555"/>
<rect x="16" y="16" width="68" height="44" fill="#111"/>
<path d="M22 22 L36 22 M22 28 L30 28" stroke="#555" stroke-width="3"/>
<rect x="44" y="66" width="12" height="10" fill="#888"/>
<rect x="30" y="76" width="40" height="5" rx="2" fill="#888"/>
<rect x="18" y="85" width="64" height="10" rx="3" fill="#ddd"/>
"""

ICONS["줄넘기"] = """
<path d="M24 26 C60 -4 104 40 62 58 C24 74 30 100 74 80" fill="none" stroke="#ff8c42" stroke-width="5"/>
<g transform="rotate(-50 18 20)"><rect x="12" y="4" width="12" height="30" rx="6" fill="#3a86ff"/><line x1="12" y1="26" x2="24" y2="26" stroke-width="2"/></g>
<g transform="rotate(-70 82 80)"><rect x="76" y="64" width="12" height="30" rx="6" fill="#3a86ff"/><line x1="76" y1="72" x2="88" y2="72" stroke-width="2"/></g>
"""

ICONS["돌하르방"] = """
<path d="M28 26 Q26 4 50 4 Q74 4 72 26 Z" fill="#6e6e6e"/>
<ellipse cx="50" cy="27" rx="30" ry="5" fill="#6e6e6e"/>
<path d="M26 30 L74 30 Q78 46 74 62 L26 62 Q22 46 26 30 Z" fill="#8a8a8a"/>
<circle cx="37" cy="41" r="8" fill="#a8a8a8"/><circle cx="63" cy="41" r="8" fill="#a8a8a8"/>
<circle cx="37" cy="41" r="3" fill="#2b2b2b"/><circle cx="63" cy="41" r="3" fill="#2b2b2b"/>
<path d="M47 36 L42 54 Q50 58 58 54 L53 36 Z" fill="#9a9a9a"/>
<path d="M40 60 L60 60" stroke-width="3"/>
<path d="M28 62 L72 62 L76 96 L24 96 Z" fill="#7d7d7d"/>
<rect x="24" y="68" width="34" height="10" rx="5" fill="#9a9a9a"/>
<rect x="42" y="82" width="34" height="10" rx="5" fill="#9a9a9a"/>
<g fill="#555" stroke="none"><circle cx="40" cy="12" r="1.8"/><circle cx="58" cy="16" r="1.8"/><circle cx="30" cy="50" r="1.6"/><circle cx="70" cy="52" r="1.6"/><circle cx="66" cy="72" r="1.8"/><circle cx="32" cy="88" r="1.8"/><circle cx="50" cy="20" r="1.5"/></g>
"""

ICONS["은행잎"] = """
<path d="M50 64 Q48 82 40 94" fill="none" stroke="#8b5a2b" stroke-width="4"/>
<path d="M50 64 Q24 50 8 30 Q14 10 34 10 Q44 10 47 20 L50 30 L53 20 Q56 10 66 10 Q86 10 92 30 Q76 50 50 64 Z" fill="#ffc300"/>
<g fill="none" stroke="#e09f00" stroke-width="2"><path d="M50 62 L16 28"/><path d="M50 62 L30 16"/><path d="M50 62 L44 20"/><path d="M50 62 L56 20"/><path d="M50 62 L70 16"/><path d="M50 62 L84 28"/></g>
"""

ICONS["연못"] = """
<path d="M14 52 Q8 30 34 28 Q52 16 72 26 Q94 30 90 54 Q92 78 64 80 Q44 90 28 78 Q8 72 14 52 Z" fill="#4cc9f0"/>
<g fill="none" stroke="#fff" stroke-width="2.5"><ellipse cx="40" cy="58" rx="10" ry="4"/><ellipse cx="40" cy="58" rx="4" ry="1.5"/></g>
<path d="M62 44 A12 9 0 1 1 74 54 L64 49 Z" fill="#4caf50"/>
<circle cx="70" cy="44" r="5" fill="#f78fb3" stroke-width="2"/>
<g stroke="#2e7d32" stroke-width="3"><line x1="22" y1="50" x2="20" y2="16"/><line x1="28" y1="48" x2="30" y2="20"/></g>
<rect x="16" y="12" width="7" height="14" rx="3.5" fill="#8b5a2b" stroke-width="2"/>
<rect x="27" y="16" width="7" height="14" rx="3.5" fill="#8b5a2b" stroke-width="2"/>
<ellipse cx="74" cy="80" rx="9" ry="6" fill="#9e9e9e"/><ellipse cx="84" cy="74" rx="6" ry="5" fill="#bdbdbd"/>
"""

ICONS["선생님"] = """
<line x1="70" y1="36" x2="94" y2="8" stroke="#8b5a2b" stroke-width="4"/>
<path d="M58 44 L72 34" stroke="#2b2b2b" stroke-width="10"/>
<path d="M58 44 L72 34" stroke="#2a9d8f" stroke-width="6"/>
<circle cx="73" cy="34" r="4" fill="#ffd6a5" stroke-width="2"/>
<rect x="36" y="72" width="10" height="22" fill="#555"/><rect x="50" y="72" width="10" height="22" fill="#555"/>
<rect x="32" y="40" width="32" height="36" rx="8" fill="#2a9d8f"/>
<path d="M42 40 L48 52 L54 40 Z" fill="#fff" stroke-width="2.5"/>
<rect x="22" y="50" width="16" height="20" rx="2" fill="#ffd23f"/>
<circle cx="48" cy="24" r="14" fill="#ffd6a5"/>
<path d="M33 28 Q30 8 48 8 Q66 8 63 28 Q62 18 54 16 Q44 20 36 18 Q34 22 33 28 Z" fill="#4a3220"/>
<circle cx="42" cy="26" r="5" fill="none" stroke-width="2"/><circle cx="54" cy="26" r="5" fill="none" stroke-width="2"/>
<line x1="47" y1="26" x2="49" y2="26" stroke-width="2"/>
<path d="M44 33 Q48 36 52 33" fill="none" stroke-width="2"/>
"""

ICONS["학생"] = """
<rect x="28" y="48" width="44" height="30" rx="8" fill="#ffc93c"/>
<path d="M68 54 L84 34" stroke="#2b2b2b" stroke-width="10"/>
<path d="M68 54 L84 34" stroke="#8ac926" stroke-width="6"/>
<circle cx="85" cy="32" r="5" fill="#ffd6a5" stroke-width="2"/>
<rect x="38" y="74" width="9" height="18" fill="#ffd6a5"/><rect x="53" y="74" width="9" height="18" fill="#ffd6a5"/>
<rect x="34" y="50" width="32" height="28" rx="8" fill="#8ac926"/>
<rect x="34" y="70" width="32" height="10" rx="2" fill="#3a86ff"/>
<line x1="38" y1="52" x2="38" y2="70" stroke="#e63946" stroke-width="4"/><line x1="62" y1="52" x2="62" y2="70" stroke="#e63946" stroke-width="4"/>
<ellipse cx="42" cy="94" rx="7" ry="3.5" fill="#fff"/><ellipse cx="58" cy="94" rx="7" ry="3.5" fill="#fff"/>
<circle cx="50" cy="30" r="18" fill="#ffd6a5"/>
<path d="M32 32 Q30 10 50 10 Q70 10 68 32 Q64 20 56 22 Q50 24 42 20 Q36 22 32 32 Z" fill="#2b2b2b"/>
<circle cx="43" cy="32" r="2.6" fill="#2b2b2b"/><circle cx="57" cy="32" r="2.6" fill="#2b2b2b"/>
<path d="M44 39 Q50 44 56 39" fill="none" stroke-width="2.5"/>
<g fill="#ff9aa2" stroke="none"><circle cx="38" cy="37" r="3"/><circle cx="62" cy="37" r="3"/></g>
"""

ICONS["하트"] = """
<path d="M50 88 L14 52 Q2 38 12 24 Q24 10 40 18 Q46 22 50 30 Q54 22 60 18 Q76 10 88 24 Q98 38 86 52 Z" fill="#e63946"/>
<path d="M24 32 Q28 24 36 24" fill="none" stroke="#fff" stroke-width="4"/>
"""

ICONS["미끄럼틀"] = """
<line x1="22" y1="24" x2="22" y2="92" stroke-width="4"/><line x1="38" y1="24" x2="38" y2="92" stroke-width="4"/>
<g stroke-width="3"><line x1="22" y1="40" x2="38" y2="40"/><line x1="22" y1="56" x2="38" y2="56"/><line x1="22" y1="72" x2="38" y2="72"/></g>
<rect x="18" y="18" width="24" height="8" rx="2" fill="#e63946"/>
<path d="M40 18 Q60 22 72 60 Q78 80 94 84 L94 92 Q72 90 64 64 Q54 34 40 28 Z" fill="#ffc93c"/>
"""

ICONS["축구골대와 축구공"] = """
<g stroke="#999" stroke-width="1.5">
<line x1="20" y1="20" x2="20" y2="68"/><line x1="35" y1="20" x2="35" y2="68"/><line x1="50" y1="20" x2="50" y2="68"/><line x1="65" y1="20" x2="65" y2="68"/><line x1="80" y1="20" x2="80" y2="68"/>
<line x1="8" y1="32" x2="92" y2="32"/><line x1="8" y1="44" x2="92" y2="44"/><line x1="8" y1="56" x2="92" y2="56"/>
</g>
<path d="M8 68 L8 14 L92 14 L92 68" fill="none" stroke-width="5"/>
<circle cx="56" cy="76" r="17" fill="#fff"/>
<path d="M56 68 L63 73 L60 81 L52 81 L49 73 Z" fill="#2b2b2b" stroke-width="2"/>
<path d="M56 68 L56 60 M63 73 L72 70 M60 81 L65 89 M52 81 L47 89 M49 73 L40 70" fill="none" stroke-width="2"/>
"""

ICONS["농구골대와 농구공"] = """
<rect x="18" y="6" width="64" height="40" rx="3" fill="#fff"/>
<rect x="38" y="22" width="24" height="18" fill="none" stroke="#e63946" stroke-width="3"/>
<ellipse cx="50" cy="44" rx="16" ry="4" fill="none" stroke="#e85d04" stroke-width="4"/>
<path d="M35 45 L41 62 L59 62 L65 45 M41 46 L46 62 M59 46 L54 62 M50 48 L50 62" fill="none" stroke-width="2"/>
<circle cx="50" cy="78" r="16" fill="#f77f00"/>
<path d="M34 78 L66 78 M50 62 L50 94 M38 66 Q46 78 38 90 M62 66 Q54 78 62 90" fill="none" stroke-width="2.5"/>
"""

ICONS["돌담"] = """
<g fill="#4a4a4a">
<path d="M6 92 L8 72 L30 70 L34 92 Z"/><path d="M34 92 L32 72 L56 68 L60 92 Z"/><path d="M60 92 L58 70 L80 72 L94 74 L94 92 Z"/>
<path d="M10 70 L14 50 L34 48 L38 70 Z"/><path d="M38 70 L36 48 L62 50 L60 68 Z"/><path d="M60 68 L64 48 L88 52 L90 72 Z"/>
<path d="M20 48 L24 28 L46 30 L44 48 Z"/><path d="M46 48 L48 26 L72 30 L70 50 Z"/>
</g>
<g fill="#888" stroke="none">
<circle cx="18" cy="80" r="2"/><circle cx="46" cy="80" r="2.5"/><circle cx="74" cy="84" r="2"/><circle cx="24" cy="60" r="2"/><circle cx="50" cy="58" r="2"/><circle cx="76" cy="60" r="2.5"/><circle cx="34" cy="38" r="2"/><circle cx="60" cy="38" r="2"/>
</g>
"""

ICONS["자"] = """
<g transform="rotate(-30 50 50)">
<rect x="4" y="36" width="92" height="28" rx="2" fill="#a8dadc"/>
<g stroke-width="2">
<line x1="12" y1="36" x2="12" y2="50"/><line x1="20" y1="36" x2="20" y2="44"/><line x1="28" y1="36" x2="28" y2="44"/><line x1="36" y1="36" x2="36" y2="44"/><line x1="44" y1="36" x2="44" y2="44"/>
<line x1="52" y1="36" x2="52" y2="50"/><line x1="60" y1="36" x2="60" y2="44"/><line x1="68" y1="36" x2="68" y2="44"/><line x1="76" y1="36" x2="76" y2="44"/><line x1="84" y1="36" x2="84" y2="44"/><line x1="92" y1="36" x2="92" y2="50"/>
</g>
</g>
"""

ICONS["딱풀"] = f"""
<rect x="30" y="8" width="40" height="28" rx="6" fill="#8338ec"/>
<rect x="28" y="32" width="44" height="60" rx="6" fill="#fff"/>
<rect x="28" y="48" width="44" height="26" fill="#ffbe0b"/>
<text x="50" y="67" text-anchor="middle" font-size="14" fill="#2b2b2b" stroke="none" {FONT}>풀</text>
<rect x="38" y="86" width="24" height="6" fill="#8338ec" stroke-width="2"/>
"""

ICONS["태극기"] = """
<line x1="8" y1="8" x2="8" y2="96" stroke="#8b5a2b" stroke-width="5"/>
<circle cx="8" cy="7" r="4" fill="#ffd23f" stroke-width="2"/>
<rect x="12" y="14" width="82" height="56" fill="#fff"/>
<g stroke="none">
<path d="M41 42 A12 12 0 0 1 65 42 A6 6 0 0 1 53 42 A6 6 0 0 0 41 42 Z" fill="#cd2e3a"/>
<path d="M41 42 A6 6 0 0 0 53 42 A6 6 0 0 0 65 42 A12 12 0 0 1 41 42 Z" fill="#0047a0"/>
</g>
<circle cx="53" cy="42" r="12" fill="none" stroke-width="1.5"/>
<g stroke="#000" stroke-width="2.5">
<g transform="rotate(-34 27 25)"><line x1="21" y1="21" x2="33" y2="21"/><line x1="21" y1="25" x2="33" y2="25"/><line x1="21" y1="29" x2="33" y2="29"/></g>
<g transform="rotate(34 79 59)"><line x1="73" y1="55" x2="77" y2="55"/><line x1="81" y1="55" x2="85" y2="55"/><line x1="73" y1="59" x2="77" y2="59"/><line x1="81" y1="59" x2="85" y2="59"/><line x1="73" y1="63" x2="77" y2="63"/><line x1="81" y1="63" x2="85" y2="63"/></g>
<g transform="rotate(34 79 25)"><line x1="73" y1="21" x2="77" y2="21"/><line x1="81" y1="21" x2="85" y2="21"/><line x1="73" y1="25" x2="85" y2="25"/><line x1="73" y1="29" x2="77" y2="29"/><line x1="81" y1="29" x2="85" y2="29"/></g>
<g transform="rotate(-34 27 59)"><line x1="21" y1="55" x2="33" y2="55"/><line x1="21" y1="59" x2="25" y2="59"/><line x1="29" y1="59" x2="33" y2="59"/><line x1="21" y1="63" x2="33" y2="63"/></g>
</g>
"""

ICONS["사물함"] = """
<rect x="10" y="8" width="80" height="86" rx="3" fill="#bbb"/>
<rect x="14" y="12" width="34" height="38" fill="#ff8fa3"/><rect x="52" y="12" width="34" height="38" fill="#80ed99"/>
<rect x="14" y="52" width="34" height="38" fill="#7cc6f2"/><rect x="52" y="52" width="34" height="38" fill="#ffd166"/>
<g fill="#555"><rect x="40" y="26" width="4" height="10" rx="1"/><rect x="78" y="26" width="4" height="10" rx="1"/><rect x="40" y="66" width="4" height="10" rx="1"/><rect x="78" y="66" width="4" height="10" rx="1"/></g>
<g stroke-width="2"><line x1="20" y1="18" x2="32" y2="18"/><line x1="58" y1="18" x2="70" y2="18"/><line x1="20" y1="58" x2="32" y2="58"/><line x1="58" y1="58" x2="70" y2="58"/></g>
"""

ICONS["식판"] = """
<rect x="6" y="18" width="88" height="66" rx="10" fill="#cfd4da"/>
<rect x="12" y="24" width="24" height="22" rx="5" fill="#8ac926"/>
<rect x="38" y="24" width="24" height="22" rx="5" fill="#ff8c42"/>
<rect x="64" y="24" width="24" height="22" rx="5" fill="#ffd166"/>
<rect x="12" y="50" width="36" height="28" rx="6" fill="#fff"/>
<rect x="52" y="50" width="36" height="28" rx="6" fill="#e63946"/>
<g fill="#eee" stroke="none"><circle cx="22" cy="60" r="2"/><circle cx="30" cy="64" r="2"/><circle cx="38" cy="60" r="2"/><circle cx="26" cy="70" r="2"/><circle cx="36" cy="70" r="2"/></g>
"""

ICONS["그네"] = """
<path d="M6 94 L24 10 L76 10 L94 94" fill="none" stroke="#e63946" stroke-width="6"/>
<line x1="20" y1="10" x2="80" y2="10" stroke-width="6" stroke="#e63946"/>
<line x1="38" y1="12" x2="38" y2="66" stroke="#666" stroke-width="2.5" stroke-dasharray="4 2"/>
<line x1="62" y1="12" x2="62" y2="66" stroke="#666" stroke-width="2.5" stroke-dasharray="4 2"/>
<rect x="32" y="64" width="36" height="8" rx="3" fill="#ffc93c"/>
"""

ICONS["귤"] = """
<circle cx="50" cy="56" r="34" fill="#ff9f1c"/>
<g fill="#e07b00" stroke="none"><circle cx="34" cy="50" r="1.8"/><circle cx="44" cy="70" r="1.8"/><circle cx="62" cy="66" r="1.8"/><circle cx="68" cy="48" r="1.8"/><circle cx="52" cy="40" r="1.8"/><circle cx="38" cy="62" r="1.8"/></g>
<path d="M50 24 Q60 6 78 12 Q70 28 50 24 Z" fill="#2e7d32"/>
<circle cx="50" cy="24" r="3" fill="#2e7d32"/>
<path d="M30 44 Q34 36 42 34" fill="none" stroke="#fff" stroke-width="3.5"/>
"""

ICONS["우산"] = """
<path d="M8 50 Q10 12 50 10 Q90 12 92 50 Q83 42 74 50 Q65 42 56 50 Q50 46 44 50 Q35 42 26 50 Q17 42 8 50 Z" fill="#3a86ff"/>
<path d="M50 10 Q38 26 44 50 M50 10 Q62 26 56 50" fill="none" stroke-width="2"/>
<line x1="50" y1="6" x2="50" y2="10" stroke-width="4"/>
<path d="M50 50 L50 84 Q50 94 40 94 Q32 94 32 86" fill="none" stroke-width="5"/>
"""

ICONS["새싹"] = """
<path d="M14 92 Q50 72 86 92 Z" fill="#8b5a2b"/>
<path d="M50 86 L50 50" stroke="#2e7d32" stroke-width="5"/>
<path d="M50 52 Q20 56 12 30 Q40 22 50 52 Z" fill="#80d468"/>
<path d="M50 52 Q80 56 88 30 Q60 22 50 52 Z" fill="#80d468"/>
<path d="M50 52 Q36 44 26 34 M50 52 Q64 44 74 34" fill="none" stroke="#2e7d32" stroke-width="2"/>
"""

ICONS["실내화"] = """
<path d="M8 72 L8 56 Q8 46 20 44 L48 40 Q58 38 66 48 L86 58 Q94 62 94 72 Z" fill="#fff"/>
<path d="M26 44 Q40 30 56 40" fill="none" stroke="#3a86ff" stroke-width="7"/>
<path d="M30 46 Q42 36 54 44" fill="#3a86ff" stroke="none"/>
<rect x="6" y="72" width="90" height="10" rx="4" fill="#8ecae6"/>
<g stroke-width="2"><line x1="62" y1="50" x2="56" y2="58"/><line x1="70" y1="54" x2="64" y2="62"/></g>
"""

ICONS["빗자루"] = """
<line x1="78" y1="6" x2="46" y2="58" stroke="#a0703c" stroke-width="7"/>
<line x1="78" y1="6" x2="46" y2="58" stroke="#c99a5b" stroke-width="3"/>
<path d="M40 52 L56 62 L44 96 L8 78 Z" fill="#f2c94c"/>
<rect x="38" y="50" width="20" height="10" rx="2" transform="rotate(32 48 55)" fill="#e63946"/>
<g stroke="#c9a227" stroke-width="2"><line x1="40" y1="64" x2="22" y2="84"/><line x1="46" y1="68" x2="34" y2="90"/><line x1="36" y1="60" x2="14" y2="78"/></g>
"""

ICONS["크레파스"] = f"""
<g stroke-width="2.5">
<path d="M18 40 L18 18 L24 8 L30 18 L30 40 Z" fill="#e63946"/>
<path d="M32 40 L32 12 L38 2 L44 12 L44 40 Z" fill="#ffbe0b"/>
<path d="M46 40 L46 16 L52 6 L58 16 L58 40 Z" fill="#3a86ff"/>
<path d="M60 40 L60 12 L66 2 L72 12 L72 40 Z" fill="#8ac926"/>
<path d="M74 40 L74 18 L80 8 L86 18 L86 40 Z" fill="#8338ec"/>
</g>
<rect x="12" y="36" width="80" height="56" rx="4" fill="#ffd166"/>
<rect x="12" y="36" width="80" height="12" fill="#fb8500"/>
<text x="52" y="78" text-anchor="middle" font-size="15" fill="#2b2b2b" stroke="none" {FONT}>크레파스</text>
"""

ICONS["시소"] = """
<path d="M40 92 L50 60 L60 92 Z" fill="#e63946"/>
<g transform="rotate(-14 50 58)">
<rect x="4" y="52" width="92" height="10" rx="4" fill="#ffc93c"/>
<path d="M14 52 L14 40 M10 40 L18 40" fill="none" stroke-width="4"/>
<path d="M86 52 L86 40 M82 40 L90 40" fill="none" stroke-width="4"/>
</g>
<circle cx="50" cy="58" r="4" fill="#555"/>
"""

ICONS["마이크"] = """
<g transform="rotate(-25 50 50)">
<rect x="42" y="44" width="16" height="50" rx="6" fill="#333"/>
<rect x="38" y="40" width="24" height="10" rx="3" fill="#888"/>
<circle cx="50" cy="26" r="20" fill="#cfd4da"/>
<g stroke-width="1.5" stroke="#777"><line x1="34" y1="18" x2="66" y2="18"/><line x1="31" y1="26" x2="69" y2="26"/><line x1="34" y1="34" x2="66" y2="34"/><line x1="42" y1="8" x2="42" y2="44"/><line x1="50" y1="6" x2="50" y2="46"/><line x1="58" y1="8" x2="58" y2="44"/></g>
<circle cx="50" cy="26" r="20" fill="none"/>
</g>
"""

ICONS["별"] = """
<path d="M50 6 L62 36 L94 38 L69 58 L78 90 L50 72 L22 90 L31 58 L6 38 L38 36 Z" fill="#ffd23f"/>
<path d="M44 30 L48 22" stroke="#fff" stroke-width="4"/>
"""

ICONS["피아노"] = """
<rect x="10" y="8" width="80" height="50" rx="4" fill="#2b2b2b"/>
<rect x="18" y="16" width="64" height="12" rx="2" fill="#444" stroke="#666" stroke-width="1.5"/>
<rect x="6" y="56" width="88" height="32" rx="2" fill="#fff"/>
<g stroke-width="2"><line x1="17" y1="56" x2="17" y2="88"/><line x1="28" y1="56" x2="28" y2="88"/><line x1="39" y1="56" x2="39" y2="88"/><line x1="50" y1="56" x2="50" y2="88"/><line x1="61" y1="56" x2="61" y2="88"/><line x1="72" y1="56" x2="72" y2="88"/><line x1="83" y1="56" x2="83" y2="88"/></g>
<g fill="#2b2b2b"><rect x="13" y="56" width="8" height="18"/><rect x="24" y="56" width="8" height="18"/><rect x="46" y="56" width="8" height="18"/><rect x="57" y="56" width="8" height="18"/><rect x="68" y="56" width="8" height="18"/></g>
<line x1="12" y1="88" x2="12" y2="96" stroke-width="4"/><line x1="88" y1="88" x2="88" y2="96" stroke-width="4"/>
"""

ICONS["바이올린"] = """
<g transform="rotate(-30 50 50)">
<rect x="46" y="4" width="8" height="34" fill="#2b2b2b"/>
<circle cx="50" cy="6" r="5" fill="#6d3b14"/>
<path d="M50 34 Q36 34 36 46 Q36 54 41 58 Q34 62 34 74 Q34 92 50 92 Q66 92 66 74 Q66 62 59 58 Q64 54 64 46 Q64 34 50 34 Z" fill="#8b4513"/>
<path d="M42 64 Q40 68 43 72 M58 64 Q60 68 57 72" fill="none" stroke-width="2.5"/>
<rect x="44" y="78" width="12" height="4" fill="#2b2b2b"/>
<g stroke="#eee" stroke-width="1"><line x1="48" y1="10" x2="48" y2="80"/><line x1="52" y1="10" x2="52" y2="80"/></g>
</g>
<line x1="20" y1="20" x2="86" y2="86" stroke="#a0703c" stroke-width="3.5"/>
<line x1="23" y1="25" x2="84" y2="88" stroke="#eee" stroke-width="1.5"/>
"""

ICONS["기타"] = """
<g transform="rotate(30 50 50)">
<rect x="44" y="2" width="12" height="44" fill="#6d3b14"/>
<rect x="42" y="0" width="16" height="10" rx="2" fill="#2b2b2b"/>
<path d="M50 36 Q30 34 30 50 Q30 58 36 62 Q24 68 24 80 Q24 98 50 98 Q76 98 76 80 Q76 68 64 62 Q70 58 70 50 Q70 34 50 36 Z" fill="#3a86ff"/>
<circle cx="50" cy="66" r="8" fill="#2b2b2b"/>
<rect x="42" y="82" width="16" height="5" fill="#6d3b14"/>
<g stroke="#eee" stroke-width="1"><line x1="47" y1="8" x2="47" y2="84"/><line x1="50" y1="8" x2="50" y2="84"/><line x1="53" y1="8" x2="53" y2="84"/></g>
</g>
"""

ICONS["벚꽃"] = """
<g fill="#ffc2d4">
<path id="p" d="M50 50 Q34 34 40 14 L50 22 L60 14 Q66 34 50 50 Z"/>
<path d="M50 50 Q34 34 40 14 L50 22 L60 14 Q66 34 50 50 Z" transform="rotate(72 50 50)"/>
<path d="M50 50 Q34 34 40 14 L50 22 L60 14 Q66 34 50 50 Z" transform="rotate(144 50 50)"/>
<path d="M50 50 Q34 34 40 14 L50 22 L60 14 Q66 34 50 50 Z" transform="rotate(216 50 50)"/>
<path d="M50 50 Q34 34 40 14 L50 22 L60 14 Q66 34 50 50 Z" transform="rotate(288 50 50)"/>
</g>
<circle cx="50" cy="50" r="8" fill="#ff5d8f"/>
<g fill="#ffd23f" stroke-width="1.5"><circle cx="50" cy="38" r="2.5"/><circle cx="61" cy="46" r="2.5"/><circle cx="57" cy="60" r="2.5"/><circle cx="43" cy="60" r="2.5"/><circle cx="39" cy="46" r="2.5"/></g>
"""

ICONS["탬버린"] = """
<circle cx="50" cy="50" r="40" fill="#e9a35b"/>
<circle cx="50" cy="50" r="29" fill="#fff4d6"/>
<g fill="#ffd23f" stroke-width="2.5">
<rect x="42" y="6" width="16" height="12" rx="2"/><rect x="42" y="82" width="16" height="12" rx="2"/>
<rect x="6" y="42" width="12" height="16" rx="2"/><rect x="82" y="42" width="12" height="16" rx="2"/>
<rect x="17" y="17" width="14" height="10" rx="2" transform="rotate(45 24 22)"/><rect x="69" y="73" width="14" height="10" rx="2" transform="rotate(45 76 78)"/>
<rect x="69" y="17" width="14" height="10" rx="2" transform="rotate(-45 76 22)"/><rect x="17" y="73" width="14" height="10" rx="2" transform="rotate(-45 24 78)"/>
</g>
<g fill="none" stroke="#d99a00" stroke-width="2"><circle cx="50" cy="12" r="3"/><circle cx="50" cy="88" r="3"/><circle cx="12" cy="50" r="3"/><circle cx="88" cy="50" r="3"/></g>
<path d="M40 58 L40 42 M40 42 L52 38 L52 54" fill="none" stroke-width="3"/>
<circle cx="37" cy="58" r="4" fill="#2b2b2b"/><circle cx="49" cy="54" r="4" fill="#2b2b2b"/>
"""

ICONS["호박"] = """
<path d="M50 26 Q48 14 56 6" fill="none" stroke="#6b4f1d" stroke-width="7"/>
<ellipse cx="30" cy="58" rx="22" ry="30" fill="#f48c06"/>
<ellipse cx="70" cy="58" rx="22" ry="30" fill="#f48c06"/>
<ellipse cx="50" cy="58" rx="20" ry="32" fill="#faa307"/>
<path d="M60 18 Q76 10 84 22 Q72 26 60 18 Z" fill="#2e7d32" stroke-width="2.5"/>
"""

ICONS["토마토"] = """
<circle cx="50" cy="58" r="36" fill="#e63946"/>
<path d="M50 24 L56 34 L70 30 L62 40 L74 46 L58 44 L50 52 L42 44 L26 46 L38 40 L30 30 L44 34 Z" fill="#2e7d32" stroke-width="2.5"/>
<line x1="50" y1="26" x2="50" y2="12" stroke="#2e7d32" stroke-width="5"/>
<path d="M28 58 Q28 46 36 40" fill="none" stroke="#fff" stroke-width="4"/>
"""

ICONS["필통"] = """
<g transform="rotate(-15 50 50)">
<rect x="6" y="30" width="88" height="40" rx="18" fill="#9b5de5"/>
<line x1="14" y1="40" x2="86" y2="40" stroke-width="3"/>
<g stroke-width="1.5"><line x1="20" y1="37" x2="20" y2="43"/><line x1="28" y1="37" x2="28" y2="43"/><line x1="36" y1="37" x2="36" y2="43"/><line x1="44" y1="37" x2="44" y2="43"/><line x1="52" y1="37" x2="52" y2="43"/><line x1="60" y1="37" x2="60" y2="43"/><line x1="68" y1="37" x2="68" y2="43"/></g>
<rect x="72" y="36" width="10" height="8" rx="2" fill="#ffd23f" stroke-width="2"/>
<path d="M77 44 L77 54" stroke-width="3"/>
<circle cx="30" cy="56" r="5" fill="#fff" stroke-width="2"/>
</g>
"""

ICONS["노란 바구니"] = """
<path d="M10 28 L90 28 L82 90 L18 90 Z" fill="#ffd23f"/>
<rect x="6" y="20" width="88" height="12" rx="3" fill="#ffc300"/>
<rect x="38" y="22" width="24" height="7" rx="3" fill="#fff"/>
<g fill="#e0a800" stroke="none">
<rect x="22" y="40" width="9" height="12" rx="2"/><rect x="36" y="40" width="9" height="12" rx="2"/><rect x="50" y="40" width="9" height="12" rx="2"/><rect x="64" y="40" width="9" height="12" rx="2"/>
<rect x="24" y="58" width="9" height="12" rx="2"/><rect x="37" y="58" width="9" height="12" rx="2"/><rect x="50" y="58" width="9" height="12" rx="2"/><rect x="63" y="58" width="9" height="12" rx="2"/>
<rect x="26" y="76" width="9" height="8" rx="2"/><rect x="38" y="76" width="9" height="8" rx="2"/><rect x="50" y="76" width="9" height="8" rx="2"/><rect x="62" y="76" width="9" height="8" rx="2"/>
</g>
"""

ICONS["훌라후프"] = """
<ellipse cx="50" cy="50" rx="42" ry="42" fill="none" stroke="#2b2b2b" stroke-width="11"/>
<ellipse cx="50" cy="50" rx="42" ry="42" fill="none" stroke="#e63946" stroke-width="7" stroke-dasharray="22 44"/>
<ellipse cx="50" cy="50" rx="42" ry="42" fill="none" stroke="#ffd23f" stroke-width="7" stroke-dasharray="22 44" stroke-dashoffset="22"/>
<ellipse cx="50" cy="50" rx="42" ry="42" fill="none" stroke="#3a86ff" stroke-width="7" stroke-dasharray="22 44" stroke-dashoffset="44"/>
"""

ICONS["메달"] = f"""
<path d="M30 6 L44 6 L56 44 L42 44 Z" fill="#3a86ff"/>
<path d="M70 6 L56 6 L44 44 L58 44 Z" fill="#e63946"/>
<circle cx="50" cy="64" r="28" fill="#ffc300"/>
<circle cx="50" cy="64" r="20" fill="#ffd60a" stroke="#e0a800" stroke-width="3"/>
<text x="50" y="76" text-anchor="middle" font-size="30" fill="#b07d00" stroke="none" {FONT}>1</text>
"""

ICONS["풍선"] = """
<path d="M40 64 Q34 80 44 88 Q52 94 46 100" fill="none" stroke-width="2"/>
<path d="M66 70 Q72 84 62 92 Q56 98 62 100" fill="none" stroke-width="2"/>
<ellipse cx="38" cy="36" rx="24" ry="28" fill="#3a86ff"/>
<path d="M35 63 L41 63 L38 68 Z" fill="#3a86ff" stroke-width="2"/>
<ellipse cx="66" cy="44" rx="20" ry="24" fill="#9b5de5"/>
<path d="M63 67 L69 67 L66 72 Z" fill="#9b5de5" stroke-width="2"/>
<path d="M26 26 Q28 18 36 16" fill="none" stroke="#fff" stroke-width="4"/>
<path d="M56 36 Q58 30 64 28" fill="none" stroke="#fff" stroke-width="3.5"/>
"""


def svg(name, size=None, extra=""):
    attrs = f'width="{size}" height="{size}"' if size else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" {attrs} {extra}>'
        f'<g stroke="{K}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">'
        f"{ICONS[name]}</g></svg>"
    )
