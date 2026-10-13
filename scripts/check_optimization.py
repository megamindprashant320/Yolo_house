from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
import json,re,hashlib,sys
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent.parent
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if not self.path.startswith('/Yolo_house/'):self.send_error(404);return
  self.path='/'+self.path[len('/Yolo_house/'):];super().do_GET()
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/Yolo_house/'
b=json.loads((root/'.preview/optimization-baseline.json').read_text(encoding='utf-8'))

def relocated_source(name, source):
 if name == 'index.html':return source.replace('href="style.css"', 'href="assets/css/style.css"').replace('src="main.js"', 'src="assets/js/main.js"').replace('images/', 'assets/images/')
 if name == 'style.css':return source.replace('images/', '../images/')
 return source
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]:
  ctx=browser.new_context(viewport={'width':w,'height':h},is_mobile=w<=768,has_touch=w<=768)
  page=ctx.new_page();errors=[];bad=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append(r.url) if r.url.startswith(base) and r.status>=400 else None)
  page.goto(base+'index.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(900)
  assert page.locator('h1').count()==1 and page.locator('main').count()==1
  assert page.locator('link[rel="canonical"]').get_attribute('href')=='https://megamindprashant320.github.io/Yolo_house/'
  assert page.locator('meta[name="description"]').get_attribute('content')
  assert page.locator('main img').evaluate_all('es=>es.every(e=>e.width>0&&e.hasAttribute("width")&&e.hasAttribute("height")&&e.loading==="lazy"&&e.decoding==="async"&&!!e.alt)')
  page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('e=>document.activeElement===e')
  page.keyboard.press('Enter');assert page.locator('main').evaluate('e=>document.activeElement===e')
  page.wait_for_timeout(300)
  header_bottom=page.locator('header').bounding_box()['height'];assert page.locator('.hero h1').bounding_box()['y']>=header_bottom
  # Compare approved layout with the exact pre-change sources, using warm identical fonts.
  old=ctx.new_page()
  for name,path,typ in [('index.html','index.html','text/html'),('style.css','assets/css/style.css','text/css'),('main.js','assets/js/main.js','text/javascript')]:
   old.route(base+path,lambda route,request,n=name,t=typ:route.fulfill(status=200,content_type=t,body=relocated_source(n,b[n])))
  old.goto(base+'index.html');old.evaluate('document.fonts.ready');old.wait_for_timeout(900)
  for selector in ['.hero','.hero h1','.hero-stats','.about','.services','.portfolio','.home-project-cta','.home-footer']:
   a=page.locator(selector).evaluate('e=>({w:e.offsetWidth,h:e.offsetHeight})');z=old.locator(selector).evaluate('e=>({w:e.offsetWidth,h:e.offsetHeight})');assert a==z,(w,selector,a,z)
  old.close()
  for selector in ['.about','.home-approach','.services','.portfolio','.home-project-cta','.home-footer']:
   section=page.locator(selector);section.scroll_into_view_if_needed();page.wait_for_timeout(700)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   assert section.evaluate('s=>[...s.querySelectorAll("h1,h2,h3,p,a,summary")].filter(e=>!e.closest("details:not([open])")||e.closest("summary")).every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left-1&&r.right<=b.right+1&&r.top>=b.top-1&&r.bottom<=b.bottom+1})'),(w,selector)
  page.locator('.approach-step summary').nth(1).click();assert page.locator('.approach-step').nth(1).get_attribute('open') is not None
  page.wait_for_function('document.querySelector(".approach-status").textContent.startsWith("02 /")')
  assert page.locator('[data-service-showcase] p').evaluate_all('es=>es.every(e=>getComputedStyle(e).opacity==="1")')
  t=page.locator('.project-trigger').first;t.scroll_into_view_if_needed();page.wait_for_timeout(750);t.focus();page.keyboard.press('Enter')
  page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"')
  assert page.locator('[data-viewer-close]').evaluate('e=>document.activeElement===e')
  page.keyboard.press('Shift+Tab');assert page.locator('[data-viewer-next]').evaluate('e=>document.activeElement===e')
  page.keyboard.press('Tab');assert page.locator('[data-viewer-close]').evaluate('e=>document.activeElement===e')
  assert page.locator('#project-lightbox').evaluate('e=>e.matches(":modal")')
  page.keyboard.press('ArrowRight');page.wait_for_function('document.querySelector(".viewer-counter").textContent==="02 / 06"&&document.querySelector("#project-lightbox").dataset.state==="ready"')
  assert page.locator('.viewer-image').get_attribute('alt')=='Cinema camera beside a mountain lake'
  assert page.locator('.viewer-background-layer.is-visible').evaluate('e=>getComputedStyle(e).filter.includes("blur(")')
  if w<=768:
   cdp=ctx.new_cdp_session(page);box=page.locator('.viewer-stage').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
   cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x+60,'y':y}]})
   for f in [.25,.5,.75,1]:cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+60-120*f,'y':y}]})
   cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   page.wait_for_function('document.querySelector(".viewer-counter").textContent==="03 / 06"&&document.querySelector("#project-lightbox").dataset.state==="ready"')
  page.keyboard.press('Escape');assert t.evaluate('e=>document.activeElement===e')
  if w<=768:
   button=page.locator('.menu-toggle');button.tap();assert button.get_attribute('aria-expanded')=='true'
   assert page.locator('main').evaluate('e=>e.inert') and page.locator('.home-footer').evaluate('e=>e.inert')
   assert page.locator('#primary-navigation').evaluate('e=>getComputedStyle(e).filter==="none"')
   page.locator('#primary-navigation a').last.focus();page.keyboard.press('Tab');assert button.evaluate('e=>document.activeElement===e')
   page.keyboard.press('Escape');assert button.get_attribute('aria-expanded')=='false';assert not page.locator('main').evaluate('e=>e.inert')
  for selector in ['header .logo','.hero .primary-btn','.hero .secondary-btn','.project-cta-primary','.project-cta-secondary','.footer-logo','.footer-navigation a']:
   links=page.locator(selector);targets=links.evaluate_all('es=>es.map(e=>e.getAttribute("href"))')
   for i,url in enumerate(targets):
    page.locator(selector).nth(i).click();page.wait_for_url('**/'+url);page.goto(base+'index.html');page.wait_for_timeout(100)
  page.locator('.home-footer').scroll_into_view_if_needed();page.wait_for_timeout(700);page.locator('#topBtn').click();page.wait_for_function('scrollY<2')
  assert not errors and not bad,(errors,bad)
  print(f'PASS {w}px: preserved geometry, text bounds, lazy images, skip link, links, viewer focus/arrows/swipe, trust, drawer, back-to-top, no errors',flush=True)
  ctx.close()
 for opts in [{'java_script_enabled':False},{'reduced_motion':'reduce'}]:
  ctx=browser.new_context(viewport={'width':390,'height':844},**opts);ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());page=ctx.new_page();page.goto(base+'index.html');page.wait_for_timeout(900)
  for selector in ['.about','.services','.portfolio']:
   assert page.locator(selector).evaluate('e=>getComputedStyle(e).opacity==="1"')
  if 'reduced_motion' in opts:assert page.locator('main img').evaluate_all('es=>es.every(e=>getComputedStyle(e).opacity==="1")')
  ctx.close()
 # Shared font and JS regression on untouched pages.
 for name in ['about.html','services.html','portfolio.html','contact.html']:
  for w in [1440,390]:
   ctx=browser.new_context(viewport={'width':w,'height':844},has_touch=w==390,is_mobile=w==390);page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(base+name);page.evaluate('document.fonts.ready');page.wait_for_timeout(600)
   assert page.locator('header .logo').is_visible()
   if w==390:page.locator('.menu-toggle').tap();assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='true';page.keyboard.press('Escape')
   if name=='contact.html':assert not page.locator('#project-form fieldset').is_disabled()
   if name=='services.html':
    assert page.locator('#process-title').is_visible() or page.locator('#process-title').count()==1
   assert not errors,errors;ctx.close()
 browser.close()
for n,d in b['pages'].items():
 import hashlib
 assert hashlib.sha256((root/n).read_bytes()).hexdigest()==d,n
for n,d in b['assets'].items():assert hashlib.sha256((root/'assets/images'/n).read_bytes()).hexdigest()==d
print('PASS fallback/reduced motion, other-page smoke checks and asset preservation',flush=True)
server.shutdown()


