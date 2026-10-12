from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
    page = browser.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))

    def check_toggle():
        assert page.evaluate('''() => {
            const toggle = document.querySelector('.menu-toggle');
            const r = toggle.getBoundingClientRect();
            const header = document.querySelector('header').getBoundingClientRect();
            const hit = document.elementFromPoint(r.x + r.width/2, r.y + r.height/2);
            return r.width > 0 && r.height > 0 && r.top >= 0 && header.top === 0 && (hit === toggle || toggle.contains(hit));
        }'''), page.evaluate('''() => {
            const t=document.querySelector('.menu-toggle'),r=t.getBoundingClientRect();
            return {url:location.href, scroll:scrollY, rect:r.toJSON(), header:document.querySelector('header').getBoundingClientRect().toJSON(), hit:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.outerHTML, expanded:t.getAttribute('aria-expanded')};
        }''')

    def check_menu():
        before = page.evaluate('window.scrollY')
        page.locator('.menu-toggle').click()
        page.wait_for_timeout(850)
        check_toggle()
        assert page.evaluate('''() => {
            const a = document.querySelector('nav a'), r = a.getBoundingClientRect();
            return document.elementFromPoint(r.x + r.width/2, r.y + r.height/2) === a;
        }''')
        page.locator('.menu-toggle').click()
        page.wait_for_timeout(400)
        check_toggle()
        assert abs(page.evaluate('window.scrollY') - before) <= 1
        assert page.locator('.menu-toggle').get_attribute('aria-expanded') == 'false'

    for width in [375, 390, 430]:
        page.set_viewport_size({'width': width, 'height': 844})
        page.goto(Path('index.html').resolve().as_uri())
        page.evaluate('document.fonts.ready')
        for target in ['home', 'about', 'services', 'portfolio', 'contact']:
            check_toggle()
            page.locator('.menu-toggle').click()
            page.locator(f'nav a[href="#{target}"]').click()
            page.wait_for_timeout(1400)
            assert page.url.endswith('#' + target)
            check_toggle()
            assert page.locator('.menu-toggle').get_attribute('aria-expanded') == 'false'
            assert page.evaluate('''id => {
                const h = document.querySelector('#' + id + ' h1, #' + id + ' h2');
                return h.getBoundingClientRect().top >= document.querySelector('header').getBoundingClientRect().bottom;
            }''', target), f'{target} heading overlaps header'
            check_menu()
        total = page.evaluate('document.documentElement.scrollHeight - innerHeight')
        for position in range(0, int(total), 250):
            page.evaluate("y => {document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0,y)}", position)
            page.wait_for_timeout(30)
            check_toggle()
        print(f'PASS {width}px: all Home anchors, heading clearance, scrolling, and menu reopening', flush=True)
        for file in ['about.html', 'services.html', 'portfolio.html', 'contact.html']:
            page.goto(Path(file).resolve().as_uri())
            page.wait_for_timeout(900)
            check_toggle()
            check_menu()
            for position in [300, 900, 1600]:
                page.evaluate("y => {document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0,y)}", position)
                page.wait_for_timeout(400)
                check_toggle()
                check_menu()
            page.locator('.menu-toggle').click()
            page.locator('nav a').first.click()
            page.wait_for_load_state('load')
            page.evaluate('document.fonts.ready')
            page.wait_for_timeout(900)
            assert page.url.endswith('index.html')
            check_toggle()
        print(f'PASS {width}px: four standalone pages, scrolling, menu toggling and Home navigation', flush=True)
    page.set_viewport_size({'width':1440,'height':900})
    page.goto(Path('index.html').resolve().as_uri())
    assert not page.locator('.menu-toggle').is_visible()
    assert page.locator('nav a').first.is_visible()
    assert not errors, errors
    print('PASS: desktop navigation and no JavaScript runtime errors', flush=True)
    browser.close()
