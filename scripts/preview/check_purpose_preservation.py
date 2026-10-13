from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent.parent
b=json.loads((root/'.preview/purpose-baseline.json').read_text(encoding='utf-8'))
css=(root/'assets/css/style.css').read_text(encoding='utf-8');old=b['style.css'];start=old.index('/* About story:');end=old.index('/* About: editorial purpose',start);assert old[start:end] in css
js=(root/'assets/js/main.js').read_text(encoding='utf-8');normalized=js.replace('entry.target.matches(".about-story,.mission-vision")','entry.target.matches(".about-story")');assert normalized.startswith(b['main.js'])
print('PASS exact Our Story CSS and preservation of previous JS except the scoped observer extension')
