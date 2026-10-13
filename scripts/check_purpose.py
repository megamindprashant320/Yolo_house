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
b=json.loads((root/'.preview/purpose-baseline.json').read_text(encoding='utf-8'))
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]:
  ctx=browser.new_context(viewport={'width':w,'height':h},is_mobile=w<=768,has_touch=w<=768);page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(base+'about.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(900)
  assert page.evaluate("()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(t=>t.family.replaceAll('\"','')===f&&t.status==='loaded'))")
  section=page.locator('.mission-vision');section.scroll_into_view_if_needed();page.wait_for_timeout(800)
  buttons=section.locator('[data-purpose-select]');panels=section.locator('.purpose-panel');height=section.evaluate('e=>e.offsetHeight');after=page.locator('.why-us').evaluate('e=>e.offsetTop')
  assert section.evaluate('e=>e.classList.contains("show")')
  for i in [1,0,1]:
   if w<=768:buttons.nth(i).tap()
   else:buttons.nth(i).click()
   page.wait_for_timeout(400)
   assert buttons.nth(i).get_attribute('aria-selected' if w<=768 else 'aria-pressed')=='true'
   assert panels.nth(i).is_visible()
   assert panels.nth(1-i).is_visible()==(w>768)
   assert panels.nth(1-i).evaluate('e=>e.inert')==(w<=768)
   assert section.evaluate('e=>e.offsetHeight')==height and page.locator('.why-us').evaluate('e=>e.offsetTop')==after
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   assert panels.nth(i).evaluate('s=>[...s.querySelectorAll("h3,p")].every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom})')
  page.keyboard.press("Tab");buttons.nth(1).focus();assert buttons.nth(1).evaluate('e=>getComputedStyle(e).outlineStyle==="solid"');assert buttons.nth(1).bounding_box()['height']>=44
  if w<=768:
   y=page.evaluate('scrollY');page.keyboard.press('Home');assert buttons.nth(0).evaluate('e=>document.activeElement===e');assert abs(page.evaluate('scrollY')-y)<2
   page.keyboard.press('End');assert buttons.nth(1).get_attribute('aria-selected')=='true'
   page.keyboard.press('ArrowRight');assert buttons.nth(0).get_attribute('aria-selected')=='true'
   page.keyboard.press('ArrowLeft');assert buttons.nth(1).get_attribute('aria-selected')=='true'
   assert buttons.nth(0).get_attribute('tabindex')=='-1'
  else:
   assert buttons.nth(1).get_attribute('role') is None
   buttons.nth(0).focus();page.keyboard.press('Space');assert buttons.nth(0).get_attribute('aria-pressed')=='true'
   panels.nth(0).scroll_into_view_if_needed();page.wait_for_timeout(800);page.mouse.move(5,5);panels.nth(0).hover();page.wait_for_function('!!document.querySelector(".purpose-experience").style.getPropertyValue("--purpose-x")')
  if w in [1440,375]:section.screenshot(path=str(root/'.preview'/f'purpose-{w}.png'))
  # Preserve selected state while changing semantics and visibility at the breakpoint.
  buttons.nth(1).click();page.set_viewport_size({'width':1024 if w<=768 else 390,'height':844});page.wait_for_timeout(500)
  assert buttons.nth(1).get_attribute('aria-pressed' if w<=768 else 'aria-selected')=='true'
  assert panels.nth(0).is_visible()==(w<=768)
  page.locator('.menu-toggle').click() if w>768 else None
  if w>768:page.keyboard.press('Escape')
  assert not errors,errors;ctx.close();print(f'PASS {w}px: fonts, selection, stable layout, bounds, semantics, keyboard/touch, resize and graphics',flush=True)
 for opts in [{'java_script_enabled':False},{'reduced_motion':'reduce'}]:
  ctx=browser.new_context(viewport={'width':390,'height':844},**opts);ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());page=ctx.new_page();page.goto(base+'about.html');page.wait_for_timeout(900);section=page.locator('.mission-vision');section.scroll_into_view_if_needed()
  if 'java_script_enabled' in opts:
   assert section.locator('.purpose-selectors').is_hidden();assert section.locator('.purpose-panel').nth(0).is_visible() and section.locator('.purpose-panel').nth(1).is_visible();assert page.locator('.preloader').is_hidden()
  else:assert section.locator('.purpose-connector span').evaluate('e=>getComputedStyle(e).transitionDuration==="0s"')
  ctx.close()
 browser.close()
now=(root/'about.html').read_text(encoding='utf-8');pat=r'<section class="mission-vision.*?</section>'
assert re.sub(pat,'',now,flags=re.S)==re.sub(pat,'',b['about.html'],flags=re.S)
for n,d in b['pages'].items():assert hashlib.sha256((root/n).read_bytes()).hexdigest()==d,n
for n,d in b['assets'].items():assert hashlib.sha256((root/'assets/images'/n).read_bytes()).hexdigest()==d,n
for text in re.findall(r'<h3>(.*?)</h3>|<p>(.*?)</p>',re.search(pat,b['about.html'],re.S)[0]):
 assert next(x for x in text if x) in now
print('PASS no JS/reduced motion, statements and other sections/pages/assets preserved',flush=True)
server.shutdown()
