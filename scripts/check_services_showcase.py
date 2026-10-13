"""Local Chrome checks for Services Step 1; serves relative URLs under /Yolo_house/."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
import hashlib, html, json, re, sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASELINE = json.loads((ROOT / '.preview/services-showcase-baseline.json').read_text(encoding='utf-8'))
original = re.search(r'<section class="services-page.*?</section>', BASELINE['services.html'], re.S)[0]
SERVICES = []
for article in re.findall(r'<article.*?</article>', original, re.S):
    SERVICES.append({
        'id': re.search(r'id="([^"]+)"', article)[1],
        'title': html.unescape(re.search(r'<h3>(.*?)</h3>', article, re.S)[1]),
        'description': html.unescape(re.search(r'<p>(.*?)</p>', article, re.S)[1]),
        'link': re.search(r'<a .*?</a>', article, re.S)[0]
    })
assert len(SERVICES) == 6

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Chrome also probes the origin favicon; it is outside this subpath test.
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return
        if not self.path.startswith('/Yolo_house/'):
            self.send_error(404)
            return
        self.path = '/' + self.path[len('/Yolo_house/'):]
        try:
            super().do_GET()
        except (ConnectionResetError, BrokenPipeError):
            pass  # Closing a context cancels outstanding image requests.
    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
Thread(target=server.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{server.server_port}/Yolo_house/'
sizes = [(1440, 900), (1024, 768), (768, 1024), (430, 932), (390, 844), (375, 667)]
fallback_only = '--fallback-only' in sys.argv
preview_only = '--preview-only' in sys.argv
if fallback_only:
    sizes = []

def load(page, name='services.html', fonts=True):
    page.set_default_navigation_timeout(60000)
    page.goto(BASE + name)
    page.evaluate('document.fonts.ready')
    if fonts:
        assert page.evaluate("""()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(t=>t.family.replaceAll('"','')===f&&t.status==='loaded'))"""), 'Existing fonts did not load'
    page.wait_for_timeout(900)

def active_is(section, i):
    assert section.locator(f'#service-tab-{i}').get_attribute('aria-selected') == 'true'
    assert section.locator('.service-presentation.is-active').count() == 1
    panel = section.locator('.service-presentation').nth(i)
    assert panel.is_visible() and panel.get_attribute('aria-hidden') == 'false'
    assert panel.locator('h3').inner_text() == SERVICES[i]['title']
    assert panel.locator('p').inner_text() == SERVICES[i]['description']
    assert panel.get_attribute('id') == SERVICES[i]['id']
    assert panel.locator('a').get_attribute('href') == 'contact.html'
    assert panel.locator('a').evaluate('e=>e.outerHTML') == SERVICES[i]['link']
    assert section.locator('.service-presentation').evaluate_all('es=>es.filter(e=>!e.inert).length') == 1
    assert section.locator('.service-selector button').evaluate_all('es=>es.filter(e=>e.tabIndex===0).length') == 1

def no_overflow(page):
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'), 'Horizontal page overflow'

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
    if preview_only:
        for width,height in [sizes[0],sizes[-1]]:
            ctx=browser.new_context(viewport={'width':width,'height':height},is_mobile=width<=768,has_touch=width<=768)
            page=ctx.new_page()
            load(page)
            section=page.locator('.services-showcase')
            section.scroll_into_view_if_needed()
            page.wait_for_timeout(800)
            section.screenshot(path=str(ROOT/'.preview'/f'services-showcase-{width}.png'),style='body > header,body .custom-cursor,body #topBtn,body #progress-bar{display:none;}')
            page.locator('.service-stage').scroll_into_view_if_needed()
            page.wait_for_timeout(800)
            page.screenshot(path=str(ROOT/'.preview'/f'services-viewport-{width}.png'))
            ctx.close()
        browser.close()
        server.shutdown()
        print('Saved component previews (fixed controls hidden only during capture) and unmodified viewport screenshots',flush=True)
        sys.exit(0)
    for width, height in sizes:
        ctx = browser.new_context(viewport={'width': width, 'height': height}, is_mobile=width<=768, has_touch=width<=768)
        page = ctx.new_page()
        errors, bad_responses, console_errors = [], [], []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('response', lambda r: bad_responses.append(r.url) if r.url.startswith(BASE) and r.status>=400 else None)
        page.on('console', lambda m: console_errors.append(m.text) if m.type=='error' else None)
        load(page)
        section = page.locator('.services-showcase')
        section.scroll_into_view_if_needed()
        page.wait_for_timeout(700)
        buttons, panels = section.locator('[role="tab"]'), section.locator('[role="tabpanel"]')
        active_is(section, 0)
        assert buttons.count() == panels.count() == 6
        assert section.locator('[role="tablist"]').get_attribute('aria-orientation') == ('horizontal' if width<=768 else 'vertical')
        height_before = section.evaluate('e=>e.offsetHeight')
        following_before = page.locator('.work-process').evaluate('e=>e.offsetTop')
        graphics = []
        for i in range(6):
            if width<=768:
                buttons.nth(i).tap()
            else:
                buttons.nth(i).click()
            page.wait_for_timeout(500)
            active_is(section, i)
            panel = panels.nth(i)
            assert panel.locator('.service-presentation-number').inner_text() == f'{i+1:02}'
            assert section.evaluate('e=>e.offsetHeight') == height_before
            assert page.locator('.work-process').evaluate('e=>e.offsetTop') == following_before
            no_overflow(page)
            assert panel.evaluate('s=>[...s.querySelectorAll("h3,p,svg,a,.service-presentation-number")].every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom})'), f'Panel bounds at {width}px: {i}'
            assert panel.evaluate('s=>[...s.querySelectorAll("h3,p")].every(e=>e.scrollWidth<=e.clientWidth)'), f'Text glyph overflow at {width}px: {i}'
            assert buttons.nth(i).evaluate('e=>e.scrollWidth<=e.clientWidth'), f'Selector glyph overflow at {width}px: {i}'
            assert panel.evaluate('s=>{let p=s.querySelector("p").getBoundingClientRect(),g=s.querySelector(".service-scene").getBoundingClientRect(),a=s.querySelector("a").getBoundingClientRect();return p.bottom<=g.top&&g.bottom<=a.top;}')
            assert panel.evaluate('s=>{let t=s.querySelector("h3").getBoundingClientRect(),n=s.querySelector(".service-presentation-number").getBoundingClientRect();return t.right<=n.left;}')
            assert buttons.nth(i).bounding_box()['height']>=44 and panel.locator('a').bounding_box()['height']>=44
            assert panel.locator('path').evaluate('e=>e.getAnimations().every(a=>a.playState==="finished")')
            graphics.append(panel.locator('path').get_attribute('d'))
            assert panel.locator('.service-scene').get_attribute('aria-hidden') == 'true'
            if width>768:
                track = section.locator('.service-selection-track').bounding_box()
                indicator = section.locator('.service-selection-track i').bounding_box()
                assert abs(indicator['y'] - (track['y']+track['height']*i/6))<1
            else:
                assert buttons.nth(i).evaluate('e=>getComputedStyle(e).borderBottomColor==="rgb(212, 175, 55)"')
        assert len(set(graphics)) == 6
        page.wait_for_timeout(700)
        active_is(section, 5)  # No automatic cycling.
        page.keyboard.press('Tab')
        buttons.nth(5).focus()
        assert buttons.nth(5).evaluate('e=>e.matches(":focus-visible")&&getComputedStyle(e).outlineStyle==="solid"')
        page.keyboard.press('Home')
        active_is(section, 0)
        assert page.evaluate('scrollY')>0, 'Tabs Home leaked to global page shortcut'
        page.keyboard.press('End')
        active_is(section, 5)
        page.keyboard.press('ArrowRight' if width<=768 else 'ArrowDown')
        active_is(section, 0)
        page.keyboard.press('ArrowLeft' if width<=768 else 'ArrowUp')
        active_is(section, 5)
        if width<=768:
            page.keyboard.press('ArrowUp')
            active_is(section, 3)
            page.keyboard.press('ArrowDown')
            active_is(section, 5)
        page.keyboard.press('Tab')
        assert panels.nth(5).evaluate('e=>document.activeElement===e')
        page.keyboard.press('Tab')
        assert panels.nth(5).locator('a').evaluate('e=>document.activeElement===e')
        assert panels.nth(5).locator('a').evaluate('e=>getComputedStyle(e).outlineStyle==="solid"')
        stage = section.locator('.service-stage')
        panels.nth(5).scroll_into_view_if_needed()
        page.wait_for_timeout(700)
        if width>768:
            page.mouse.move(1, 1)
            panels.nth(5).hover()
            page.wait_for_function('document.querySelector(".service-stage").style.getPropertyValue("--service-light-x")!==""')
            if width==1440:
                page.emulate_media(reduced_motion='reduce')
                page.wait_for_function('document.querySelector(".service-stage").style.getPropertyValue("--service-light-x")===""')
                assert panels.nth(5).locator('path').evaluate('e=>getComputedStyle(e).animationName==="none"')
                page.emulate_media(reduced_motion='no-preference')
            page.mouse.move(1, 1)
            assert stage.evaluate('e=>!e.style.getPropertyValue("--service-light-x")')
        else:
            assert stage.evaluate('e=>!e.style.getPropertyValue("--service-light-x")')
        if width in [1440,375]:
            buttons.nth(0).click()
            section.scroll_into_view_if_needed()
            page.wait_for_timeout(800)
            section.screenshot(path=str(ROOT/'.preview'/f'services-showcase-{width}.png'),style='body > header,body .custom-cursor,body #topBtn,body #progress-bar{display:none;}')
            buttons.nth(5).click()
        if width==1440:
            cdp=ctx.new_cdp_session(page)
            expr='getEventListeners(document.querySelector(".service-selector button")).click.length'
            assert cdp.send('Runtime.evaluate', {'expression':expr,'includeCommandLineAPI':True,'returnByValue':True})['result']['value']==1
            page.evaluate('initServicesShowcase();initServicesShowcase()')
            assert cdp.send('Runtime.evaluate', {'expression':expr,'includeCommandLineAPI':True,'returnByValue':True})['result']['value']==1
        page.set_viewport_size({'width':1024 if width<=768 else 390,'height':844})
        page.wait_for_timeout(500)
        active_is(section, 5)
        assert section.locator('[role="tablist"]').get_attribute('aria-orientation')==('vertical' if width<=768 else 'horizontal')
        no_overflow(page)
        page.set_viewport_size({'width':width,'height':height})
        # Real local navigation for every preserved service enquiry link.
        for i in range(6):
            page.locator(f'#service-tab-{i}').click()
            with page.expect_navigation(wait_until='load'):
                if width<=768:
                    page.locator(f'#{SERVICES[i]["id"]} a').tap()
                else:
                    page.locator(f'#{SERVICES[i]["id"]} a').click()
            assert page.url==BASE+'contact.html'
            load(page)
        # Header open/close, backdrop, scroll restore and page navigation from this section.
        section.scroll_into_view_if_needed()
        page.wait_for_timeout(700)
        if width<=768:
            menu=page.locator('.menu-toggle')
            y=page.evaluate('scrollY')
            menu.tap()
            assert menu.get_attribute('aria-expanded')=='true'
            assert page.locator('body').evaluate('e=>e.classList.contains("menu-open")')
            page.locator('nav a[href="about.html"]').wait_for(state='visible')
            page.keyboard.press('Escape')
            assert menu.get_attribute('aria-expanded')=='false'
            assert abs(page.evaluate('scrollY')-y)<2
            menu.tap()
            page.locator('.nav-overlay').click(position={'x':10,'y':200})
            assert menu.get_attribute('aria-expanded')=='false'
            menu.tap()
        with page.expect_navigation(wait_until='load'):
            page.locator('nav a[href="about.html"]').click()
        assert page.url==BASE+'about.html'
        page.wait_for_timeout(900)
        page.locator('.about-story').scroll_into_view_if_needed()
        page.wait_for_timeout(800)
        assert page.locator('.about-story').evaluate('e=>e.classList.contains("show")')
        page.locator('[data-purpose-select="1"]').click()
        assert page.locator('#purpose-panel-1').evaluate('e=>e.classList.contains("is-active")')
        page.locator('#strength-tab-3').click()
        assert page.locator('#strength-panel-3').is_visible()
        assert page.locator('.company-stats dd').count()==0
        with page.expect_navigation(wait_until='load'):
            page.locator('header .logo').click()
        assert page.url==BASE+'index.html'
        page.wait_for_timeout(900)
        trigger=page.locator('.project-trigger').first
        trigger.click()
        page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"')
        before=page.locator('.viewer-counter').inner_text()
        page.keyboard.press('ArrowRight')
        page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"')
        assert page.locator('.viewer-counter').inner_text()!=before
        page.keyboard.press('Escape')
        assert page.locator('#project-lightbox').is_hidden()
        assert trigger.evaluate('e=>document.activeElement===e')
        assert not errors and not bad_responses and not console_errors, (errors,bad_responses,console_errors)
        ctx.close()
        print(f'PASS {width}px: six services, correct content/graphics, stable layout, bounds/overflow, touch/keys/focus, indicator, pointer, resize, Contact links, header and About/home viewer regression', flush=True)
    # Existing fragment links remain usable on first load and hash changes.
    if not fallback_only:
        ctx=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
        page=ctx.new_page()
        for i,service in enumerate(SERVICES):
            load(page,'services.html#'+service['id'])
            active_is(page.locator('.services-showcase'),i)
            assert page.locator('#'+service['id']).bounding_box()['y']>=page.locator('header').bounding_box()['height']
        page.evaluate('location.hash="brand-films"')
        page.wait_for_timeout(300)
        active_is(page.locator('.services-showcase'),0)
        page.evaluate('location.hash="not-a-service"')
        page.wait_for_timeout(100)
        active_is(page.locator('.services-showcase'),0)
        page.evaluate('location.hash="%invalid"')
        page.wait_for_timeout(100)
        active_is(page.locator('.services-showcase'),0)
        ctx.close()
        print('PASS all six service deep links and valid/unknown/malformed hash changes',flush=True)
    # Isolate fallback behavior from third-party font availability. Main size checks use real fonts.
    for mode in ['no-js','failed-js','reduced-mobile','reduced-desktop','failed-js-reduced']:
        opts={'viewport':{'width':1440 if mode=='reduced-desktop' else 390,'height':900}}
        if mode=='no-js':opts['java_script_enabled']=False
        if 'reduced' in mode:opts['reduced_motion']='reduce'
        ctx=browser.new_context(**opts)
        ctx.route('https://fonts.googleapis.com/**',lambda route:route.abort())
        if mode.startswith('failed-js'):ctx.route(BASE+'assets/js/main.js',lambda route:route.abort())
        page=ctx.new_page()
        load(page,fonts=False)
        section=page.locator('.services-showcase')
        if mode in ['no-js','failed-js','failed-js-reduced']:
            if mode.startswith('failed-js'):page.wait_for_timeout(4500)
            assert page.locator('.preloader').is_hidden()
            assert section.locator('.service-selector').is_hidden()
            for i in range(6):
                panel=section.locator('.service-presentation').nth(i)
                assert panel.is_visible() and panel.locator('h3').inner_text()==SERVICES[i]['title']
                assert panel.locator('p').inner_text()==SERVICES[i]['description']
                assert panel.locator('a').get_attribute('href')=='contact.html'
                assert panel.evaluate('s=>[...s.querySelectorAll("h3,p")].every(e=>e.scrollWidth<=e.clientWidth)'), (mode,i,'fallback text overflow')
            with page.expect_navigation(wait_until='load'):
                section.locator('.service-presentation a').last.click()
            assert page.url==BASE+'contact.html'
        else:
            section.locator('#service-tab-4').click()
            active_is(section,4)
            panel=section.locator('.is-active')
            assert panel.evaluate('e=>getComputedStyle(e).transitionDuration==="0s"')
            assert panel.locator('path').evaluate('e=>getComputedStyle(e).animationName==="none"')
            panel.hover()
            page.wait_for_timeout(100)
            assert section.locator('.service-stage').evaluate('e=>!e.style.getPropertyValue("--service-light-x")')
        no_overflow(page)
        ctx.close()
        print(f'PASS {mode}: readable fallback or motion suppression and working enquiry link',flush=True)
    browser.close()

now=(ROOT/'services.html').read_text(encoding='utf-8')
strip_section=lambda s:re.sub(r'<section class="services-page.*?</section>','',s,flags=re.S)
assert strip_section(now).replace('<noscript><style>.preloader{display:none;}</style></noscript>\n\n','')==strip_section(BASELINE['services.html'])
assert (ROOT/'assets/js/main.js').read_text(encoding='utf-8').startswith(BASELINE['main.js'])
for name,digest in BASELINE['pages'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
for name,digest in BASELINE['assets'].items():assert hashlib.sha256((ROOT/'assets/images'/name).read_bytes()).hexdigest()==digest,name
print('PASS scope: other Services sections, previous JS, all other pages and local assets preserved',flush=True)
server.shutdown()
