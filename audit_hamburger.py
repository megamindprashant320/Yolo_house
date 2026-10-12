from pathlib import Path
import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    errors=[]
    for width in [375,390,430]:
        context=browser.new_context(viewport={'width':width,'height':844},is_mobile=True,has_touch=True,device_scale_factor=2)
        page=context.new_page()
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(Path('index.html').resolve().as_uri())
        page.evaluate('document.fonts.ready')
        for target in ['home','about','services','portfolio','contact']:
            page.evaluate('''id=>{document.documentElement.style.scrollBehavior='auto';document.getElementById(id).scrollIntoView()}''',target)
            page.wait_for_timeout(450)
            result=page.evaluate('''() => {
                const b=document.querySelector('.menu-toggle'),h=document.querySelector('header'),r=b.getBoundingClientRect(),s=getComputedStyle(b);
                return {scroll:scrollY,classes:b.className,style:b.getAttribute('style'),display:s.display,visibility:s.visibility,opacity:s.opacity,transform:s.transform,zIndex:s.zIndex,background:getComputedStyle(h).backgroundColor,
                    clickable:b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)),
                    bars:[...b.children].map(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e); return {width:r.width,height:r.height,color:s.backgroundColor,opacity:s.opacity,visibility:s.visibility,transform:s.transform,inView:r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight,hit:e===document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)};})};
            }''')
            assert result['clickable'] and result['display']=='block' and result['visibility']=='visible' and result['opacity']=='1',result
            assert all(b['width']>0 and b['height']==3 and b['color']=='rgb(255, 255, 255)' and b['opacity']=='1' and b['inView'] and b['hit'] for b in result['bars']),result
            page.locator('.menu-toggle').tap()
            page.wait_for_timeout(850)
            assert page.locator('nav').evaluate("e=>e.classList.contains('active')")
            assert page.locator('.menu-toggle').evaluate('''e=>{const r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}''')
            page.locator('.menu-toggle').tap()
            page.wait_for_timeout(450)
            assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
            print(json.dumps({'width':width,'section':target,**result}),flush=True)
        context.close()
    assert not errors,errors
    browser.close()
    print('PASS: touch emulation, visible white bars and clickable toggle on every section at all three widths',flush=True)
