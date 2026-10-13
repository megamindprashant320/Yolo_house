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
b=json.loads((root/'.preview/story-baseline.json').read_text(encoding='utf-8'))
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]:
  ctx=browser.new_context(viewport={'width':w,'height':h},is_mobile=w<=768,has_touch=w<=768);page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(base+'about.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(900)
  assert page.evaluate("()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(t=>t.family.replaceAll('\"','')===f&&t.status==='loaded'))")
  story=page.locator('.about-story');height=story.evaluate('e=>e.offsetHeight');following=page.locator('.mission-vision').evaluate('e=>e.offsetTop')
  story.scroll_into_view_if_needed();page.wait_for_timeout(1200)
  assert story.evaluate('e=>e.classList.contains("show")')
  assert story.locator('.story-entrance').evaluate_all('es=>es.every(e=>getComputedStyle(e).opacity==="1"&&getComputedStyle(e).transform==="none")')
  assert story.locator('.story-image-media').evaluate('e=>getComputedStyle(e).clipPath==="inset(0px)"')
  assert story.evaluate('e=>e.offsetHeight')==height and page.locator('.mission-vision').evaluate('e=>e.offsetTop')==following
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  assert story.evaluate('s=>[...s.querySelectorAll("img,h2,p,a")].every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom})')
  im=story.locator('img');assert abs(im.bounding_box()['width']/im.bounding_box()['height']-1)<.01
  assert im.evaluate('e=>e.naturalWidth===1129&&!e.style.transform&&!e.style.opacity')
  if w in [1440,375]:
   page.locator('header').evaluate('e=>e.style.visibility="hidden"');story.screenshot(path=str(root/'.preview'/f'story-{w}.png'));page.locator('header').evaluate('e=>e.style.visibility=""')
  cta=story.locator('.story-work-link');cta.focus();assert cta.evaluate('e=>getComputedStyle(e).outlineStyle==="solid"');assert cta.bounding_box()['height']>=44
  if w<=768:cta.tap()
  else:page.keyboard.press('Enter')
  page.wait_for_url('**/portfolio.html');page.goto(base+'about.html');page.wait_for_timeout(900)
  if w<=768:
   page.locator('.menu-toggle').tap();assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='true';page.keyboard.press('Escape');assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
  page.locator('header .logo').click();page.wait_for_url('**/index.html')
  assert not errors,errors;print(f'PASS {w}px: fonts, reveal/text completion, stable height, bounds, image ratio, focus, CTA and navbar',flush=True);ctx.close()
 for opts in [{'java_script_enabled':False},{'reduced_motion':'reduce'}]:
  ctx=browser.new_context(viewport={'width':390,'height':844},**opts);ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());page=ctx.new_page();page.goto(base+'about.html');page.wait_for_timeout(900)
  if 'java_script_enabled' in opts:assert not page.locator('.preloader').is_visible()
  story=page.locator('.about-story');story.scroll_into_view_if_needed();page.wait_for_timeout(300)
  assert story.locator('p').evaluate_all('es=>es.every(e=>getComputedStyle(e).opacity==="1")')
  assert story.locator('.story-image-media').evaluate('e=>["none","inset(0px)"].includes(getComputedStyle(e).clipPath)')
  if 'reduced_motion' in opts:assert story.locator('img').evaluate('e=>getComputedStyle(e).transitionDuration==="0s"')
  ctx.close()
 browser.close()
now=(root/'about.html').read_text(encoding='utf-8').replace('<noscript><style>.preloader{display:none;}</style></noscript>\n\n','');pat=r'<section class="about-story[^>]*>.*?</section>'
assert re.sub(pat,'',now,flags=re.S)==re.sub(pat,'',b['about.html'],flags=re.S)
old=re.search(pat,b['about.html'],re.S)[0];new=re.search(pat,now,re.S)[0]
assert [re.sub(r'\s+',' ',x).strip() for x in re.findall(r'<p[^>]*>(.*?)</p>',old,re.S)]==[re.sub(r'\s+',' ',x).strip() for x in re.findall(r'<p[^>]*>(.*?)</p>',new,re.S)]
for n,d in b['pages'].items():assert hashlib.sha256((root/n).read_bytes()).hexdigest()==d,n
for n,d in b['assets'].items():assert hashlib.sha256((root/'assets/images'/n).read_bytes()).hexdigest()==d,n
print('PASS fallback/reduced motion, unchanged copy, other sections/pages/assets',flush=True)
server.shutdown()
