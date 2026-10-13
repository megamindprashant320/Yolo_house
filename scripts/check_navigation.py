"""Run with Python + Playwright and installed Chrome; serves the GitHub Pages path locally."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PAGES = ['index.html', 'about.html', 'services.html', 'portfolio.html', 'contact.html']

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        self.refs.extend(value for key, value in attrs if key in ['href', 'src'] and value)

def check_path(ref, directory=ROOT):
    url = urlsplit(ref)
    if url.scheme or url.netloc or not url.path:
        return
    assert not url.path.startswith('/'), f'Root-relative path: {ref}'
    current = directory
    for part in Path(unquote(url.path)).parts:
        if part == '..':
            current = current.parent
            assert current == ROOT or ROOT in current.parents, f'Path leaves the project: {ref}'
            continue
        assert part in [item.name for item in current.iterdir()], f'Missing or incorrectly cased path: {ref}'
        current /= part

for filename in PAGES:
    parser = References()
    parser.feed((ROOT / filename).read_text(encoding='utf-8'))
    for ref in parser.refs:
        check_path(ref)
for ref in re.findall(r'url\([\s\"\']*([^\"\')\s]+)', (ROOT / 'assets/css/style.css').read_text(encoding='utf-8')):
    check_path(ref, ROOT / 'assets/css')
print('PASS: local HTML/CSS file references exist, use relative paths and exact filename case', flush=True)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        prefix = '/Yolo_house/'
        if not self.path.startswith(prefix):
            self.send_error(404)
            return
        self.path = '/' + self.path[len(prefix):]
        super().do_GET()
    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}/Yolo_house/'
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
        for width in [1440, 1024, 375, 390, 430]:
            mobile = width <= 992
            context = browser.new_context(viewport={'width':width, 'height':900}, is_mobile=mobile, has_touch=mobile)
            # The embedded external map is outside the local deployment asset checks.
            context.route('https://www.google.com/maps**', lambda route:route.abort())
            page = context.new_page()
            errors, failed = [], []
            page.on('pageerror', lambda e:errors.append(str(e)))
            page.on('response', lambda r:failed.append((r.url, r.status)) if r.url.startswith(base) and r.status >= 400 else None)
            page.on('requestfailed', lambda r:failed.append((r.url, r.failure)) if r.url.startswith(base) else None)
            page.goto(base + PAGES[0])
            for index, filename in enumerate(PAGES):
                page.wait_for_load_state('load')
                page.locator('img').evaluate_all("images=>images.forEach(img=>img.loading='eager')")
                page.wait_for_function('Array.from(document.images).every(img=>img.complete && img.naturalWidth>0)')
                page.evaluate('document.fonts.ready')
                page.wait_for_timeout(800)
                assert page.url == base + filename, page.url
                assert page.locator('nav a.active').count() == 1
                active = page.locator('nav a[aria-current="page"]')
                assert active.count() == 1 and active.get_attribute('href') == filename
                assert page.locator('nav a').evaluate_all('(links)=>links.map(a=>a.getAttribute("href"))') == PAGES
                assert page.evaluate('Array.from(document.images).every(img=>img.complete && img.naturalWidth>0)')
                for position in [0, 400, 1100]:
                    page.evaluate("y=>{document.documentElement.style.scrollBehavior='auto';window.scrollTo(0,y)}", position)
                    page.wait_for_timeout(400)
                    assert page.locator('nav a.active').get_attribute('href') == filename
                    if mobile:
                        toggle = page.locator('.menu-toggle')
                        assert toggle.evaluate('''e=>{const r=e.getBoundingClientRect(); const s=getComputedStyle(e);return r.width>0 && r.top>=0 && s.visibility==='visible' && e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}''')
                        assert toggle.locator('span').evaluate_all('''bars=>bars.every(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0 && r.height===3 && s.opacity==='1' && s.backgroundColor==='rgb(255, 255, 255)'})''')
                        toggle.tap()
                        page.wait_for_timeout(850)
                        assert page.locator('nav a').first.evaluate('''e=>{const r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e}''')
                        if position == 0:
                            toggle.tap()
                        elif position == 400:
                            page.keyboard.press('Escape')
                        else:
                            page.locator('.nav-overlay').tap(position={'x':10,'y':300})
                        assert toggle.get_attribute('aria-expanded') == 'false'
                        assert not page.evaluate("document.body.classList.contains('menu-open')")
                    else:
                        assert not page.locator('.menu-toggle').is_visible()
                        assert page.locator('nav a').first.is_visible()
                next_file = PAGES[(index + 1) % len(PAGES)]
                if mobile:
                    page.locator('.menu-toggle').tap()
                page.locator(f'nav a[href="{next_file}"]').click()
                page.wait_for_url(base + next_file)
            page.wait_for_load_state('load')
            assert not errors, errors
            assert not failed, failed
            print(f'PASS {width}px: Home -> About -> Services -> Portfolio -> Contact -> Home; page highlighting, scrolling, menu behavior and local assets', flush=True)
            context.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()
