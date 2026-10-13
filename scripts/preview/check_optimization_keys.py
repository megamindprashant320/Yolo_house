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
 ctx=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);ctx.route('https://fonts.googleapis.com/**',lambda r:r.abort());page=ctx.new_page();page.goto(base+'index.html')
 page.locator('.project-trigger').first.tap();page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"')
 page.keyboard.press('ArrowLeft');page.wait_for_function('document.querySelector(".viewer-counter").textContent==="06 / 06"&&document.querySelector("#project-lightbox").dataset.state==="ready"')
 page.keyboard.press('ArrowRight');page.wait_for_function('document.querySelector(".viewer-counter").textContent==="01 / 06"&&document.querySelector("#project-lightbox").dataset.state==="ready"')
 page.keyboard.press('Escape');page.locator('.menu-toggle').tap();page.locator('.nav-overlay').tap(position={'x':5,'y':100});assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
 page.locator('.menu-toggle').tap();page.locator('#primary-navigation a').last.tap();page.wait_for_url('**/contact.html');assert page.locator('#project-form').count()==1
 ctx.close();browser.close()
server.shutdown();print('PASS ArrowLeft/ArrowRight wrap, mobile backdrop dismissal, actual drawer-link navigation')
