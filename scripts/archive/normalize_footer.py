from pathlib import Path
root=Path(__file__).resolve().parent.parent.parent
import json,re
p=(root/'index.html');n=p.read_text(encoding='utf-8-sig');b=json.loads((root/'.preview/footer-baseline.json').read_text(encoding='utf-8'))['index.html'];n=n.rstrip()+b[len(b.rstrip()):];p.write_text(n,encoding='utf-8')
