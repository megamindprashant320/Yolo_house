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
b=json.loads((root/'.preview/about-closing-baseline.json').read_text(encoding='utf-8'))
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]:
  ctx=browser.new_context(viewport={'width':w,'height':h},is_mobile=w<=768,has_touch=w<=768);page=ctx.new_page();errors=[];bad=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:bad.append(r.url) if r.url.startswith(base) and r.status>=400 else None);page.goto(base+'about.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(900)
  assert page.evaluate("()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(t=>t.family.replaceAll('\"','')===f&&t.status==='loaded'))")
  cta=page.locator('.about-project-cta');cta.scroll_into_view_if_needed();page.wait_for_timeout(800)
  assert cta.evaluate('e=>e.classList.contains("is-in-view")')
  assert cta.locator('.project-cta-content').evaluate('e=>getComputedStyle(e).opacity==="1"')
  before=page.locator('footer').evaluate('e=>e.offsetTop');cta.evaluate('e=>e.classList.remove("is-in-view")');page.wait_for_timeout(100);cta.evaluate('e=>e.classList.add("is-in-view")');page.wait_for_timeout(600);assert page.locator('footer').evaluate('e=>e.offsetTop')==before
  for selector in ['.about-project-cta','.home-footer']:
   s=page.locator(selector);s.scroll_into_view_if_needed();page.wait_for_timeout(600);assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');assert s.evaluate('s=>[...s.querySelectorAll("h2,p,a")].every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom})')
  footer=page.locator('.home-footer');assert footer.locator('[data-footer-year]').inner_text()==page.evaluate('String(new Date().getFullYear())');assert footer.locator('a[aria-current="page"]').get_attribute('href')=='about.html'
  assert footer.locator('a[href="#"],a[href=""],a[href^="mailto:"],a[href^="tel:"]').count()==0
  for selector in ['.project-cta-primary','.project-cta-secondary','.home-footer a']:
   targets=page.locator(selector).evaluate_all('es=>es.map(e=>e.getAttribute("href"))')
   for i,url in enumerate(targets):
    a=page.locator(selector).nth(i);a.scroll_into_view_if_needed();page.keyboard.press('Tab');a.focus();assert a.evaluate('e=>getComputedStyle(e).outlineStyle==="solid"');assert a.bounding_box()['height']>=44
    with page.expect_navigation(wait_until='load'):
     if w<=768:a.tap()
     else:page.keyboard.press('Enter')
    assert page.url==base+url
    page.goto(base+'about.html');page.wait_for_timeout(150)
  page.locator('.home-footer').scroll_into_view_if_needed();page.wait_for_timeout(650);page.evaluate('scrollTo(0,document.documentElement.scrollHeight)');page.wait_for_timeout(600)
  assert page.locator('.footer-bottom').evaluate('s=>{let t=document.querySelector("#topBtn").getBoundingClientRect();return [...s.querySelectorAll("p")].every(e=>{let r=e.getBoundingClientRect();return r.right<=t.left||r.bottom<=t.top||r.top>=t.bottom})}')
  if w in [1440,375]:
   page.locator('.about-project-cta').screenshot(path=str(root/'.preview'/f'about-cta-{w}.png'));page.locator('.home-footer').screenshot(path=str(root/'.preview'/f'about-footer-{w}.png'))
  page.locator('#topBtn').click();page.wait_for_function('scrollY<2')
  page.locator('.about-story').scroll_into_view_if_needed();page.wait_for_timeout(900);assert page.locator('.about-story').evaluate('e=>e.classList.contains("show")')
  page.locator('[data-purpose-select="1"]').click();assert page.locator('#purpose-panel-1').evaluate('e=>e.classList.contains("is-active")')
  page.locator('#strength-tab-3').click();assert page.locator('#strength-panel-3').is_visible()
  page.locator('.company-stats').scroll_into_view_if_needed();page.wait_for_timeout(900);assert page.locator('.company-stats').evaluate('e=>e.classList.contains("show")');assert page.locator('.company-stats dd').count()==0
  if w<=768:page.locator('.menu-toggle').tap();page.keyboard.press('Escape');assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
  # Footer geometry matches the approved local homepage at the same viewport.
  page.goto(base+'index.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(700);home=page.locator('.home-footer');home.scroll_into_view_if_needed();page.wait_for_timeout(500)
  home_geometry=home.evaluate('s=>[s,...s.querySelectorAll(".footer-layout,.footer-column,.footer-bottom")].map(e=>[e.offsetWidth,e.offsetHeight])')
  trigger=page.locator('.project-trigger').first;trigger.click();page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"');page.keyboard.press('Escape')
  page.goto(base+'about.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(700);about=page.locator('.home-footer');about.scroll_into_view_if_needed();page.wait_for_timeout(500)
  assert about.evaluate('s=>[s,...s.querySelectorAll(".footer-layout,.footer-column,.footer-bottom")].map(e=>[e.offsetWidth,e.offsetHeight])')==home_geometry
  assert not errors and not bad,(errors,bad);ctx.close();print(f'PASS {w}px: CTA reveal/bounds, all links, focus/touch, footer match/year, back-to-top, About/navbar and homepage viewer regression',flush=True)
 for opts in [{'java_script_enabled':False},{'reduced_motion':'reduce'}]:
  ctx=browser.new_context(viewport={'width':390,'height':844},**opts);ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());page=ctx.new_page();page.goto(base+'about.html');page.wait_for_timeout(900);s=page.locator('.about-project-cta');s.scroll_into_view_if_needed()
  assert s.locator('.project-cta-content').evaluate('e=>getComputedStyle(e).opacity==="1"');assert page.locator('.footer-navigation').is_visible()
  if 'reduced_motion' in opts:assert s.locator('.project-cta-content').evaluate('e=>getComputedStyle(e).transitionDuration==="0s"')
  ctx.close()
 browser.close()
now=(root/'about.html').read_text(encoding='utf-8')
old=re.sub(r'<section class="cta about-cta">.*?</section>|<footer.*?</footer>','',b['about.html'],flags=re.S)
new=re.sub(r'<section class="home-project-cta about-project-cta.*?</section>|<footer.*?</footer>','',now,flags=re.S);assert old==new
assert (root/'main.js').read_text(encoding='utf-8')==b['main.js']
for n,d in b['pages'].items():assert hashlib.sha256((root/n).read_bytes()).hexdigest()==d,n
for n,d in b['assets'].items():assert hashlib.sha256((root/'images'/n).read_bytes()).hexdigest()==d,n
print('PASS reduced motion/no JS, unchanged previous About markup, main.js, homepage/other pages and images',flush=True)
server.shutdown()
