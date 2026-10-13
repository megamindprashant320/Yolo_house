from pathlib import Path
root=Path(__file__).resolve().parent.parent.parent
p=(root/'assets/css/style.css');s=p.read_text(encoding='utf-8');s=s.replace('.footer-bottom{gap:12px;}.footer-wordmark','.footer-bottom{gap:12px;padding-right:64px;}.footer-wordmark');p.write_text(s,encoding='utf-8')
p=(root/'scripts/preview/check_footer_remaining.py');s=p.read_text(encoding='utf-8-sig').replace('[(768,1024),(430,932),(390,844),(375,667)]','[(375,667)]');p=(root/'scripts/preview/check_footer_final.py');p.write_text(s,encoding='utf-8')
