"""Organization-only validation and before/after Chrome regression checks.

Run from any directory: python scripts/check_structure.py [--static] [--width N].
The original source is replayed read-only; archived mutators are never executed.
"""
from pathlib import Path
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
from urllib.parse import urlsplit, unquote
import ast, hashlib, io, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
PAGES=['index.html','about.html','services.html','portfolio.html','contact.html']
INVENTORY=json.loads((ROOT/'.preview/refactor-inventory.json').read_text(encoding='utf-8'))
SIZES=[(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]
if '--width' in sys.argv:SIZES=[x for x in SIZES if x[0]==int(sys.argv[sys.argv.index('--width')+1])]
RESULTS={'static':{},'browser':[],'preexisting_limitations':[]}

def old_html(s):
    return s.replace('assets/images/','images/').replace('assets/css/style.css','style.css').replace('assets/js/main.js','main.js')

def validate_ref(ref,origin):
    u=urlsplit(ref)
    if u.scheme in ['data','mailto','tel','javascript']:return
    if u.netloc:
        if u.netloc!='megamindprashant320.github.io':return
        assert u.path.startswith('/Yolo_house/'),ref
        path=ROOT/unquote(u.path[len('/Yolo_house/'):])
    elif not u.path:return
    else:
        assert not u.path.startswith('/'),f'Domain-root reference: {ref}'
        path=origin.parent/unquote(u.path)
    path=path.resolve()
    assert path.is_relative_to(ROOT),ref
    if path.is_dir():path=path/'index.html'
    assert path.is_file(),f'Missing {ref} from {origin.relative_to(ROOT)}'
    cursor=ROOT
    for part in path.relative_to(ROOT).parts:
        assert part in {p.name for p in cursor.iterdir()},f'Case mismatch: {ref}'
        cursor=cursor/part

class References(HTMLParser):
    def __init__(self,path):super().__init__();self.path=path;self.count=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        for key in ['src','href','poster']:
            if key in attrs:validate_ref(attrs[key],self.path);self.count+=1
        if 'srcset' in attrs:
            for candidate in attrs['srcset'].split(','):validate_ref(candidate.strip().split()[0],self.path);self.count+=1
        if tag=='meta' and attrs.get('property',attrs.get('name')) in ['og:image','twitter:image']:
            validate_ref(attrs['content'],self.path);self.count+=1
        for ref in re.findall(r'url\([\s\"\']*([^\"\')\s]+)',attrs.get('style','')):validate_ref(ref,self.path);self.count+=1

def static_checks():
    assert {p.name for p in ROOT.glob('*.html')}==set(PAGES)
    for page in PAGES:assert old_html((ROOT/page).read_text(encoding='utf-8'))==INVENTORY['source'][page],page
    css=ROOT/'assets/css/style.css'
    assert css.read_text(encoding='utf-8').replace('../images/','images/')==INVENTORY['source']['style.css']
    for item in INVENTORY['files']:
        source=item['path'];target=INVENTORY['moves'].get(source,source);path=ROOT/target
        assert path.is_file(),target
        if target!=source:assert not (ROOT/source).exists(),source
        if path.suffix=='.py' or (target.startswith('docs/') and path.suffix=='.md'):continue
        if source in PAGES or source=='style.css':continue
        assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],target
    count=0
    for name in PAGES:
        parser=References(ROOT/name);parser.feed((ROOT/name).read_text(encoding='utf-8'));count+=parser.count
    for ref in re.findall(r'url\([\s\"\']*([^\"\')\s]+)',css.read_text(encoding='utf-8')):validate_ref(ref,css);count+=1
    scripts=list((ROOT/'scripts').rglob('*.py'))
    for path in scripts:ast.parse(path.read_text(encoding='utf-8-sig'),filename=str(path))
    links=0
    for path in (ROOT/'docs').rglob('*.md'):
        text=path.read_text(encoding='utf-8-sig')
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
            target=target.strip('<>').split('#')[0]
            if not target or re.match(r'\w+://',target):continue
            assert (path.parent/target).resolve().exists(),(path,target)
            links+=1
    RESULTS['static']={'preserved_original_files':len(INVENTORY['files']),'moved_files':len(INVENTORY['moves']),'asset_and_page_references':count,'python_syntax_files':len(scripts),'local_document_links':links,'source_equivalence':'Only required HTML/CSS paths differ; JS, images, snapshots, README and VS Code settings exact'}
    print('PASS static:',RESULTS['static'],flush=True)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
        prefix='/before/Yolo_house/' if self.path.startswith('/before/Yolo_house/') else '/Yolo_house/'
        if not self.path.startswith(prefix):self.send_error(404);return
        rel=unquote(urlsplit(self.path).path[len(prefix):]) or 'index.html'
        if prefix.startswith('/before/') and rel in INVENTORY['source']:
            raw=INVENTORY['source'][rel].encode('utf-8')
            self.send_response(200);self.send_header('Content-Type',self.guess_type(rel));self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw);return
        if prefix.startswith('/before/'):rel=INVENTORY['moves'].get(rel,rel)
        self.path='/'+rel
        try:super().do_GET()
        except (ConnectionResetError,BrokenPipeError):pass
    def log_message(self,*args):pass

