from pathlib import Path
p=Path('style.css');s=p.read_text(encoding='utf-8');s=s.replace('.footer-bottom{gap:12px;}.footer-wordmark','.footer-bottom{gap:12px;padding-right:64px;}.footer-wordmark');p.write_text(s,encoding='utf-8')
p=Path('.preview/check_footer_remaining.py');s=p.read_text(encoding='utf-8-sig').replace('[(768,1024),(430,932),(390,844),(375,667)]','[(375,667)]');p=Path('.preview/check_footer_final.py');p.write_text(s,encoding='utf-8')
