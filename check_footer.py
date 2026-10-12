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
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Users\win11\AppData\Local\Google\Chrome\Application\chrome.exe' if False else r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]:
  context=browser.new_context(viewport={'width':w,'height':h},is_mobile=w<=768,has_touch=w<=768)
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(base+'index.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(700)
  assert page.evaluate("()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(t=>t.family.replaceAll('\"','')===f&&t.status==='loaded'))")
  footer=page.locator('.home-footer');footer.scroll_into_view_if_needed();page.wait_for_timeout(700)
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  assert footer.evaluate('s=>[...s.querySelectorAll("p,h2,a")].every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom})')
  assert footer.locator('[data-footer-year]').inner_text()==page.evaluate('String(new Date().getFullYear())')
  assert footer.locator('a[href="#"],a[href=""],a[href^="mailto:"],a[href^="tel:"]').count()==0
  links=footer.locator('a');destinations=links.evaluate_all('els=>els.map(e=>e.getAttribute("href"))')
  for i,url in enumerate(destinations):
   a=page.locator('.home-footer a').nth(i);a.scroll_into_view_if_needed();a.focus()
   assert a.evaluate('e=>getComputedStyle(e).outlineStyle==="solid"')
   assert a.bounding_box()['height']>=44
   if w<=768:a.tap()
   else:a.click()
   page.wait_for_url('**/'+url);page.locator('header').wait_for(state='visible')
   page.goto(base+'index.html');page.wait_for_timeout(350)
  footer=page.locator('.home-footer');footer.scroll_into_view_if_needed();page.wait_for_timeout(600)
  if w in [1440,375]:
   page.locator('header').evaluate('e=>e.style.visibility="hidden"');footer.screenshot(path=str(root/'.preview'/f'footer-{w}.png'));page.locator('header').evaluate('e=>e.style.visibility=""')
  page.locator('#topBtn').click();page.wait_for_function('scrollY<2')
  trigger=page.locator('.project-trigger').first;trigger.click();page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"');page.keyboard.press('Escape');assert not page.locator('#project-lightbox').evaluate('e=>e.open')
  if w<=768:
   page.locator('.menu-toggle').tap();assert page.locator('nav').first.evaluate('e=>e.classList.contains("active")');page.keyboard.press('Escape')
  assert not errors,errors
  print(f'PASS {w}px: fonts, bounds, no overflow, all footer links/logo, focus/touch, year, back-to-top, viewer/menu',flush=True)
  context.close()
 for options in [{'java_script_enabled':False},{'reduced_motion':'reduce'}]:
  context=browser.new_context(viewport={'width':390,'height':844},**options);context.route('https://fonts.googleapis.com/**',lambda r:r.abort())
  page=context.new_page();page.goto(base+'index.html');footer=page.locator('.home-footer');footer.scroll_into_view_if_needed()
  assert footer.locator('.footer-navigation').is_visible()
  if 'reduced_motion' in options:assert footer.locator('.footer-column').first.evaluate('e=>getComputedStyle(e,"::before").transitionDuration==="0s"')
  context.close()
 browser.close()
b=json.loads((root/'.preview/footer-baseline.json').read_text(encoding='utf-8'));now=(root/'index.html').read_text(encoding='utf-8')
assert re.sub(r'<footer.*?</footer>','',now,flags=re.S)==re.sub(r'<footer.*?</footer>','',b['index.html'],flags=re.S)
assert (root/'style.css').read_text(encoding='utf-8').startswith(b['style.css'])
assert (root/'main.js').read_text(encoding='utf-8').startswith(b['main.js'])
for n,d in b['pages'].items():assert hashlib.sha256((root/n).read_bytes()).hexdigest()==d
for n,d in b['assets'].items():assert hashlib.sha256((root/'images'/n).read_bytes()).hexdigest()==d
print('PASS reduced motion/no JS, exact preservation of previous code/pages/assets',flush=True)
server.shutdown()

