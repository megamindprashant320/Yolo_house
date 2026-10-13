from pathlib import Path
import json,re,hashlib
root=Path(__file__).resolve().parent.parent.parent
b=json.loads((root/'.preview/cta-baseline.json').read_text(encoding='utf-8'));now=(root/'index.html').read_text(encoding='utf-8')
for cls in ['hero','services','portfolio','home-approach']:
 pattern=r'<section class="'+cls+r'(?: [^"]*)?"[^>]*>.*?</section>'
 assert re.search(pattern,now,re.S)[0]==re.search(pattern,b['index.html'],re.S)[0],cls
for tag in ['header','footer','dialog']:
 pattern='<'+tag+r'[^>]*>.*?</'+tag+'>'
 assert re.search(pattern,now,re.S)[0]==re.search(pattern,b['index.html'],re.S)[0],tag
for name,digest in b['pages'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
for name,digest in b['assets'].items():assert hashlib.sha256((root/'assets/images'/name).read_bytes()).hexdigest()==digest
print('PASS preserved sections, other pages and images')


