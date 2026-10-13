"""Trust section checks, scoped preservation assertions and existing viewer regression."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
import hashlib,json,re,sys
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent.parent
baseline=json.loads((root/'.preview/trust-baseline.json').read_text(encoding='utf-8'))
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith('/Yolo_house/'):
            self.send_error(404);return
        self.path='/'+self.path[len('/Yolo_house/'):];super().do_GET()
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/Yolo_house/'
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
        for width,height in [(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]:
            context=browser.new_context(viewport={'width':width,'height':height},is_mobile=width<=768,has_touch=width<=768)
            if '--require-fonts' not in sys.argv:context.route('https://fonts.googleapis.com/**',lambda r:r.abort())
            page=context.new_page();errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(base+'index.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(850)
            if '--require-fonts' in sys.argv:
                assert page.evaluate('''()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(font=>font.family.replaceAll('"','')===f&&font.status==='loaded'))''')
            section=page.locator('.home-approach')
            before=section.evaluate('e=>e.offsetHeight')
            section.scroll_into_view_if_needed();page.wait_for_timeout(900)
            assert section.evaluate("e=>e.classList.contains('is-in-view')")
            assert section.evaluate('e=>e.offsetHeight')==before
            # Isolate the new entrance animation from the existing header/hero resizing on scroll.
            following=page.locator('#services').evaluate('e=>e.offsetTop')
            section.evaluate("e=>e.classList.remove('is-in-view')")
            page.wait_for_timeout(100)
            section.evaluate("e=>e.classList.add('is-in-view')")
            page.wait_for_timeout(900)
            assert page.locator('#services').evaluate('e=>e.offsetTop')==following
            steps=section.locator('details')
            assert steps.count()==4 and page.locator('#about .stats').count()==0
            assert page.locator('.hero-stats h3').all_text_contents()==['18+','100+','50+']
            for index,step in enumerate(steps.all()):
                if step.get_attribute('open') is None:
                    if width<=768:step.locator('summary').tap()
                    else:step.locator('summary').click()
                page.wait_for_timeout(450)
                assert step.get_attribute('open') is not None
                assert section.locator('details[open]').count()==1
                assert step.locator('.approach-detail').is_visible()
                assert section.locator('.approach-node.is-active').count()==index+1
                assert section.locator('.approach-status').inner_text().startswith(f'{index+1:02} / ')
                assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
                assert section.evaluate('''section=>[...section.querySelectorAll('h2,p,summary,svg')].every(e=>{
                    if(e.closest('details:not([open])')&&!e.closest('summary'))return true;
                    const r=e.getBoundingClientRect(),b=section.getBoundingClientRect();
                    return r.left>=b.left && r.right<=b.right && r.top>=b.top && r.bottom<=b.bottom;
                })''')
                # Summary and expanded prose occupy distinct vertical regions.
                assert step.evaluate("e=>e.querySelector('.approach-detail').getBoundingClientRect().top>=e.querySelector('summary').getBoundingClientRect().bottom")
                step.locator('summary').focus();page.keyboard.press('Space')
                page.wait_for_timeout(50);assert step.get_attribute('open') is None
                page.keyboard.press('Enter');page.wait_for_timeout(50);assert step.get_attribute('open') is not None
            if width in [1440,375]:
                page.locator('header').evaluate('e=>e.style.visibility="hidden"')
                section.screenshot(path=str(root/'.preview'/f'trust-{width}.png'))
                page.locator('header').evaluate('e=>e.style.visibility=""')
            # Regression: actual gallery click, navigation and scroll/focus restoration.
            trigger=page.locator('.project-trigger').first
            trigger.scroll_into_view_if_needed();page.wait_for_timeout(850)
            y=page.evaluate('scrollY');trigger.click()
            page.wait_for_function("document.querySelector('#project-lightbox').dataset.state==='ready'")
            assert page.locator('.viewer-counter').inner_text()=='01 / 06'
            page.keyboard.press('ArrowRight')
            page.wait_for_function("document.querySelector('.viewer-counter').textContent==='02 / 06'&&document.querySelector('#project-lightbox').dataset.state==='ready'")
            page.keyboard.press('Escape');page.wait_for_timeout(100)
            assert abs(page.evaluate('scrollY')-y)<=1
            assert trigger.evaluate('e=>document.activeElement===e')
            if width<=768:
                page.locator('.menu-toggle').tap();assert page.locator('nav').evaluate("e=>e.classList.contains('active')")
                page.keyboard.press('Escape');assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
            else:
                assert page.locator('nav a').first.is_visible()
            assert not errors,errors
            print(f'PASS {width}px: content bounds, selection/graphic, keyboard/touch, no entrance layout shift, lightbox/navbar regression',flush=True)
            context.close()
        for options in [{'java_script_enabled':False},{'reduced_motion':'reduce'}]:
            context=browser.new_context(viewport={'width':390,'height':844},**options)
            context.route('https://fonts.googleapis.com/**',lambda r:r.abort())
            page=context.new_page();page.goto(base+'index.html');page.wait_for_timeout(850)
            section=page.locator('.home-approach');section.scroll_into_view_if_needed()
            section.locator('summary').nth(1).click()
            assert section.locator('.approach-detail').nth(1).is_visible()
            if 'reduced_motion' in options:
                assert section.locator('.approach-progress').evaluate("e=>getComputedStyle(e).transitionDuration==='0s'")
                assert section.locator('.approach-step').first.evaluate("e=>getComputedStyle(e).opacity==='1'")
            context.close()
        browser.close()
    current=(root/'index.html').read_text(encoding='utf-8')
    for cls in ['hero','services','portfolio','cta']:
        pattern=r'<section class="'+cls+r'(?: [^"]*)?"[^>]*>.*?</section>'
        assert re.search(pattern,current,re.S)[0]==re.search(pattern,baseline['index.html'],re.S)[0],cls
    for tag in ['header','footer','dialog']:
        pattern='<'+tag+r'[^>]*>.*?</'+tag+'>'
        assert re.search(pattern,current,re.S)[0]==re.search(pattern,baseline['index.html'],re.S)[0],tag
    original_viewer=re.search(r'function initProjectLightbox\(\).*?initProjectLightbox\(\);',baseline['main.js'],re.S)[0]
    assert original_viewer in (root/'assets/js/main.js').read_text(encoding='utf-8')
    for filename,digest in baseline['other_pages'].items():assert hashlib.sha256((root/filename).read_bytes()).hexdigest()==digest
    assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'assets/images').iterdir() if p.is_file()}==baseline['assets']
    print('PASS: no-JS and reduced motion; hero/services/gallery/lightbox/header/footer, other pages and all assets unchanged',flush=True)
finally:
    server.shutdown();server.server_close()
