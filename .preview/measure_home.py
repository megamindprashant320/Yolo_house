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
import urllib.request
try:
 for url in ['https://megamindprashant320.github.io/Yolo_house/','https://megamindprashant320.github.io/Yolo_house/images/hero.jpg']:
  with urllib.request.urlopen(url,timeout=25) as response:print('PUBLIC URL',response.status,response.url,response.headers.get('Content-Type'),flush=True)
except Exception as e:print('PUBLIC CHECK FAILED',str(e),flush=True)
results={}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for name,w,h in [('desktop',1440,900),('mobile',390,844)]:
  context=browser.new_context(viewport={'width':w,'height':h},is_mobile=name=='mobile',has_touch=name=='mobile')
  page=context.new_page();page.add_init_script("window.lab={lcp:0,cls:0,longTasks:0};new PerformanceObserver(l=>l.getEntries().forEach(e=>lab.lcp=e.startTime)).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(!e.hadRecentInput)lab.cls+=e.value})).observe({type:'layout-shift',buffered:true});new PerformanceObserver(l=>l.getEntries().forEach(e=>lab.longTasks+=e.duration)).observe({type:'longtask',buffered:true})")
  page.goto(base+'index.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(5000)
  results[name]=page.evaluate("({...lab,fcp:performance.getEntriesByName('first-contentful-paint')[0]?.startTime,resourceBytes:performance.getEntriesByType('resource').reduce((s,e)=>s+e.transferSize,0),imagesRequested:performance.getEntriesByType('resource').filter(e=>e.name.includes('/images/')).length})")
  print(name,results[name],flush=True);context.close()
 browser.close()
(root/'.preview'/('optimization-'+sys.argv[1]+'-metrics.json')).write_text(json.dumps(results,indent=2),encoding='utf-8')
server.shutdown()
