"""Services Step 2 checks in installed Chrome, served under /Yolo_house/."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
import hashlib, html, json, re, sys
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
B=json.loads((ROOT/'.preview/workflow-baseline.json').read_text(encoding='utf-8'))

def historical_paths(source):
    """Normalize only asset relocations; retain the original historical snapshot."""
    return source.replace('assets/css/style.css', 'style.css').replace('assets/js/main.js', 'main.js').replace('assets/images/', 'images/')
old=re.search(r'<section class="work-process.*?</section>',B['services.html'],re.S)[0]
STAGES=[(html.unescape(title),html.unescape(desc)) for title,desc in re.findall(r'<h3>(.*?)</h3><p>(.*?)</p>',old,re.S)]
assert len(STAGES)>1

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/favicon.ico':
            self.send_response(204);self.end_headers();return
        if not self.path.startswith('/Yolo_house/'):
            self.send_error(404);return
        self.path='/'+self.path[len('/Yolo_house/'):]
        try:super().do_GET()
        except (ConnectionResetError,BrokenPipeError):pass
    def log_message(self,*args):pass

server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
BASE=f'http://127.0.0.1:{server.server_port}/Yolo_house/'
SIZES=[(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]
if '--fallback-only' in sys.argv:SIZES=[]
if '--width' in sys.argv:SIZES=[size for size in SIZES if size[0]==int(sys.argv[sys.argv.index('--width')+1])]

def load(page,name='services.html',fonts=True):
    page.set_default_navigation_timeout(60000)
    page.goto(BASE+name)
    page.evaluate('document.fonts.ready')
    if fonts:
        assert page.evaluate("""()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(t=>t.family.replaceAll('"','')===f&&t.status==='loaded'))"""),'Existing fonts failed to load'
    page.wait_for_timeout(900)

def state(section,index):
    buttons=section.locator('.workflow-controls button')
    panels=section.locator('.workflow-panel')
    assert buttons.nth(index).get_attribute('aria-selected')=='true'
    assert buttons.nth(index).get_attribute('aria-controls')==panels.nth(index).get_attribute('id')
    assert panels.nth(index).get_attribute('aria-labelledby')==buttons.nth(index).get_attribute('id')
    assert panels.nth(index).is_visible() and panels.nth(index).get_attribute('aria-hidden')=='false'
    assert panels.nth(index).locator('h3').inner_text()==STAGES[index][0]
    assert panels.nth(index).locator('p').inner_text()==STAGES[index][1]
    assert panels.nth(index).locator('.workflow-stage-number').inner_text().split()==[f'{index+1:02}','/',f'{len(STAGES):02}']
    assert panels.evaluate_all('es=>es.filter(e=>!e.inert).length')==1
    assert buttons.evaluate_all('es=>es.filter(e=>e.getAttribute("aria-selected")==="true").length')==1
    assert panels.evaluate_all('es=>es.every(e=>e.getAttribute("aria-hidden")===String(e.inert))')
    assert buttons.evaluate_all('es=>es.filter(e=>e.tabIndex===0).length')==1
    assert section.locator('.is-active').count()==1
    assert abs(float(section.evaluate('e=>e.style.getPropertyValue("--workflow-progress")'))-index/(len(STAGES)-1))<.001

def overflow(page):
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),'Horizontal page overflow'

def panel_bounds(panel):
    assert panel.evaluate('s=>[...s.querySelectorAll("h3,p,svg,.workflow-stage-number")].every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom})')
    assert panel.evaluate('s=>[...s.querySelectorAll("h3,p")].every(e=>e.scrollWidth<=e.clientWidth)'), 'Text glyph overflow'
    assert panel.evaluate('s=>{let c=s.querySelector(".workflow-copy").getBoundingClientRect(),g=s.querySelector(".workflow-graphic").getBoundingClientRect();return c.right<=g.left||c.bottom<=g.top;}'),'Copy/graphic overlap'

def connector(section,index,vertical):
    track=section.locator('.workflow-connector').bounding_box()
    fill=section.locator('.workflow-connector i').bounding_box()
    markers=section.locator('.workflow-marker')
    first,last=markers.first.bounding_box(),markers.last.bounding_box()
    current=markers.nth(index).bounding_box()
    if vertical:
        assert abs(track['y']-(first['y']+first['height']/2))<1
        assert abs(track['y']+track['height']-(last['y']+last['height']/2))<1
        assert abs(track['x']+track['width']/2-(current['x']+current['width']/2))<1
        assert abs(fill['height']-track['height']*index/(len(STAGES)-1))<1, (track,fill,index,section.locator('.workflow-connector i').evaluate('e=>({transform:getComputedStyle(e).transform,height:getComputedStyle(e).height,progress:getComputedStyle(e).getPropertyValue("--workflow-progress")})'))
        assert abs(fill['y']+fill['height']-(current['y']+current['height']/2))<1
    else:
        assert abs(track['x']-(first['x']+first['width']/2))<1
        assert abs(track['x']+track['width']-(last['x']+last['width']/2))<1
        assert abs(track['y']+track['height']/2-(current['y']+current['height']/2))<1
        assert abs(fill['width']-track['width']*index/(len(STAGES)-1))<1, (track,fill,index,section.locator('.workflow-connector i').evaluate('e=>({transform:getComputedStyle(e).transform,width:getComputedStyle(e).width,progress:getComputedStyle(e).getPropertyValue("--workflow-progress")})'))
        assert abs(fill['x']+fill['width']-(current['x']+current['width']/2))<1

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    for width,height in SIZES:
        ctx=browser.new_context(viewport={'width':width,'height':height},is_mobile=width<=768,has_touch=width<=768)
        page=ctx.new_page();errors=[];console=[];bad=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:console.append(m.text) if m.type=='error' else None)
        page.on('response',lambda r:bad.append(r.url) if r.url.startswith(BASE) and r.status>=400 else None)
        load(page)
        section=page.locator('.work-process');buttons=section.locator('[role="tab"]');panels=section.locator('[role="tabpanel"]')
        state(section,0)
        assert buttons.count()==panels.count()==len(STAGES)
        assert section.locator('[role="tablist"]').get_attribute('aria-orientation')==('vertical' if width<=900 else 'horizontal')
        page.locator('#service-tab-4').click()
        section.scroll_into_view_if_needed();page.wait_for_timeout(600)
        initial_height=section.evaluate('e=>e.offsetHeight');following=page.locator('.equipment').evaluate('e=>e.offsetTop')
        paths=[]
        for i in range(len(STAGES)):
            if width<=768:buttons.nth(i).tap()
            else:buttons.nth(i).click()
            page.wait_for_timeout(500)
            state(section,i);panel_bounds(panels.nth(i));connector(section,i,width<=900);overflow(page)
            assert buttons.nth(i).evaluate('e=>e.scrollWidth<=e.clientWidth'),'Control glyph overflow'
            assert buttons.nth(i).bounding_box()['height']>=44
            assert section.evaluate('e=>e.offsetHeight')==initial_height
            assert page.locator('.equipment').evaluate('e=>e.offsetTop')==following
            assert page.locator('#service-tab-4').get_attribute('aria-selected')=='true'
            assert panels.nth(i).locator('path').evaluate('e=>e.getAnimations().every(a=>a.playState==="finished")')
            assert panels.nth(i).locator('.workflow-graphic').get_attribute('aria-hidden')=='true'
            assert buttons.nth(i).locator('.workflow-marker').evaluate('e=>getComputedStyle(e).backgroundColor==="rgb(212, 175, 55)"')
            paths.append(panels.nth(i).locator('path').get_attribute('d'))
        assert len(set(paths))==len(STAGES)
        page.wait_for_timeout(700);state(section,len(STAGES)-1)
        page.keyboard.press('Tab');buttons.last.focus()
        assert buttons.last.evaluate('e=>e.matches(":focus-visible")&&getComputedStyle(e).outlineStyle==="solid"')
        page.keyboard.press('Home');state(section,0);assert page.evaluate('scrollY')>0
        page.keyboard.press('End');state(section,len(STAGES)-1)
        page.keyboard.press('ArrowDown' if width<=900 else 'ArrowRight');state(section,0)
        page.keyboard.press('ArrowUp' if width<=900 else 'ArrowLeft');state(section,len(STAGES)-1)
        page.keyboard.press('Tab');assert panels.last.evaluate('e=>document.activeElement===e')
        assert panels.last.evaluate('e=>getComputedStyle(e).outlineStyle==="solid"')
        page.keyboard.press('Tab');assert page.locator('.equipment a').evaluate('e=>document.activeElement===e'),'Inactive panel entered keyboard order'
        # Six showcase selections must not change the workflow state.
        for i in range(6):
            page.locator(f'#service-tab-{i}').click();page.wait_for_timeout(320)
            assert page.locator(f'#service-tab-{i}').get_attribute('aria-selected')=='true'
            assert page.locator('.services-showcase .service-presentation.is-active').get_attribute('aria-hidden')=='false'
            state(section,len(STAGES)-1)
        if width in [1440,375]:
            buttons.nth(2).click();section.scroll_into_view_if_needed();page.wait_for_timeout(800)
            section.screenshot(path=str(ROOT/'.preview'/f'workflow-{width}.png'),style='body > header,body .custom-cursor,body #topBtn,body #progress-bar{display:none;}')
            panels.nth(2).scroll_into_view_if_needed();page.wait_for_timeout(800)
            page.screenshot(path=str(ROOT/'.preview'/f'workflow-viewport-{width}.png'))
        buttons.nth(3).click();page.wait_for_timeout(350)
        if width==1440:
            cdp=ctx.new_cdp_session(page)
            expr='[...document.querySelectorAll(".workflow-controls button")].map(e=>getEventListeners(e).click.length)'
            assert cdp.send('Runtime.evaluate',{'expression':expr,'includeCommandLineAPI':True,'returnByValue':True})['result']['value']==[1]*len(STAGES)
            page.evaluate('initProductionWorkflow();initProductionWorkflow()')
            state(section,3)
            assert cdp.send('Runtime.evaluate',{'expression':expr,'includeCommandLineAPI':True,'returnByValue':True})['result']['value']==[1]*len(STAGES)
            page.emulate_media(reduced_motion='reduce')
            assert panels.nth(3).locator('path').evaluate('e=>getComputedStyle(e).animationName==="none"')
            assert section.locator('.workflow-connector i').evaluate('e=>getComputedStyle(e).transitionDuration==="0s"')
            page.emulate_media(reduced_motion='no-preference')
        page.set_viewport_size({'width':1440 if width<=900 else 390,'height':844})
        page.wait_for_function('()=>{const e=document.querySelector(".workflow-connector i");e.getBoundingClientRect();return e.getAnimations().every(a=>a.playState==="finished");}')
        state(section,3);connector(section,3,width>900);overflow(page)
        assert section.locator('[role="tablist"]').get_attribute('aria-orientation')==('horizontal' if width<=900 else 'vertical')
        page.set_viewport_size({'width':width,'height':height})
        # Preserve actual toolkit and final CTA navigation.
        for selector in ['.equipment .text-link','.services-cta .primary-btn']:
            with page.expect_navigation(wait_until='load'):page.locator(selector).click()
            assert page.url==BASE+'contact.html'
            load(page)
        section.scroll_into_view_if_needed();page.wait_for_timeout(500)
        if width<=768:
            y=page.evaluate('scrollY');page.locator('.menu-toggle').tap()
            assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='true'
            page.locator('nav a[href="about.html"]').wait_for(state='visible')
            page.keyboard.press('Escape')
            assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
            assert abs(page.evaluate('scrollY')-y)<2
            page.locator('.menu-toggle').tap()
            page.locator('.menu-toggle').tap()
            assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
            page.locator('.menu-toggle').tap()
        with page.expect_navigation(wait_until='load'):page.locator('nav a[href="about.html"]').click()
        assert page.url==BASE+'about.html';page.wait_for_timeout(900)
        page.locator('.about-story').scroll_into_view_if_needed();page.wait_for_timeout(800)
        assert page.locator('.about-story').evaluate('e=>e.classList.contains("show")')
        page.locator('[data-purpose-select="1"]').click()
        assert page.locator('#purpose-panel-1').evaluate('e=>e.classList.contains("is-active")')
        page.locator('#strength-tab-3').click();assert page.locator('#strength-panel-3').is_visible()
        with page.expect_navigation(wait_until='load'):page.locator('header .logo').click()
        assert page.url==BASE+'index.html';page.wait_for_timeout(900)
        trigger=page.locator('.project-trigger').first;trigger.click()
        page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"')
        counter=page.locator('.viewer-counter').inner_text();page.keyboard.press('ArrowRight')
        page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"')
        assert page.locator('.viewer-counter').inner_text()!=counter
        page.keyboard.press('Escape');assert page.locator('#project-lightbox').is_hidden()
        assert trigger.evaluate('e=>document.activeElement===e')
        assert not errors and not console and not bad,(errors,console,bad)
        ctx.close();print(f'PASS {width}px: five stages/graphics, exact copy, connector geometry, stable layout/overflow, touch/keys/focus, resize, independent showcase, CTA links, header/About/home viewer regression',flush=True)
    for mode in ['no-js','failed-js','workflow-not-initialized','reduced-mobile','reduced-desktop']:
        opts={'viewport':{'width':1440 if mode=='reduced-desktop' else 375,'height':900}}
        if mode=='no-js':opts['java_script_enabled']=False
        if mode.startswith('reduced'):opts['reduced_motion']='reduce'
        ctx=browser.new_context(**opts)
        ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort())
        if mode=='failed-js':ctx.route(BASE+'assets/js/main.js',lambda r:r.abort())
        if mode=='workflow-not-initialized':ctx.route(BASE+'assets/js/main.js',lambda r:r.fulfill(status=200,content_type='application/javascript',body=B['main.js']))
        page=ctx.new_page();load(page,fonts=False);section=page.locator('.work-process')
        if mode in ['no-js','failed-js','workflow-not-initialized']:
            if mode=='failed-js':page.wait_for_timeout(4500)
            assert page.locator('.preloader').is_hidden()
            assert section.locator('.workflow-controls').is_hidden() and section.locator('.workflow-hint').is_hidden()
            for i,(title,desc) in enumerate(STAGES):
                panel=section.locator('.workflow-panel').nth(i)
                assert panel.is_visible() and panel.locator('h3').inner_text()==title and panel.locator('p').inner_text()==desc
                panel_bounds(panel)
        else:
            for i in range(len(STAGES)):
                section.locator('.workflow-controls button').nth(i).click();state(section,i)
                panel=section.locator('.is-active');panel_bounds(panel)
                assert panel.evaluate('e=>getComputedStyle(e).transitionDuration==="0s"')
                assert panel.locator('path').evaluate('e=>getComputedStyle(e).animationName==="none"')
                assert section.locator('.workflow-connector i').evaluate('e=>getComputedStyle(e).transitionDuration==="0s"')
                assert section.locator('.workflow-controls button').nth(i).locator('.workflow-marker').evaluate('e=>getComputedStyle(e).transform==="none"')
        overflow(page);ctx.close();print(f'PASS {mode}: readable font/script fallback or immediate motion-free selection',flush=True)
    browser.close()

now=(ROOT/'services.html').read_text(encoding='utf-8')
strip=lambda s:re.sub(r'<section class="work-process.*?</section>','',s,flags=re.S)
assert strip(historical_paths(now))==strip(B['services.html'])
assert (ROOT/'assets/js/main.js').read_text(encoding='utf-8').startswith(B['main.js'])
for name,digest in B['pages'].items():assert hashlib.sha256(historical_paths((ROOT/name).read_bytes().decode('utf-8')).encode('utf-8')).hexdigest()==digest,name
for name,digest in B['assets'].items():assert hashlib.sha256((ROOT/'assets/images'/name).read_bytes()).hexdigest()==digest,name
print('PASS scope: Services Showcase, all excluded sections/pages/assets and previous JavaScript preserved',flush=True)
server.shutdown()
