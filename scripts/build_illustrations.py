"""Create original, editable SVG decoration. No downloaded illustration assets."""
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "assets" / "illustrations"
root.mkdir(parents=True, exist_ok=True)


def write(name, width, height, title, body, styles=""):
    source = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{title}">
<title>{title}</title><style>text{{font-family:Arial,"Microsoft YaHei",sans-serif}}{styles}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>{body}</svg>'''
    (root / (name + ".svg")).write_text(source + "\n", encoding="utf-8")


write("welcome", 540, 74, "Hello, World! 你好，我是 phdsx。欢迎来到我的 GitHub。", '''
<defs><clipPath id="typing"><rect x="30" y="0" width="480" height="45" class="reveal"/></clipPath></defs>
<g clip-path="url(#typing)"><text x="270" y="34" text-anchor="middle" font-size="25" font-weight="700" fill="#9280e8">Hello, World! 你好，我是 phdsx。</text></g>
<text x="270" y="65" text-anchor="middle" font-size="13" letter-spacing="3" fill="#8996b1">WELCOME TO MY GITHUB SPACE</text>
''', '.reveal{animation:type 6s steps(32,end) infinite}@keyframes type{0%,8%{width:0}55%,100%{width:480px}}')

write("developer", 700, 350, "A coding robot at a desk under a starry sky", '''
<defs><linearGradient id="panel" x2="1" y2="1"><stop stop-color="#1d2946"/><stop offset="1" stop-color="#302750"/></linearGradient></defs>
<ellipse cx="354" cy="326" rx="276" ry="15" fill="#8f83c3" opacity=".12"/>
<rect x="58" y="22" width="584" height="264" rx="24" fill="url(#panel)"/>
<g fill="#b0a3e4" opacity=".35"><circle cx="89" cy="97" r="2"/><circle cx="614" cy="181" r="2"/><circle cx="340" cy="58" r="2"/><path d="M577 49v12m-6-6h12" stroke="#b0a3e4" stroke-width="2"/></g>
<rect x="90" y="57" width="193" height="152" rx="12" fill="#111c31" stroke="#596389"/>
<circle cx="104" cy="69" r="3" fill="#f49a9a"/><circle cx="115" cy="69" r="3" fill="#f0d28c"/><circle cx="126" cy="69" r="3" fill="#89d4b0"/>
<g stroke-linecap="round" stroke-width="6" class="code"><path d="M110 96h63m-63 18h29m10 0h86m-112 18h77m-90 18h38m10 0h77m-112 18h49" stroke="#9f8edd"/><path d="M183 96h55m-28 36h40m-65 36h44" stroke="#77cbcc"/></g>
<rect x="111" y="184" width="60" height="5" rx="2" fill="#77cbcc" class="cursor"/>
<g class="float"><rect x="473" y="77" width="124" height="79" rx="10" fill="#1a253e" stroke="#736294"/><text x="534" y="126" text-anchor="middle" font-family="monospace" font-size="29" font-weight="700" fill="#a8e3da">&lt; / &gt;</text></g>
<path d="M332 260v55m91-55v55" stroke="#4a547c" stroke-width="13"/>
<path d="M321 312h35m48 0h32" stroke="#a49acd" stroke-width="11" stroke-linecap="round"/>
<rect x="319" y="174" width="118" height="93" rx="28" fill="#8f83c9"/>
<rect x="332" y="188" width="92" height="57" rx="18" fill="#b7ace4"/>
<path d="M321 195l-32 45h-33m177-45 30 45h31" stroke="#a69ad7" stroke-width="15" stroke-linecap="round" fill="none"/>
<g class="head"><rect x="320" y="95" width="114" height="87" rx="29" fill="#d7d8f2"/><rect x="332" y="113" width="90" height="49" rx="17" fill="#24314f"/><g fill="#88dfd3"><rect x="349" y="128" width="10" height="13" rx="5"/><rect x="394" y="128" width="10" height="13" rx="5"/></g><path d="M367 146q10 7 20 0" fill="none" stroke="#88dfd3" stroke-width="3" stroke-linecap="round"/><path d="M377 95V77" stroke="#a6a4d4" stroke-width="4"/><circle cx="377" cy="73" r="6" fill="#88dfd3"/></g>
<rect x="158" y="248" width="408" height="14" rx="7" fill="#b6a6d2"/><path d="M183 263v54m356-54v54" stroke="#7b749b" stroke-width="9"/>
<rect x="230" y="234" width="90" height="12" rx="5" fill="#657392"/><path d="M240 238h70" stroke="#aabbd4" stroke-dasharray="3 3"/>
<path d="M491 218h26v26h-26z" fill="#8ad5cf"/><path d="M517 223h8v12h-8" stroke="#8ad5cf" stroke-width="4" fill="none"/>
<path d="M578 275h38l-6 40h-26z" fill="#8e81b7"/><path d="M597 281v-69m0 29q-36-4-29-28 24-4 29 28m0 18q32-6 29-29-25 0-29 29" fill="#70b3a7" stroke="#70b3a7" stroke-width="3"/>
''', '.float{animation:float 4s ease-in-out infinite}.head{animation:nod 5s ease-in-out infinite;transform-origin:377px 177px}.cursor{animation:blink 1.2s steps(2,end) infinite}.code{animation:glow 4s ease-in-out infinite}@keyframes float{50%{transform:translateY(-9px)}}@keyframes nod{50%{transform:rotate(3deg)}}@keyframes blink{50%{opacity:0}}@keyframes glow{50%{opacity:.6}}')

write("astronaut", 180, 200, "A small floating astronaut", '''
<g class="float"><path d="M61 69l-18 49m88-49 19 33m-12 1 12-1 4-14" fill="none" stroke="#c6c4df" stroke-width="15" stroke-linecap="round"/>
<rect x="60" y="61" width="69" height="85" rx="24" fill="#dcdced"/>
<path d="M78 138l-7 36m40-36 6 36" stroke="#c6c4df" stroke-width="20" stroke-linecap="round"/>
<circle cx="95" cy="49" r="37" fill="#dedfee"/><rect x="67" y="29" width="56" height="38" rx="18" fill="#354363"/>
<path d="M80 37h20" stroke="#b8c9e3" opacity=".6" stroke-width="5" stroke-linecap="round"/>
<rect x="78" y="90" width="34" height="25" rx="5" fill="#9f90ce"/><circle cx="87" cy="102" r="3" fill="#8ce0ce"/><path d="M96 101h8m-8 6h6" stroke="#e0d9f2" stroke-width="2"/>
</g><g fill="#aa9bd4"><circle cx="35" cy="42" r="3"/><circle cx="146" cy="154" r="3"/><path d="M150 36v12m-6-6h12" stroke="#aa9bd4" stroke-width="2"/></g>
''', '.float{animation:f 5s ease-in-out infinite}@keyframes f{50%{transform:translateY(9px) rotate(3deg);transform-origin:center}}')

write("runner", 250, 200, "A little robot in motion", '''
<ellipse cx="127" cy="180" rx="84" ry="7" fill="#9b8dbd" opacity=".12"/>
<g class="bounce"><path d="M114 118l-29 28-34-5m76-18 22 28 39 12" stroke="#a7a0d1" stroke-width="13" fill="none" stroke-linecap="round"/>
<path d="M114 88L83 77 66 92m65 1 29 22 23-7" stroke="#ab9cda" stroke-width="11" fill="none" stroke-linecap="round"/>
<rect x="99" y="76" width="42" height="55" rx="16" fill="#a996d8" transform="rotate(13 120 100)"/>
<rect x="102" y="30" width="54" height="48" rx="17" fill="#d8d9ee"/><rect x="112" y="43" width="39" height="22" rx="10" fill="#354363"/><circle cx="132" cy="53" r="3" fill="#8fdbd4"/><circle cx="143" cy="53" r="3" fill="#8fdbd4"/><path d="M129 30V20" stroke="#a995d3" stroke-width="3"/><circle cx="129" cy="17" r="4" fill="#82ccc7"/>
</g><g stroke="#ac9ad7" stroke-width="3" stroke-linecap="round" opacity=".5"><path d="M46 109h28m-40 13h22m-8-25h13"/></g>
''', '.bounce{animation:run .8s ease-in-out infinite}@keyframes run{50%{transform:translateY(-7px) rotate(3deg);transform-origin:center}}')

write("orbit", 260, 220, "A tiny orbit of ideas", '''
<g fill="none" stroke="#a89acf" opacity=".55"><ellipse cx="130" cy="110" rx="106" ry="42" transform="rotate(-28 130 110)"/><ellipse cx="130" cy="110" rx="106" ry="42" transform="rotate(28 130 110)"/></g>
<circle cx="130" cy="110" r="45" fill="#b3a3db"/><path d="M108 92l-12 18 12 18m44-36 12 18-12 18m-17-41-10 46" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
<g class="orbit"><circle cx="222" cy="110" r="9" fill="#7ccdc0"/><circle cx="42" cy="110" r="5" fill="#e5b484"/></g>
<g fill="#b8a8d7"><circle cx="43" cy="39" r="2"/><circle cx="223" cy="169" r="2"/><circle cx="180" cy="26" r="3"/></g>
''', '.orbit{animation:spin 14s linear infinite;transform-origin:130px 110px}@keyframes spin{to{transform:rotate(360deg)}}')

write("divider", 1000, 34, "Decorative divider", '''
<defs><linearGradient id="g"><stop stop-color="#8e83bf" stop-opacity="0"/><stop offset=".5" stop-color="#a697d5"/><stop offset="1" stop-color="#8e83bf" stop-opacity="0"/></linearGradient></defs>
<path d="M0 17h475m50 0h475" stroke="url(#g)" stroke-width="2"/><path d="M500 8l9 9-9 9-9-9z" fill="#a697d5"/>
''')

write("language-tiles", 680, 146, "JavaScript, Python, HTML and Jupyter Notebook appear in phdsx's public repositories", '''
<g transform="translate(6 6)"><rect width="150" height="130" rx="17" fill="#f0d967"/><text x="75" y="73" text-anchor="middle" font-size="39" font-weight="700" fill="#50451c">JS</text><text x="75" y="109" text-anchor="middle" font-size="13" fill="#50451c">JavaScript</text></g>
<g transform="translate(178 6)"><rect width="150" height="130" rx="17" fill="#8bbfdc"/><path d="M55 31h35q10 0 10 10v24H64q-9 0-9 9H43V50q0-10 12-10m40 53H60q-10 0-10-10V59h36q9 0 9-9h12v24q0 10-12 10" fill="#e8f0fa"/><circle cx="85" cy="40" r="3" fill="#65849f"/><circle cx="65" cy="84" r="3" fill="#65849f"/><text x="75" y="110" text-anchor="middle" font-size="13" fill="#294d68">Python</text></g>
<g transform="translate(350 6)"><rect width="150" height="130" rx="17" fill="#ecab91"/><text x="75" y="73" text-anchor="middle" font-size="32" font-weight="700" fill="#743d2c">&lt;/&gt;</text><text x="75" y="109" text-anchor="middle" font-size="13" fill="#743d2c">HTML</text></g>
<g transform="translate(522 6)"><rect width="150" height="130" rx="17" fill="#c1afe1"/><ellipse cx="75" cy="59" rx="31" ry="24" fill="none" stroke="#f7f1ff" stroke-width="5"/><circle cx="105" cy="30" r="6" fill="#796894"/><circle cx="48" cy="84" r="4" fill="#796894"/><text x="75" y="109" text-anchor="middle" font-size="12" fill="#514166">Jupyter Notebook</text></g>
''')

for name, label, width, fill in [
    ("github-badge", "GitHub · phdsx", 154, "#655488"),
    ("repositories-badge", "Explore repositories →", 194, "#376b78"),
    ("stars-badge", "Starred repositories ☆", 192, "#916c48"),
]:
    write(name, width, 28, label, f'<rect width="{width}" height="28" rx="7" fill="{fill}"/><text x="{width/2}" y="18" text-anchor="middle" font-size="12" fill="#fff">{label}</text>')

print("Created 10 original SVG illustrations and badges")
