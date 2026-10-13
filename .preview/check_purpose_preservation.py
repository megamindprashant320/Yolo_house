from pathlib import Path
import json
b=json.loads(Path('.preview/purpose-baseline.json').read_text(encoding='utf-8'))
css=Path('style.css').read_text(encoding='utf-8');old=b['style.css'];start=old.index('/* About story:');end=old.index('/* About: editorial purpose',start);assert old[start:end] in css
js=Path('main.js').read_text(encoding='utf-8');normalized=js.replace('entry.target.matches(".about-story,.mission-vision")','entry.target.matches(".about-story")');assert normalized.startswith(b['main.js'])
print('PASS exact Our Story CSS and preservation of previous JS except the scoped observer extension')
