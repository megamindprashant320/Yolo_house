"""Browser regression checks under /Yolo_house/. No enquiry or external write actions."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
import hashlib
import json
import re
import sys
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
baseline=json.loads((ROOT/'.preview'/'lightbox-baseline.json').read_text(encoding='utf-8'))

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith('/Yolo_house/'):
            self.send_error(404);return
        self.path='/'+self.path[len('/Yolo_house/'):]
        super().do_GET()
    def log_message(self,*args):pass

server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/Yolo_house/'

def context_for(browser,width,height=900,**options):
    context=browser.new_context(viewport={'width':width,'height':height},is_mobile=width<=768,has_touch=width<=768,**options)
    if '--require-fonts' not in sys.argv:
        context.route('https://fonts.googleapis.com/**',lambda route:route.abort())
    return context

def ready(page,index):
    expected=f'{index:02} / 06'
    page.wait_for_function('''expected=>{
        const d=document.querySelector('#project-lightbox');
        return d.open && d.dataset.state==='ready' && d.querySelector('.viewer-counter').textContent===expected;
    }''',arg=expected)
    assert page.locator('.viewer-image').get_attribute('src').endswith(f'/images/work{index}.jpg')
    assert f'work{index}.jpg' in page.locator('.viewer-background-layer.is-visible').evaluate('e=>e.style.backgroundImage')

def close_check(page,trigger,y):
    page.wait_for_function("!document.querySelector('#project-lightbox').open && !document.body.classList.contains('project-viewer-open')")
    assert abs(page.evaluate('window.scrollY')-y)<=1,(page.evaluate('window.scrollY'),y)
    assert trigger.evaluate('e=>document.activeElement===e')

def gallery_geometry(page):
    page.locator('#portfolio').scroll_into_view_if_needed();page.wait_for_timeout(900)
    page.wait_for_function("[...document.querySelectorAll('#portfolio img')].every(e=>e.complete && e.naturalWidth>0)")
    page.wait_for_function("document.querySelector('#portfolio').getAnimations({subtree:true}).every(animation=>animation.playState!=='running')")
    return page.evaluate('''()=>{
        const g=document.querySelector('#portfolio .gallery'),r=g.getBoundingClientRect(),s=getComputedStyle(g);
        return {columns:s.gridTemplateColumns,gap:s.gap,margin:s.marginTop,items:[...g.children].map(e=>{
            const b=e.getBoundingClientRect(),i=e.querySelector('img'),t=i.getBoundingClientRect();
            return {x:Math.round((b.x-r.x)*100)/100,y:Math.round((b.y-r.y)*100)/100,width:b.width,height:b.height,imageWidth:t.width,imageHeight:t.height,fit:getComputedStyle(i).objectFit,radius:getComputedStyle(e).borderRadius};
        })};
    }''')

try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
        for width,height in [(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]:
            context=context_for(browser,width,height)
            old=context.new_page()
            old.route(base+'index.html',lambda route:route.fulfill(status=200,content_type='text/html',body=baseline['index_before']))
            old.route(base+'style.css',lambda route:route.fulfill(status=200,content_type='text/css',body=baseline['css_before']))
            old.goto(base+'index.html');old.evaluate('document.fonts.ready')
            geometry_before=gallery_geometry(old)
            old.locator('#portfolio .item').first.hover();old.wait_for_timeout(700)
            old.wait_for_function("document.querySelector('#portfolio').getAnimations({subtree:true}).every(animation=>animation.playState!=='running')")
            hover_before=old.locator('#portfolio .item img').first.evaluate('e=>getComputedStyle(e).transform')
            old.close()
            page=context.new_page();errors=[];failed=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('response',lambda r:failed.append((r.url,r.status)) if r.url.startswith(base) and r.status>=400 else None)
            page.goto(base+'index.html');page.evaluate('document.fonts.ready')
            if '--require-fonts' in sys.argv:
                assert page.evaluate('''()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(font=>font.family.replaceAll('"','')===f && font.status==='loaded'))''')
            assert gallery_geometry(page)==geometry_before,(width,gallery_geometry(page),geometry_before)
            page.locator('#portfolio .item').first.hover();page.wait_for_timeout(700)
            page.wait_for_function("document.querySelector('#portfolio').getAnimations({subtree:true}).every(animation=>animation.playState!=='running')")
            hover_after=page.locator('#portfolio .item img').first.evaluate('e=>getComputedStyle(e).transform')
            assert hover_after==hover_before,(width,hover_before,hover_after)
            triggers=page.locator('#portfolio .project-trigger')
            for index in range(1,7):
                trigger=triggers.nth(index-1)
                trigger.scroll_into_view_if_needed();page.wait_for_timeout(100)
                before=page.evaluate('window.scrollY')
                if width<=768:trigger.tap()
                else:trigger.click()
                ready(page,index)
                assert page.locator('.viewer-title').is_hidden()
                assert page.locator('[data-viewer-close]').evaluate('e=>document.activeElement===e')
                assert page.evaluate("document.body.classList.contains('project-viewer-open') && getComputedStyle(document.body).position==='fixed'")
                bounds=page.locator('.viewer-image').evaluate('''e=>{
                    const r=e.getBoundingClientRect();
                    return {inside:r.left>=0&&r.top>=0&&r.right<=innerWidth&&r.bottom<=innerHeight,ratio:r.width/r.height,natural:e.naturalWidth/e.naturalHeight,notUpscaled:r.width<=e.naturalWidth&&r.height<=e.naturalHeight,fit:getComputedStyle(e).objectFit,inlineOpacity:e.style.opacity,inlineTransform:e.style.transform};
                }''')
                assert bounds['inside'] and bounds['notUpscaled'] and bounds['fit']=='contain' and abs(bounds['ratio']-bounds['natural'])<.01,bounds
                assert not bounds['inlineOpacity'] and not bounds['inlineTransform'],bounds
                assert page.locator('.viewer-background-layer.is-visible').evaluate("e=>getComputedStyle(e).filter.includes('blur(') && getComputedStyle(e).filter.includes('brightness(')")
                assert page.locator('.viewer-control:visible').evaluate_all('es=>es.every(e=>{const r=e.getBoundingClientRect();return r.width>=48&&r.height>=48&&r.x>=0&&r.y>=0&&r.right<=innerWidth&&r.bottom<=innerHeight})')
                page.locator('.viewer-image').click();assert page.locator('#project-lightbox').evaluate('e=>e.open')
                if index==1:
                    page.keyboard.press('Shift+Tab')
                    assert page.locator('[data-viewer-next]').evaluate('e=>document.activeElement===e')
                    page.keyboard.press('Tab')
                    assert page.locator('[data-viewer-close]').evaluate('e=>document.activeElement===e')
                    page.mouse.wheel(0,500);page.wait_for_timeout(100)
                    assert page.evaluate('window.scrollY')==0
                    page.locator('[data-viewer-previous]').click();ready(page,6)
                    page.locator('[data-viewer-next]').click();ready(page,1)
                    page.keyboard.press('ArrowRight');ready(page,2)
                    page.keyboard.press('ArrowLeft');ready(page,1)
                    for _ in range(4):page.keyboard.press('ArrowRight')
                    ready(page,5)
                    page.wait_for_timeout(750);ready(page,5) # no autoplay
                if index%3==1:
                    page.keyboard.press('Escape')
                elif index%3==2:
                    page.locator('[data-viewer-close]').click()
                else:
                    page.mouse.click(5,height/2)
                close_check(page,trigger,before)
            if width<=768:
                trigger=triggers.first;trigger.scroll_into_view_if_needed();before=page.evaluate('window.scrollY');trigger.tap();ready(page,1)
                cdp=context.new_cdp_session(page)
                rectangle=page.locator('.viewer-image').bounding_box()
                center_x=rectangle['x']+rectangle['width']/2;center_y=rectangle['y']+rectangle['height']/2
                def swipe(dx,dy=0):
                    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':center_x-dx/2,'y':center_y-dy/2}]})
                    for fraction in [.25,.5,.75,1]:
                        cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':center_x-dx/2+dx*fraction,'y':center_y-dy/2+dy*fraction}]})
                    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
                swipe(-120);ready(page,2)
                swipe(120);ready(page,1)
                swipe(0,100);page.wait_for_timeout(300);ready(page,1)
                page.keyboard.press('Escape');close_check(page,trigger,before)
                # The existing drawer still works after the viewer closes.
                page.locator('.menu-toggle').tap()
                assert page.locator('nav').evaluate("e=>e.classList.contains('active')")
                page.keyboard.press('Escape')
                assert not page.evaluate("document.body.classList.contains('menu-open')")
            if width in [1440,375]:
                triggers.first.click();ready(page,1);page.wait_for_timeout(500)
                page.screenshot(path=str(ROOT/'.preview'/f'lightbox-{width}.png'))
                page.keyboard.press('Escape')
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
            assert not errors and not failed,(errors,failed)
            print(f'PASS {width}px: all six previews/backgrounds; image fit, buttons/arrows/wrap, focus/scroll restoration, Escape/backdrop, original grid/hover; '+('touch swipes' if width<=768 else 'mouse/keyboard'),flush=True)
            context.close()

        # Deliberately fail one existing source, then retry it and continue browsing.
        context=context_for(browser,390,844)
        failing={'enabled':True}
        context.route('**/images/work3.jpg',lambda route:route.fulfill(status=404,headers={'Cache-Control':'no-store'},body='') if failing['enabled'] else route.continue_())
        page=context.new_page();errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(base+'index.html');page.wait_for_timeout(850)
        page.locator('.project-trigger').nth(2).click()
        page.wait_for_function("document.querySelector('#project-lightbox').dataset.state==='error'")
        assert page.locator('.viewer-error').is_visible() and page.locator('.viewer-image').is_hidden()
        failing['enabled']=False
        page.locator('[data-viewer-retry]').click();ready(page,3)
        assert page.locator('[data-viewer-close]').evaluate('e=>document.activeElement===e')
        page.locator('[data-viewer-next]').click();ready(page,4)
        page.keyboard.press('Escape')
        # Opening and immediately closing must not leave a delayed image or scroll lock.
        page.locator('.project-trigger').first.click();page.keyboard.press('Escape');page.wait_for_timeout(350)
        assert not page.evaluate("document.querySelector('#project-lightbox').open || document.body.classList.contains('project-viewer-open')")
        assert not errors,errors
        context.close()

        context=context_for(browser,390,844,reduced_motion='reduce')
        page=context.new_page();page.goto(base+'index.html');page.wait_for_timeout(850)
        trigger=page.locator('.project-trigger').first;trigger.focus();page.keyboard.press('Enter');ready(page,1)
        assert page.locator('#project-lightbox').evaluate("e=>getComputedStyle(e).animationName==='none'")
        assert page.locator('.viewer-image').evaluate("e=>getComputedStyle(e).transitionDuration==='0s' && getComputedStyle(e).transform==='none'")
        page.locator('[data-viewer-next]').click();ready(page,2)
        assert page.locator('.viewer-background-layer.is-visible').evaluate("e=>getComputedStyle(e).transitionDuration==='0s'")
        page.set_viewport_size({'width':768,'height':540})
        page.wait_for_timeout(150)
        assert page.locator('.viewer-image').evaluate('''e=>{const r=e.getBoundingClientRect();return r.x>=0&&r.y>=0&&r.right<=innerWidth&&r.bottom<=innerHeight;}''')
        page.keyboard.press('Escape');assert trigger.evaluate('e=>document.activeElement===e')
        trigger.focus();page.keyboard.press('Space');ready(page,1)
        page.keyboard.press('Escape');context.close()
        browser.close()

    current=(ROOT/'index.html').read_text(encoding='utf-8')
    for cls in ['hero','about','services','cta']:
        pattern=r'<section class="'+cls+r'(?: [^"]*)?"[^>]*>.*?</section>'
        assert re.search(pattern,current,re.S)[0]==re.search(pattern,baseline['index_before'],re.S)[0],cls
    for tag in ['header','footer']:
        pattern='<'+tag+r'>.*?</'+tag+'>'
        assert re.search(pattern,current,re.S)[0]==re.search(pattern,baseline['index_before'],re.S)[0],tag
    for filename in ['about.html','services.html','portfolio.html','contact.html']:
        assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==baseline[filename]
    assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'images').iterdir() if p.is_file()}==baseline['images']
    print('PASS: missing-image retry/recovery, cancellation, reduced motion, Enter/Space; other pages/sections and all assets unchanged',flush=True)
finally:
    server.shutdown();server.server_close()
