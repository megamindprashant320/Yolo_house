"""Check stage-one Home disclosures without changing the other page interactions."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re
import subprocess

root=Path(__file__).resolve().parent.parent
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    for width in [1440,1024,768,430,390,375]:
        touch=width<=768
        context=browser.new_context(viewport={'width':width,'height':900},is_mobile=touch,has_touch=touch)
        page=context.new_page();errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto((root/'index.html').as_uri());page.wait_for_timeout(850)
        cards=page.locator('[data-service-showcase]')
        assert cards.count()==6
        assert page.locator('.particle').count()==0
        for index,card in enumerate(cards.all()):
            summary=card.locator('summary');details=card.locator('details')
            summary.scroll_into_view_if_needed()
            assert card.locator('h3').is_visible()
            assert card.locator('.studio-card-body > p').is_visible()
            assert card.locator('a').is_visible()
            if touch:summary.tap()
            else:summary.click()
            page.wait_for_timeout(450)
            assert details.get_attribute('open') is not None
            assert card.locator('.showcase-detail p').is_visible()
            assert page.locator('.showcase-disclosure[open]').count()==1
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
            summary.focus();page.keyboard.press('Space')
            assert details.get_attribute('open') is None
            page.keyboard.press('Enter')
            assert details.get_attribute('open') is not None
        if not touch:
            cards.first.locator('summary').scroll_into_view_if_needed()
            cards.first.hover();page.wait_for_timeout(500)
            assert cards.first.locator('.showcase-frame').evaluate("e=>getComputedStyle(e).transform!=='none'")
            assert cards.first.locator('.studio-card-image').evaluate("e=>getComputedStyle(e,'::after').transform.startsWith('matrix(1,')")
        if width==375:
            page.locator('header').evaluate('e=>e.style.visibility="hidden"')
            cards.last.screenshot(path=str(root/'.preview'/'home-interactive-375.png'))
            page.locator('header').evaluate('e=>e.style.visibility=""')
        cards.first.locator('a').click();page.wait_for_load_state('load')
        assert page.url.endswith('/services.html')
        if touch:
            page.locator('.menu-toggle').tap()
            assert page.locator('nav').evaluate("e=>e.classList.contains('active')")
            page.keyboard.press('Escape')
            assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
        assert not errors,errors
        print(f'PASS {width}px: disclosures, persistent content/links, keyboard, hover/tap, no overflow or runtime errors',flush=True)
        context.close()
    for options in [{'java_script_enabled':False},{'reduced_motion':'reduce'}]:
        context=browser.new_context(viewport={'width':390,'height':844},**options)
        page=context.new_page();page.goto((root/'index.html').as_uri());page.wait_for_timeout(850)
        assert page.locator('.services').evaluate("e=>getComputedStyle(e).opacity==='1'")
        summary=page.locator('.showcase-disclosure summary').first
        summary.click()
        assert page.locator('.showcase-detail p').first.is_visible()
        if 'reduced_motion' in options:
            assert page.locator('.showcase-detail').first.evaluate("e=>getComputedStyle(e).animationName==='none'")
            assert page.locator('.showcase-frame').first.evaluate("e=>getComputedStyle(e).transform==='none' && getComputedStyle(e).transitionDuration==='0s'")
        context.close()
    browser.close()
pattern=r'<section class="portfolio".*?</section>'
before=subprocess.check_output(['git','show','HEAD:index.html'],cwd=root).decode('utf-8')
after=(root/'index.html').read_text(encoding='utf-8')
assert re.search(pattern,before,re.S)[0]==re.search(pattern,after,re.S)[0]
print('PASS: no-JavaScript and reduced-motion disclosures; Featured Projects markup unchanged',flush=True)