def browser_checks():
    from playwright.sync_api import sync_playwright
    from PIL import Image,ImageChops
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}/Yolo_house/'
    before=base.replace('/Yolo_house/','/before/Yolo_house/')
    captures=ROOT/'.preview/refactor-browser';captures.mkdir(parents=True,exist_ok=True)
    def ready(page):
        page.evaluate('document.fonts.ready')
        assert page.evaluate("""()=>['Bebas Neue','Poppins'].every(f=>[...document.fonts].some(t=>t.family.replaceAll('"','')===f&&t.status==='loaded'))""")
        page.wait_for_function('!document.querySelector(".preloader")||getComputedStyle(document.querySelector(".preloader")).visibility==="hidden"')
        page.locator('img[src]').evaluate_all("es=>es.forEach(e=>e.loading='eager')")
        page.wait_for_function('[...document.querySelectorAll("img[src]")].every(e=>e.complete&&e.naturalWidth>0)')
        page.evaluate('''async()=>{
            const urls=new Set([...document.querySelectorAll('*')].flatMap(e=>[...getComputedStyle(e).backgroundImage.matchAll(/url\\(["']?(.*?)["']?\\)/g)].map(m=>m[1])));
            await Promise.all([...urls].map(async src=>{const image=new Image();image.src=src;await image.decode();}));
            await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
        }''')
    def layout(page):
        return page.evaluate('()=>({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,items:[...document.querySelectorAll("header,section,footer,h1,h2,h3,img[src]")].map(e=>{const c=getComputedStyle(e);return [e.tagName,e.id,e.offsetLeft,e.offsetTop,e.offsetWidth,e.offsetHeight,c.fontFamily,c.fontSize,c.color,c.display];})})')
    def change_page(page,target,width):
        if width<=992:page.locator('.menu-toggle').click()
        with page.expect_navigation(wait_until='load'):page.locator(f'header nav a[href="{target}"]').click()
        assert page.url==base+target;ready(page)
    def viewer(page,width,ctx):
        trigger=page.locator('.project-trigger').first;trigger.click()
        page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"')
        assert page.locator('[data-viewer-image]').evaluate('e=>e.complete&&e.naturalWidth>0&&e.src.includes("/Yolo_house/assets/images/work1.jpg")')
        assert page.locator('.viewer-background-layer.is-visible').evaluate('e=>getComputedStyle(e).backgroundImage.includes("/Yolo_house/assets/images/work1.jpg")')
        assert page.locator('.viewer-background-layer').first.evaluate('e=>getComputedStyle(e).filter.includes("blur")')
        for i in range(1,6):
            page.keyboard.press('ArrowRight');page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"')
            assert page.locator('[data-viewer-image]').evaluate('e=>e.complete&&e.naturalWidth>0')
            assert str(i+1) in page.locator('.viewer-counter').inner_text()
        page.keyboard.press('ArrowLeft');page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"')
        if width<=768:
            cdp=ctx.new_cdp_session(page);b=page.locator('.viewer-stage').bounding_box();x=b['x']+b['width']*.75;y=b['y']+b['height']*.5
            c=page.locator('.viewer-counter').inner_text()
            for kind,px in [('touchStart',x),('touchMove',x-100),('touchEnd',x-100)]:cdp.send('Input.dispatchTouchEvent',{'type':kind,'touchPoints':[] if kind=='touchEnd' else [{'x':px,'y':y}]})
            page.wait_for_function('document.querySelector("#project-lightbox").dataset.state==="ready"')
            assert page.locator('.viewer-counter').inner_text()!=c
        page.keyboard.press('Escape');assert page.locator('#project-lightbox').is_hidden();assert trigger.evaluate('e=>document.activeElement===e')
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
        for width,height in SIZES:
            ctx=browser.new_context(viewport={'width':width,'height':height},is_mobile=width<=768,has_touch=width<=768,reduced_motion='reduce',timezone_id='Asia/Kolkata')
            original=ctx.new_page();page=ctx.new_page();errors=[];bad=[]
            page.set_default_navigation_timeout(60000);original.set_default_navigation_timeout(60000)
            for view in [page,original]:
                view.on('pageerror',lambda e:errors.append(str(e)))
                view.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
                view.on('response',lambda r:bad.append(r.url) if r.url.startswith(f'http://127.0.0.1:{server.server_port}/') and r.status>=400 else None)
            diffs=[]
            for name in PAGES:
                original.goto(before+name);ready(original)
                page.goto(base+name);ready(page)
                assert layout(page)==layout(original),f'Layout changed at {width}px on {name}'
                a=original.screenshot(animations='disabled');b=page.screenshot(animations='disabled')
                diff=ImageChops.difference(Image.open(io.BytesIO(a)).convert('RGB'),Image.open(io.BytesIO(b)).convert('RGB'))
                maximum=max(high for low,high in diff.getextrema())
                maximum_band=ImageChops.lighter(ImageChops.lighter(diff.getchannel('R'),diff.getchannel('G')),diff.getchannel('B'))
                histogram=maximum_band.histogram();pixels=maximum_band.width*maximum_band.height
                mean=sum(level*count for level,count in enumerate(histogram))/pixels
                edge_fraction=sum(histogram[4:])/pixels
                # Source and geometry equality are strict. Image-edge rounding varies
                # between captures; record its maximum and area, gate the average.
                visual_match=mean<=.25
                if not visual_match:
                    (captures/f'{Path(name).stem}-{width}-before.png').write_bytes(a)
                    (captures/f'{Path(name).stem}-{width}-after.png').write_bytes(b)
                    print('Pixel diagnostic:',name,width,diff.getbbox(),flush=True)
                assert visual_match,f'Viewport changed at {width}px on {name}: max {maximum}, mean {mean}, edge fraction {edge_fraction}'
                diffs.append({'page':name,'geometry':'identical','viewport_pixels':'identical' if maximum==0 else 'within documented raster tolerance','max_channel_difference':maximum,'mean_max_channel_difference':mean,'fraction_above_3':edge_fraction})
                if width in [1440,375]:(captures/f'{Path(name).stem}-{width}-before.png').write_bytes(a);(captures/f'{Path(name).stem}-{width}-after.png').write_bytes(b)
                assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
                assert page.locator('header a[aria-current="page"]').get_attribute('href')==name
                if name=='index.html':
                    summaries=page.locator('[data-approach-step] summary')
                    for i in range(summaries.count()):
                        step=page.locator('[data-approach-step]').nth(i);opened=step.get_attribute('open') is not None
                        summaries.nth(i).click();assert (step.get_attribute('open') is not None)!=opened
                        if opened:summaries.nth(i).click();assert step.get_attribute('open') is not None
                    assert page.locator('[data-service-showcase]').count()==6
                    viewer(page,width,ctx)
                elif name=='about.html':
                    page.locator('.about-story').scroll_into_view_if_needed();assert page.locator('.about-story').evaluate('e=>e.classList.contains("show")')
                    page.locator('[data-purpose-select="1"]').click();assert page.locator('#purpose-panel-1').evaluate('e=>e.classList.contains("is-active")')
                    for i in range(4):page.locator(f'#strength-tab-{i}').click();assert page.locator(f'#strength-panel-{i}').is_visible()
                    assert page.locator('.company-stats dd').count()==0
                elif name=='services.html':
                    for i in range(6):page.locator(f'#service-tab-{i}').click();assert page.locator(f'#service-tab-{i}').get_attribute('aria-selected')=='true'
                    for i in range(5):page.locator(f'#workflow-tab-{i}').click();assert page.locator(f'#workflow-tab-{i}').get_attribute('aria-selected')=='true';assert page.locator('#service-tab-5').get_attribute('aria-selected')=='true'
                elif name=='portfolio.html':
                    for i in range(page.locator('.filter-btn').count()):
                        original.locator('.filter-btn').nth(i).click();page.locator('.filter-btn').nth(i).click()
                        get_state='es=>es.map(e=>e.className)'
                        assert page.locator('.filter-btn').evaluate_all(get_state)==original.locator('.filter-btn').evaluate_all(get_state)
                        if i>0 and page.locator('.filter-btn').nth(i).get_attribute('class')=='filter-btn':
                            limitation='Existing Portfolio filter buttons have no filtering handler; original behavior preserved.'
                            if limitation not in RESULTS['preexisting_limitations']:RESULTS['preexisting_limitations'].append(limitation)
                elif name=='contact.html':
                    page.locator('#review-enquiry').click();assert page.locator('#enquiry-errors').is_visible()
                    page.locator('#enquiry-name').fill('Local refactor check');page.locator('#enquiry-email').fill('test@example.com');page.locator('#enquiry-service').select_option(label='Brand Films');page.locator('#enquiry-details').fill('Local browser validation of the existing enquiry review. No message should be sent.')
                    page.locator('#review-enquiry').click();assert 'NOT SENT' in page.locator('#enquiry-brief').input_value()
                page.evaluate('scrollTo(0,document.documentElement.scrollHeight)')
                page.wait_for_function('document.querySelector("#topBtn").classList.contains("show")')
                if width<=992:
                    toggle=page.locator('.menu-toggle');assert toggle.is_visible()
                    assert toggle.evaluate('e=>{let r=e.getBoundingClientRect();return document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)?.closest(".menu-toggle")===e;}')
                    y=page.evaluate('scrollY');toggle.click();assert toggle.get_attribute('aria-expanded')=='true';assert page.locator('body').evaluate('e=>e.classList.contains("menu-open")')
                    assert page.locator('header nav').evaluate('e=>getComputedStyle(e).filter==="none"')
                    page.keyboard.press('Escape');assert toggle.get_attribute('aria-expanded')=='false';assert abs(page.evaluate('scrollY')-y)<2
                    toggle.click();toggle.click();assert toggle.get_attribute('aria-expanded')=='false'
                page.locator('#topBtn').click();page.wait_for_function('scrollY<2')
                with page.expect_navigation(wait_until='load'):page.locator('header .logo').click()
                assert page.url==base+'index.html';ready(page)
            # Explicit page-to-page chain exercises every header destination.
            for name in PAGES:change_page(page,name,width)
            # Existing Home/About CTA and footer links: real navigation, desktop and mobile.
            if width in [1440,375]:
                for owner in ['index.html','about.html']:
                    page.goto(base+owner);ready(page)
                    selectors=['.project-cta-primary','.project-cta-secondary']
                    selectors+=['.home-footer a[href="'+n+'"]' for n in PAGES]
                    for selector in selectors:
                        link=page.locator(selector).first;href=link.get_attribute('href')
                        with page.expect_navigation(wait_until='load'):link.click()
                        assert page.url==base+href;page.goto(base+owner);ready(page)
                page.goto(base+'services.html');ready(page)
                for selector in ['.equipment a','.services-cta a']:
                    with page.expect_navigation(wait_until='load'):page.locator(selector).click()
                    assert page.url==base+'contact.html';page.goto(base+'services.html');ready(page)
            assert not errors and not bad,(errors,bad)
            RESULTS['browser'].append({'width':width,'height':height,'comparison':diffs,'functional':'navigation/logo/menu, all page interactions, viewer/background/keys/swipe, back-to-top; CTA/footer checks at 1440/375','errors':errors,'failed_local_requests':bad})
            (ROOT/'docs/testing/REFACTOR_RESULTS.json').write_text(json.dumps(RESULTS,indent=2),encoding='utf-8')
            ctx.close();print(f'PASS {width}px: five original page layouts and visual comparisons, assets, navigation and feature regressions',flush=True)
        # Normal-motion smoke checks supplement reduced-motion visual comparisons.
        for width in [1440,375]:
            ctx=browser.new_context(viewport={'width':width,'height':900},is_mobile=width==375,has_touch=width==375)
            page=ctx.new_page();page.goto(base+'services.html');ready(page)
            page.locator('#service-tab-3').click();assert page.locator('#documentaries path').evaluate('e=>getComputedStyle(e).animationName==="service-scene-draw"')
            page.locator('#workflow-tab-3').click();assert page.locator('#workflow-post-production path').evaluate('e=>getComputedStyle(e).animationName==="workflow-line-reveal"')
            ctx.close()
        RESULTS['normal_motion_smoke']=[1440,375]
        browser.close()
    server.shutdown()

if __name__=='__main__':
    static_checks()
    if '--static' not in sys.argv:
        browser_checks()
        (ROOT/'docs/testing/REFACTOR_RESULTS.json').write_text(json.dumps(RESULTS,indent=2),encoding='utf-8')
        print('Saved docs/testing/REFACTOR_RESULTS.json',flush=True)
