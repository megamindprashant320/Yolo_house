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
 for w,h in [(1440,900),(390,844)]:
  ctx=browser.new_context(viewport={'width':w,'height':h},is_mobile=w==390,has_touch=w==390);page=ctx.new_page();pending=[]
  page.route(base+'assets/images/**',lambda route:pending.append(route))
  page.goto(base+'index.html',wait_until='domcontentloaded');page.evaluate('document.fonts.ready');page.wait_for_timeout(400)
  assert page.evaluate("()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(t=>t.family.replaceAll('\"','')===f&&t.status==='loaded'))")
  page.locator('.about').scroll_into_view_if_needed();page.wait_for_timeout(600);before=page.locator('.about').evaluate('e=>e.offsetHeight')
  for route in list(pending):route.fulfill(status=200,content_type='image/jpeg',body=(root/'assets/images'/route.request.url.split('/')[-1]).read_bytes())
  page.wait_for_timeout(900);assert page.locator('.about').evaluate('e=>e.offsetHeight')==before
  page.unroute(base+'assets/images/**')
  page.locator('.services').scroll_into_view_if_needed();page.wait_for_timeout(700)
  if w==1440:
   frame=page.locator('.showcase-frame').first;initial=frame.evaluate('e=>getComputedStyle(e).transform');frame.hover();page.wait_for_timeout(550);assert frame.evaluate('e=>getComputedStyle(e).transform')!=initial
  else:page.locator('.studio-card-body').first.tap();assert page.locator('.studio-card-body p').first.is_visible()
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(850)
  assert page.locator('.hero').evaluate('s=>[...s.querySelectorAll("h1,h2,p,a,.hero-stat-value")].every(e=>{let r=e.getBoundingClientRect(),b=s.getBoundingClientRect();return r.left>=b.left&&r.right<=b.right&&r.top>=b.top&&r.bottom<=b.bottom})')
  page.locator('.home-footer').scroll_into_view_if_needed();page.wait_for_timeout(900);page.evaluate('scrollTo(0,document.documentElement.scrollHeight)');page.wait_for_timeout(600)
  assert page.locator('.footer-bottom').evaluate('s=>{let t=document.querySelector("#topBtn").getBoundingClientRect();return [...s.querySelectorAll("p")].every(e=>{let r=e.getBoundingClientRect();return r.right<=t.left||r.left>=t.right||r.bottom<=t.top||r.top>=t.bottom})}')
  page.screenshot(path=str(root/'.preview'/f'optimized-footer-{w}.png'))
  print(f'PASS {w}px: actual fonts, delayed image height stability, service hover/tap, hero bounds, footer control separation',flush=True)
  ctx.close()
 browser.close()
server.shutdown()
def lum(hex):
 v=[int(hex[i:i+2],16)/255 for i in (0,2,4)];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v];return sum(x*y for x,y in zip(v,[.2126,.7152,.0722]))
for text,bg in [('d4af37','0b0b0b'),('c6c3bb','10100d'),('bbb7ad','080808'),('111111','d4af37')]:
 a,b=sorted([lum(text),lum(bg)]);ratio=(b+.05)/(a+.05);assert ratio>=4.5;print(f'Contrast spot check #{text}/#{bg}: {ratio:.2f}:1')
