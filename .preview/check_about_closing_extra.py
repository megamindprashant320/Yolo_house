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
  ctx=browser.new_context(viewport={'width':w,'height':h},is_mobile=w==375,has_touch=w==375);page=ctx.new_page();page.goto(base+'about.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(900)
  cta=page.locator('.about-project-cta');cta.scroll_into_view_if_needed();page.wait_for_function('getComputedStyle(document.querySelector(".project-cta-content")).opacity==="1"');page.wait_for_timeout(300)
  if w==1440:
   cta.locator('h2').hover();page.wait_for_function('!!document.querySelector(".about-project-cta").style.getPropertyValue("--cta-spot-x")')
   cta.locator('.project-cta-secondary').hover();page.wait_for_timeout(400);assert cta.locator('.project-cta-secondary').evaluate('e=>getComputedStyle(e,"::after").transform==="matrix(1, 0, 0, 1, 0, 0)"')
  else:assert cta.evaluate('e=>!e.style.getPropertyValue("--cta-spot-x")')
  style='header,#topBtn,#progress-bar,.custom-cursor{visibility:hidden !important;}'
  cta.screenshot(path=str(root/'.preview'/f'about-cta-{w}.png'),style=style)
  footer=page.locator('.home-footer');footer.scroll_into_view_if_needed();page.wait_for_timeout(900);footer.screenshot(path=str(root/'.preview'/f'about-footer-{w}.png'),style=style)
  page.locator('#topBtn').focus();page.keyboard.press('Enter');page.wait_for_function('scrollY<2')
  ctx.close();print(f'PASS {w}px: settled CTA visibility, desktop spotlight/underline or static touch, keyboard Back to Top',flush=True)
 browser.close()
server.shutdown()
