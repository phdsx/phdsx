"""Build a standalone local preview of README.md; no packages or web server needed."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
content = (root / "README.md").read_text(encoding="utf-8")
page = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>phdsx · GitHub 主页预览</title>
<style>
:root{color-scheme:light;--bg:#f6f8fa;--card:#fff;--text:#1f2328;--muted:#656d76;--line:#d0d7de;--link:#6554ad}
html.dark{color-scheme:dark;--bg:#0d1117;--card:#0d1117;--text:#e6edf3;--muted:#8b949e;--line:#30363d;--link:#b6a9fa}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif}a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
.toolbar{max-width:1040px;margin:24px auto 12px;padding:0 24px;display:flex;align-items:center;justify-content:space-between;gap:16px}.toolbar small{color:var(--muted)}button{border:1px solid var(--line);background:var(--card);color:var(--text);padding:8px 14px;border-radius:8px;cursor:pointer}
main{max-width:1012px;margin:0 auto 40px;border:1px solid var(--line);border-radius:10px;background:var(--card);padding:32px}.repo{font:12px ui-monospace,monospace;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:18px;margin-bottom:24px}
img{max-width:100%;height:auto;vertical-align:middle}h2{font-size:23px;line-height:1.4;padding-bottom:9px;border-bottom:1px solid var(--line);margin:30px 0 18px}h3{font-size:18px;line-height:1.4;margin:20px 0 14px}p{margin:0 0 16px}table{border-collapse:collapse;max-width:100%;width:100%;margin-bottom:16px}td{border:1px solid var(--line);padding:12px 16px}td h3:first-child{margin-top:8px}code{font:12px ui-monospace,monospace;background:var(--bg);padding:3px 6px;border-radius:4px}sub{font-size:12px;color:var(--muted)}li{margin:8px 0}
@media(max-width:650px){body{font-size:14px}main{border-radius:0;padding:18px;border-left:0;border-right:0}.toolbar{margin:14px auto;padding:0 18px}.toolbar small{display:none}h2{font-size:20px}td{padding:10px}td h3{font-size:15px;word-break:break-word}img[align="right"]{width:90px}}
</style></head><body><div class="toolbar"><div><strong>phdsx / phdsx</strong> <small>README 本地预览</small></div><button id="theme" type="button">切换为深色</button></div><main><div class="repo">README.md</div>''' + content + '''</main>
<script>
const root=document.documentElement; const button=document.querySelector('#theme');
function setTheme(dark){root.classList.toggle('dark',dark);document.querySelectorAll('picture').forEach(p=>{const target=[...p.querySelectorAll('source')].find(s=>(s.dataset.original||s.media).includes(dark?'dark':'light'));if(target)p.querySelector('img').src=target.srcset;p.querySelectorAll('source').forEach(s=>{if(!s.dataset.original)s.dataset.original=s.media;s.media='not all'})});button.textContent=dark?'切换为浅色':'切换为深色';localStorage.setItem('phdsx-preview-theme',dark?'dark':'light')}
button.addEventListener('click',()=>setTheme(!root.classList.contains('dark')));setTheme(localStorage.getItem('phdsx-preview-theme')==='dark');
</script></body></html>'''
(root / "preview.html").write_text(page, encoding="utf-8")
print("Created preview.html")
