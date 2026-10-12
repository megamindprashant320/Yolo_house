from pathlib import Path
import json,re
p=Path('index.html');n=p.read_text(encoding='utf-8-sig');b=json.loads(Path('.preview/footer-baseline.json').read_text(encoding='utf-8'))['index.html'];n=n.rstrip()+b[len(b.rstrip()):];p.write_text(n,encoding='utf-8')
