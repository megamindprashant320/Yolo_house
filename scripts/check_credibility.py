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
b=json.loads((root/'.preview/credibility-baseline.json').read_text(encoding='utf-8'))
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]:
  ctx=browser.new_context(viewport={'width':w,'height':h},is_mobile=w<=768,has_touch=w<=768);page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(base+'about.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(900)
  s=page.locator('.company-stats');height=s.evaluate('e=>e.offsetHeight');after=page.locator('.about-cta').evaluate('e=>e.offsetTop');s.scroll_into_view_if_needed();page.wait_for_timeout(900)
  assert s.evaluate('e=>e.classList.contains("show")')
  assert s.locator('.credibility-sequence path').evaluate('e=>getComputedStyle(e).strokeDashoffset==="0px"')
  assert s.evaluate('e=>e.offsetHeight')==height and page.locator('.about-cta').evaluate('e=>e.offsetTop')==after
  assert not re.search(r'18\+|100\+|50\+|15\+',s.inner_text())
  assert s.locator('dd,[data-counter],[role="progressbar"]').count()==0
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  assert s.evaluate('s=>[...s.querySelectorAll("h2,p,a,.credibility-sequence")].every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom})')
  if w in [1440,375]:s.screenshot(path=str(root/'.preview'/f'credibility-{w}.png'))
  page.keyboard.press('Tab');a=s.locator('a');a.focus();assert a.evaluate('e=>getComputedStyle(e).outlineStyle==="solid"');assert a.bounding_box()['height']>=44
  if w<=768:a.tap()
  else:page.keyboard.press('Enter')
  page.wait_for_url('**/portfolio.html');page.goto(base+'about.html');page.wait_for_timeout(900)
  page.locator('.about-story').scroll_into_view_if_needed();page.wait_for_timeout(1000);assert page.locator('.about-story').evaluate('e=>e.classList.contains("show")')
  page.locator('[data-purpose-select="1"]').click();assert page.locator('#purpose-panel-1').evaluate('e=>e.classList.contains("is-active")')
  page.locator('#strength-tab-2').click();assert page.locator('#strength-panel-2').is_visible()
  if w<=768:page.locator('.menu-toggle').tap();page.keyboard.press('Escape');assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
  page.set_viewport_size({'width':1024 if w<=768 else 390,'height':844});page.locator('.company-stats').scroll_into_view_if_needed();assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  assert not errors,errors;ctx.close();print(f'PASS {w}px: no unverified numbers, reveal/stable layout, bounds, focus, actual Portfolio link, resize and About regression',flush=True)
 for opts in [{'java_script_enabled':False},{'reduced_motion':'reduce'}]:
  ctx=browser.new_context(viewport={'width':390,'height':844},**opts);ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());page=ctx.new_page();page.goto(base+'about.html');page.wait_for_timeout(900);s=page.locator('.company-stats');s.scroll_into_view_if_needed()
  assert s.locator('h2').is_visible() and s.locator('p').is_visible() and s.locator('a').is_visible()
  assert s.locator('path').first.evaluate('e=>getComputedStyle(e).strokeDashoffset==="0px"')
  if 'reduced_motion' in opts:assert s.locator('path').first.evaluate('e=>getComputedStyle(e).transitionDuration==="0s"')
  ctx.close()
 browser.close()
now=(root/'about.html').read_text(encoding='utf-8');pat=r'<section class="company-stats.*?</section>';assert re.sub(pat,'',now,flags=re.S)==re.sub(pat,'',b['about.html'],flags=re.S)
js=(root/'assets/js/main.js').read_text(encoding='utf-8').replace('entry.target.matches(".about-story,.mission-vision,.company-stats")','entry.target.matches(".about-story,.mission-vision")');assert js.startswith(b['main.js'])
for n,d in b['pages'].items():assert hashlib.sha256((root/n).read_bytes()).hexdigest()==d,n
for n,d in b['assets'].items():assert hashlib.sha256((root/'assets/images'/n).read_bytes()).hexdigest()==d,n
print('PASS no JS/reduced motion, other sections/pages/images and existing interactions code preserved',flush=True)
server.shutdown()
