from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
import json,re,hashlib,sys
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent.parent.parent
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if not self.path.startswith('/Yolo_house/'):self.send_error(404);return
  self.path='/'+self.path[len('/Yolo_house/'):];super().do_GET()
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(root)))
Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/Yolo_house/'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in []:
  context=browser.new_context(viewport={'width':w,'height':h},is_mobile=w<=768,has_touch=w<=768)
  if '--require-fonts' not in sys.argv:context.route('https://fonts.googleapis.com/**',lambda r:r.abort())
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(base+'index.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(800)
  if '--require-fonts' in sys.argv:assert page.evaluate('''()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(t=>t.family.replaceAll('"','')===f&&t.status==='loaded'))''')
  section=page.locator('.home-project-cta');section.scroll_into_view_if_needed();page.wait_for_timeout(900)
  assert section.locator('.project-cta-content').evaluate('e=>getComputedStyle(e).opacity==="1"')
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  assert section.evaluate('''s=>[...s.querySelectorAll('h2,p,a')].every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom})''')
  assert section.evaluate('s=>s.querySelector("p").getBoundingClientRect().top>=s.querySelector("h2").getBoundingClientRect().bottom')
  primary=section.locator('.project-cta-primary');secondary=section.locator('.project-cta-secondary')
  for a in [primary,secondary]:
   assert a.bounding_box()['height']>=44
   a.focus();assert a.evaluate('e=>getComputedStyle(e).outlineStyle==="solid"')
  top=page.locator('footer').evaluate('e=>e.offsetTop')
  section.evaluate('e=>e.classList.remove("is-in-view")');page.wait_for_timeout(100)
  section.evaluate('e=>e.classList.add("is-in-view")');page.wait_for_timeout(650)
  assert page.locator('footer').evaluate('e=>e.offsetTop')==top
  if w>768:
   primary.hover();page.wait_for_timeout(350);assert primary.evaluate('e=>getComputedStyle(e).backgroundColor==="rgb(226, 194, 99)"')
   secondary.hover();page.wait_for_timeout(350);assert secondary.evaluate('e=>getComputedStyle(e,"::after").transform==="matrix(1, 0, 0, 1, 0, 0)"')
   r=section.bounding_box();page.mouse.move(r['x']+r['width']*.8,r['y']+r['height']*.7);page.wait_for_timeout(600)
   assert section.evaluate('e=>!!e.style.getPropertyValue("--cta-spot-x")')
  else:assert section.evaluate('e=>!e.style.getPropertyValue("--cta-spot-x")')
  if w in [1440,375]:section.screenshot(path=str(root/'.preview'/f'cta-{w}.png'))
  primary.focus();page.keyboard.press('Enter');page.wait_for_url('**/contact.html');assert page.locator('#project-form').count()==1
  page.goto(base+'index.html');secondary=page.locator('.project-cta-secondary')
  if w<=768:secondary.tap()
  else:secondary.click()
  page.wait_for_url('**/portfolio.html')
  page.goto(base+'index.html');page.wait_for_timeout(800)
  trigger=page.locator('.project-trigger').first;trigger.click();page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"');page.keyboard.press('Escape')
  assert not page.locator('#project-lightbox').evaluate('e=>e.open')
  if w<=768:
   page.locator('.menu-toggle').tap();assert page.locator('nav').evaluate('e=>e.classList.contains("active")');page.keyboard.press('Escape');assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
  assert not errors,errors
  print(f'PASS {w}px: bounds, overflow, targets, focus, reveal stability, navigation, lightbox/menu',flush=True)
  context.close()
 for opts in [{'java_script_enabled':False},{'reduced_motion':'reduce'}]:
  context=browser.new_context(viewport={'width':390,'height':844},**opts);context.route('https://fonts.googleapis.com/**',lambda r:r.abort())
  page=context.new_page();page.goto(base+'index.html');s=page.locator('.home-project-cta');s.scroll_into_view_if_needed();page.wait_for_timeout(700)
  assert s.locator('.project-cta-content').evaluate('e=>getComputedStyle(e).opacity==="1"')
  if 'reduced_motion' in opts:assert s.locator('.project-cta-content').evaluate('e=>getComputedStyle(e).transitionDuration==="0s"')
  context.close()
 print('PASS no-JS and reduced-motion readability')
 browser.close()
b=json.loads((root/'.preview/cta-baseline.json').read_text(encoding='utf-8'));now=(root/'index.html').read_text(encoding='utf-8')
for cls in ['hero','services','portfolio','home-approach']:
 pattern=r'<section class="'+cls+r'(?: [^"]*)?"[^>]*>.*?</section>'
 assert re.search(pattern,now,re.S)[0]==re.search(pattern,b['index.html'],re.S)[0],cls
for tag in ['header','footer','dialog']:
 pattern='<'+tag+r'[^>]*>.*?</'+tag+'>'
 assert re.search(pattern,now,re.S)[0]==re.search(pattern,b['index.html'],re.S)[0],tag
for name,digest in b['pages'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
for name,digest in b['assets'].items():assert hashlib.sha256((root/'assets/images'/name).read_bytes()).hexdigest()==digest
print('PASS preserved sections, other pages and images')
server.shutdown()

