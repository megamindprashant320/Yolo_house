from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
import json,re,hashlib,sys
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if not self.path.startswith('/Yolo_house/'):self.send_error(404);return
  self.path='/'+self.path[len('/Yolo_house/'):];super().do_GET()
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/Yolo_house/'
b=json.loads((root/'.preview/strength-baseline.json').read_text(encoding='utf-8'));old=re.search(r'<section class="why-us.*?</section>',b['about.html'],re.S)[0];features=re.findall(r'<h3>(.*?)</h3><p>(.*?)</p>',old,re.S)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]:
  ctx=browser.new_context(viewport={'width':w,'height':h},is_mobile=w<=768,has_touch=w<=768);page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(base+'about.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(900)
  assert page.evaluate("()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(t=>t.family.replaceAll('\"','')===f&&t.status==='loaded'))")
  s=page.locator('.why-us');s.scroll_into_view_if_needed();page.wait_for_timeout(500);buttons=s.locator('[role="tab"]');panels=s.locator('[role="tabpanel"]');height=s.evaluate('e=>e.offsetHeight');following=page.locator('.company-stats').evaluate('e=>e.offsetTop');paths=[]
  for i,(title,desc) in enumerate(features):
   if w<=768:buttons.nth(i).tap()
   else:buttons.nth(i).click()
   page.wait_for_timeout(500)
   assert buttons.nth(i).get_attribute('aria-selected')=='true'
   assert panels.nth(i).locator('h3').inner_text()==title and panels.nth(i).locator('p').inner_text()==desc
   assert panels.evaluate_all('es=>es.filter(e=>!e.inert).length')==1
   assert panels.nth(i).is_visible() and not panels.nth((i+1)%4).is_visible()
   assert s.evaluate('e=>e.offsetHeight')==height and page.locator('.company-stats').evaluate('e=>e.offsetTop')==following
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   assert panels.nth(i).evaluate('s=>[...s.querySelectorAll("h3,p,svg")].every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom})')
   assert panels.nth(i).evaluate('s=>s.querySelector(".strength-graphic").getBoundingClientRect().bottom<=s.querySelector("h3").getBoundingClientRect().top')
   paths.append(panels.nth(i).locator('path').get_attribute('d'))
   assert buttons.nth(i).bounding_box()['height']>=44
   if w>768:
    track=s.locator('.strength-track').bounding_box();marker=s.locator('.strength-track i').bounding_box();assert abs(marker['y']-(track['y']+track['height']*i/4))<1
  assert len(set(paths))==4
  page.keyboard.press('Tab');buttons.nth(3).focus();assert buttons.nth(3).evaluate('e=>getComputedStyle(e).outlineStyle==="solid"')
  page.keyboard.press('Home');assert buttons.nth(0).get_attribute('aria-selected')=='true'
  page.keyboard.press('End');assert buttons.nth(3).get_attribute('aria-selected')=='true'
  page.keyboard.press('ArrowRight' if w<=768 else 'ArrowDown');assert buttons.nth(0).get_attribute('aria-selected')=='true'
  page.keyboard.press('ArrowLeft' if w<=768 else 'ArrowUp');assert buttons.nth(3).get_attribute('aria-selected')=='true'
  page.keyboard.press('Tab');assert panels.nth(3).evaluate('e=>document.activeElement===e')
  if w in [1440,375]:s.screenshot(path=str(root/'.preview'/f'strength-{w}.png'))
  page.set_viewport_size({'width':1024 if w<=768 else 390,'height':844});page.wait_for_timeout(400);assert buttons.nth(3).get_attribute('aria-selected')=='true';assert s.locator('[role="tablist"]').get_attribute('aria-orientation')==('vertical' if w<=768 else 'horizontal')
  # Prior About upgrades remain functional.
  page.locator('.about-story').scroll_into_view_if_needed();page.wait_for_timeout(1000);assert page.locator('.about-story').evaluate('e=>e.classList.contains("show")');assert page.locator('[data-story-image]').evaluate('e=>!e.style.transform&&!e.style.opacity')
  page.locator('[data-purpose-select="1"]').click();assert page.locator('#purpose-panel-1').is_visible()
  if w>768:page.locator('.menu-toggle').click();page.keyboard.press('Escape');assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
  if w==1440:
   cdp=ctx.new_cdp_session(page);expression='getEventListeners(document.querySelector(".strength-selector button")).click.length'
   assert cdp.send('Runtime.evaluate',{'expression':expression,'includeCommandLineAPI':True,'returnByValue':True})['result']['value']==1
   page.evaluate('initStrengthShowcase();initStrengthShowcase()');assert cdp.send('Runtime.evaluate',{'expression':expression,'includeCommandLineAPI':True,'returnByValue':True})['result']['value']==1
  page.locator('header .logo').click();page.wait_for_url('**/index.html');assert not errors,errors;ctx.close();print(f'PASS {w}px: all features/graphics, stable layout, bounds, touch/keys, indicator, resize, prior About interactions and navigation',flush=True)
 for opts in [{'java_script_enabled':False},{'reduced_motion':'reduce'}]:
  ctx=browser.new_context(viewport={'width':390,'height':844},**opts);ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());page=ctx.new_page();page.goto(base+'about.html');page.wait_for_timeout(900);s=page.locator('.why-us');s.scroll_into_view_if_needed()
  if 'java_script_enabled' in opts:
   assert s.locator('.strength-selector').is_hidden();assert all(e.is_visible() for e in s.locator('.strength-panel').all())
  else:
   s.locator('[role="tab"]').last.click();assert s.locator('.is-active path').evaluate('e=>getComputedStyle(e).animationName==="none"');assert s.locator('.is-active').evaluate('e=>getComputedStyle(e).transitionDuration==="0s"')
  ctx.close()
 browser.close()
now=(root/'about.html').read_text(encoding='utf-8');pat=r'<section class="why-us.*?</section>';assert re.sub(pat,'',now,flags=re.S)==re.sub(pat,'',b['about.html'],flags=re.S)
assert (root/'main.js').read_text(encoding='utf-8').startswith(b['main.js'])
for n,d in b['pages'].items():assert hashlib.sha256((root/n).read_bytes()).hexdigest()==d,n
for n,d in b['assets'].items():assert hashlib.sha256((root/'images'/n).read_bytes()).hexdigest()==d,n
print('PASS no JS/reduced motion, idempotent initialization, previous JS and other sections/pages/images preserved',flush=True)
server.shutdown()
