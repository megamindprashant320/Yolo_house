"""Local responsive checks for each design stage. Requires Python Playwright and Chrome."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
from pathlib import Path
import sys
import re
import subprocess
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent.parent
stage=sys.argv[1]
if stage=='all':
    for current in ['home','about','services','contact']:
        subprocess.check_call([sys.executable,__file__,current,*sys.argv[2:]])
    sys.exit(0)
filename={'home':'index.html','about':'about.html','services':'services.html','contact':'contact.html'}[stage]
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith('/Yolo_house/'):
            self.send_error(404);return
        self.path='/'+self.path[len('/Yolo_house/'):]
        super().do_GET()
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/Yolo_house/'
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
        sizes=[(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]
        if '--screenshots-only' in sys.argv:
            sizes=[(1440,900),(375,667)]
        for width,height in sizes:
            context=browser.new_context(viewport={'width':width,'height':height},is_mobile=width<=768,has_touch=width<=768)
            page=context.new_page();errors=[];failed=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('response',lambda r:failed.append(r.url) if r.url.startswith(base) and r.status>=400 else None)
            page.goto(base+filename);page.evaluate('document.fonts.ready');page.wait_for_timeout(850)
            if '--require-fonts' in sys.argv:
                assert page.evaluate('''()=>['Bebas Neue','Poppins'].every(family=>[...document.fonts].some(font=>font.family.replaceAll('"','')===family && font.status==='loaded'))'''), 'Expected Google Fonts did not load'
            page.locator('.studio-section').first.scroll_into_view_if_needed()
            page.wait_for_timeout(900)
            result=page.evaluate('''()=>{
                const sections=[...document.querySelectorAll('.studio-section')];
                const oversized=[...document.querySelectorAll('.studio-section *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.left < -1||r.right>innerWidth+1)}).map(e=>e.tagName+'.'+e.className);
                const cards=[...document.querySelectorAll('.studio-card')];
                return {overflow:document.documentElement.scrollWidth>innerWidth,oversized,cards:cards.length,
                    contained:cards.every(e=>{const r=e.getBoundingClientRect();return [...e.querySelectorAll('h3,p,a')].every(c=>{if(c.closest('details:not([open])'))return true;const b=c.getBoundingClientRect();return (!b.width&&!b.height)||(b.left>=r.left&&b.right<=r.right&&b.top>=r.top&&b.bottom<=r.bottom)})})};
            }''')
            assert not result['overflow'] and not result['oversized'] and result['contained'],result
            if stage=='home':
                assert result['cards']==6
                assert page.locator('.services .text-link').evaluate_all("links=>links.every(a=>a.getAttribute('href')==='services.html')")
                page.locator('.services .text-link').first.click()
                page.wait_for_url(base+'services.html');page.wait_for_load_state('load')
                page.goto(base+filename);page.wait_for_timeout(900)
            if width in [1440,375]:
                (root/'.preview').mkdir(exist_ok=True)
                page.locator('.studio-section').first.scroll_into_view_if_needed()
                page.wait_for_timeout(1000)
                assert page.locator('.studio-section').first.evaluate("e=>Number(getComputedStyle(e).opacity)===1")
                page.locator('.studio-section').first.screenshot(path=str(root/'.preview'/f'{stage}-{width}.png'),style='header,#topBtn,#topBtn.show,#progress-bar,.custom-cursor{visibility:hidden;}')
                if width==1440:
                    for index,element in enumerate(page.locator('.studio-section').all()[1:],2):
                        element.scroll_into_view_if_needed();page.wait_for_timeout(900)
                        element.screenshot(path=str(root/'.preview'/f'{stage}-{width}-{index}.png'),style='header,#topBtn,#topBtn.show,#progress-bar,.custom-cursor{visibility:hidden;}')
            assert not errors,errors
            assert not failed,failed
            print(f'PASS {stage} {width}px: content bounds, horizontal overflow, local assets and JavaScript',flush=True)
            context.close()
        if stage=='home':
            baseline=subprocess.check_output(['git','show','HEAD:index.html'],cwd=root).decode('utf-8')
            current=(root/'index.html').read_text(encoding='utf-8')
            pattern=r'<section class="portfolio".*?</section>'
            assert re.search(pattern,current,re.S)[0]==re.search(pattern,baseline,re.S)[0]
            print('PASS: Featured Projects markup unchanged',flush=True)
        browser.close()
finally:
    server.shutdown();server.server_close()
