from pathlib import Path
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
    page=browser.new_page()
    errors=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    for width,height in [(1440,900),(1024,768),(768,1024),(430,932),(390,844),(375,667)]:
        page.set_viewport_size({'width':width,'height':height})
        page.goto(Path('index.html').resolve().as_uri())
        page.evaluate('document.fonts.ready')
        page.wait_for_timeout(700)
        result=page.evaluate('''() => {
            const r=s=>document.querySelector(s).getBoundingClientRect();
            const header=r('header'), hero=r('.hero'), content=r('.hero-content'), heading=r('.hero h1'), desc=r('.hero-description'), stats=r('.hero-stats'), indicator=r('.scroll-down');
            const buttons=[...document.querySelectorAll('.buttons a')].map(e=>e.getBoundingClientRect());
            return {width:innerWidth, heroHeight:hero.height, headerBottom:header.bottom, headingTop:heading.top, statsBottom:stats.bottom,
                clearHeader:content.top>=header.bottom+24, contained:heading.top>=hero.top && desc.top>=hero.top && stats.bottom<=hero.bottom,
                indicatorClear:stats.bottom+20<=indicator.top, overflow:document.documentElement.scrollWidth>innerWidth,
                stacked:innerWidth>768 || buttons[1].top>=buttons[0].bottom+10,
                fonts:document.fonts.check('16px "Bebas Neue"') && document.fonts.check('16px Poppins')};
        }''')
        assert result['clearHeader'] and result['contained'] and result['indicatorClear'] and result['stacked'] and not result['overflow'], result
        if width<=992:
            page.locator('.menu-toggle').click()
            page.wait_for_timeout(900)
            menu=page.evaluate('''() => {
                const nav=document.querySelector('nav'), a=nav.querySelector('a'), r=a.getBoundingClientRect(), n=nav.getBoundingClientRect();
                return {clickable:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===a,
                    fits:n.left>=0 && n.right<=innerWidth, filter:getComputedStyle(nav).filter,
                    headerBlur:getComputedStyle(document.querySelector('header')).backdropFilter,
                    locked:getComputedStyle(document.body).position==='fixed'};
            }''')
            assert menu['clickable'] and menu['fits'] and menu['locked'] and menu['filter']=='none' and menu['headerBlur']=='none',menu
            page.mouse.wheel(0,400)
            page.wait_for_timeout(100)
            assert page.evaluate('window.scrollY')==0
            page.keyboard.press('Escape')
            assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
            page.locator('.menu-toggle').click()
            page.locator('.menu-toggle').click()
            assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
            page.locator('.menu-toggle').click()
            page.locator('.nav-overlay').click(position={'x':10,'y':300})
            assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
            page.evaluate("document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0,350)")
            page.wait_for_timeout(400)
            before=page.evaluate('window.scrollY')
            page.locator('.menu-toggle').click()
            page.keyboard.press('Escape')
            assert page.evaluate('window.scrollY')==before
            page.locator('.menu-toggle').click()
            page.evaluate("document.querySelector('nav a').addEventListener('click',e=>e.preventDefault(),{once:true})")
            page.locator('nav a').first.click()
            assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
            page.locator('.menu-toggle').click()
            page.set_viewport_size({'width':1440,'height':900})
            assert not page.evaluate("document.body.classList.contains('menu-open')")
            result['menu']=menu
        print(json.dumps(result))
    for selector,target in [('.buttons .primary-btn','portfolio.html'),('.buttons .secondary-btn','contact.html')]:
        page.goto(Path('index.html').resolve().as_uri())
        page.locator(selector).click()
        assert page.url.endswith(target)
    assert not errors,errors
    print('PASS: hero buttons navigate; no JavaScript runtime errors')
    browser.close()
