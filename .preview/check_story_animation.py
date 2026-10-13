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
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for w,h in [(1440,900),(375,667)]:
  ctx=browser.new_context(viewport={'width':w,'height':h});ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());page=ctx.new_page();page.goto(base+'about.html');page.wait_for_timeout(900);story=page.locator('.about-story');story.scroll_into_view_if_needed();page.wait_for_timeout(1100)
  before=story.evaluate('e=>e.offsetHeight');story.evaluate('e=>e.classList.remove("show")');page.wait_for_timeout(1100)
  assert story.locator('.story-image-media').evaluate('e=>getComputedStyle(e).clipPath.includes("100%")')
  assert story.locator('h2').evaluate('e=>getComputedStyle(e).opacity==="0"')
  story.evaluate('e=>e.classList.add("show")');page.wait_for_timeout(200)
  assert story.locator('h2').evaluate('e=>{let n=+getComputedStyle(e).opacity;return n>0&&n<1}')
  page.wait_for_timeout(1000);assert story.evaluate('e=>e.offsetHeight')==before
  story.evaluate('e=>e.classList.remove("show")');story.locator('a').focus();assert story.evaluate('e=>e.classList.contains("show")')
  ctx.close();print(f'PASS {w}px: masked initial state, intermediate heading animation, completion without height shift, focus reveal')
 ctx=browser.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce');ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());page=ctx.new_page();page.goto(base+'about.html');page.wait_for_timeout(900);page.locator('.story-image').hover()
 assert page.locator('[data-story-image]').evaluate('e=>getComputedStyle(e).transform==="none"')
 page.locator('.story-work-link').hover();assert page.locator('.story-work-link svg').evaluate('e=>getComputedStyle(e).transform==="none"')
 print('PASS desktop reduced-motion image/button hover')
 ctx.close();browser.close()
server.shutdown()
