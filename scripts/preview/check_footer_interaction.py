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
 page=browser.new_page(viewport={'width':1440,'height':900});page.route('https://fonts.googleapis.com/**',lambda r:r.abort());page.goto(base+'index.html')
 f=page.locator('.home-footer');f.scroll_into_view_if_needed();page.wait_for_timeout(750)
 a=f.locator('.footer-navigation a').nth(1);a.hover();page.wait_for_timeout(300)
 assert a.evaluate('e=>getComputedStyle(e,"::after").transform==="matrix(1, 0, 0, 1, 0, 0)"')
 a.focus();page.keyboard.press('Enter');page.wait_for_url('**/about.html')
 page.goto(base+'index.html');f=page.locator('.home-footer');f.scroll_into_view_if_needed();page.wait_for_timeout(700)
 before=f.evaluate('e=>e.offsetHeight');f.locator('.footer-column').evaluate_all('els=>els.forEach(e=>e.classList.remove("show"))');page.wait_for_timeout(100);f.locator('.footer-column').evaluate_all('els=>els.forEach(e=>e.classList.add("show"))');page.wait_for_timeout(750);assert f.evaluate('e=>e.offsetHeight')==before
 browser.close()
server.shutdown()
print('PASS desktop underline hover, keyboard Enter navigation, divider height stability')
