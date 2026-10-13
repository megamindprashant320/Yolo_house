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
 for reduced in [False,True]:
  ctx=browser.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce' if reduced else 'no-preference');ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());page=ctx.new_page();page.goto(base+'about.html');page.wait_for_timeout(900);s=page.locator('.mission-vision');s.scroll_into_view_if_needed();page.wait_for_timeout(900)
  if reduced:
   s.locator('.purpose-panel').first.hover();assert s.locator('.purpose-experience').evaluate('e=>!e.style.getPropertyValue("--purpose-x")');assert s.locator('.purpose-connector span').evaluate('e=>getComputedStyle(e).transitionDuration==="0s"');page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(150);assert s.locator('.purpose-panel').first.evaluate('e=>getComputedStyle(e).transitionDuration==="0s"');s.locator('[data-purpose-select="1"]').click();assert s.locator('#purpose-panel-1').evaluate('e=>getComputedStyle(e).opacity==="1"')
  else:
   s.evaluate('e=>e.classList.remove("show")');page.wait_for_timeout(800);assert s.locator('.purpose-connector span').evaluate('e=>getComputedStyle(e).transform==="matrix(0, 0, 0, 1, 0, 0)"');s.evaluate('e=>e.classList.add("show")');page.wait_for_timeout(800)
   s.locator('[data-purpose-select="1"]').focus();page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(400)
   assert s.locator('[data-purpose-select="0"]').evaluate('e=>document.activeElement===e')
   page.keyboard.press('Tab');assert s.locator('#purpose-panel-0').evaluate('e=>document.activeElement===e&&getComputedStyle(e).outlineStyle==="solid"')
   assert s.locator('.purpose-experience').evaluate('e=>!e.style.getPropertyValue("--purpose-x")')
  ctx.close()
 browser.close()
server.shutdown();print('PASS connector drawing, resize focus, panel keyboard focus, static mobile/reduced-motion illumination')
