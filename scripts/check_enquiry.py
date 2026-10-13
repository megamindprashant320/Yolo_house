"""Exercise local form review; mock clipboard only, never send a real enquiry."""
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright

url=(Path(__file__).resolve().parent.parent/'contact.html').as_uri()
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    for width in ([375] if '--smoke' in sys.argv else [1440,768,430,390,375]):
        context=browser.new_context(viewport={'width':width,'height':900})
        page=context.new_page();posted=[];errors=[]
        page.on('request',lambda r:posted.append(r.url) if r.method=='POST' else None)
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(url);page.wait_for_timeout(850)
        assert page.locator('#project-form fieldset input,#project-form fieldset select,#project-form fieldset textarea').evaluate_all('fields=>fields.every(field=>field.labels.length===1 && field.name && field.getAttribute("aria-describedby"))')
        assert page.locator('#enquiry-name').evaluate(r'''e=>{
            const luminance=color=>{const c=color.match(/[\d.]+/g).slice(0,3).map(Number).map(n=>n/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722;};
            const s=getComputedStyle(e), parent=getComputedStyle(document.querySelector('.enquiry-panel'));
            const border=luminance(s.borderTopColor);
            return [s.backgroundColor,parent.backgroundColor].every(bg=>(border+.05)/(luminance(bg)+.05)>=3);
        }''')
        review=page.locator('#review-enquiry')
        review.click()
        assert page.locator('[aria-invalid="true"]').count()==4
        assert page.locator('#enquiry-errors').is_visible()
        assert page.locator('#enquiry-errors').evaluate('e=>document.activeElement===e')
        page.locator('#enquiry-errors a').first.click()
        assert page.locator('#enquiry-name').evaluate('e=>document.activeElement===e')
        page.locator('#enquiry-name').fill('   ')
        page.locator('#enquiry-email').fill('bad-email')
        page.locator('#enquiry-details').fill('too short')
        review.click()
        assert page.locator('#enquiry-email-error').is_visible()
        assert page.locator('#enquiry-details-error').is_visible()
        assert page.locator('#enquiry-name-error').is_visible()
        page.locator('#enquiry-name').fill('Test Project Owner')
        page.locator('#enquiry-email').fill('owner@example.com')
        page.locator('#enquiry-service').select_option(label='Brand Films')
        page.locator('#enquiry-details').fill('<script>not executable</script> A film brief for our product launch.')
        review.click()
        assert not page.locator('#enquiry-errors').is_visible()
        assert page.locator('#enquiry-review').is_visible()
        assert 'Nothing has been sent' in page.locator('#enquiry-status').inner_text()
        assert page.locator('#enquiry-status').evaluate('e=>document.activeElement===e')
        assert page.locator('#enquiry-brief').input_value().startswith('YOLO HOUSE')
        assert '<script>' in page.locator('#enquiry-brief').input_value()
        # A successful clipboard operation is simulated to avoid writing to the OS clipboard.
        page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{window.testCopied=text}}})")
        page.locator('#copy-brief').click()
        assert page.evaluate('window.testCopied')==page.locator('#enquiry-brief').input_value()
        assert 'Brief copied' in page.locator('#copy-status').inner_text()
        page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('blocked')}}})")
        page.locator('#copy-brief').click()
        assert 'Automatic copying is unavailable' in page.locator('#copy-status').inner_text()
        assert page.locator('#enquiry-brief').evaluate('e=>e.selectionEnd-e.selectionStart===e.value.length')
        page.locator('#enquiry-details').fill('A revised brief for a product launch with more context.')
        assert not page.locator('#enquiry-review').is_visible()
        page.locator('#enquiry-details').focus()
        page.evaluate("window.originalScrollTo=window.scrollTo;window.homeScrollCalls=[];window.scrollTo=function(...args){window.homeScrollCalls.push(new Error().stack);return window.originalScrollTo.apply(window,args)};void 0")
        page.keyboard.press('Home')
        assert not page.evaluate('window.homeScrollCalls'),page.evaluate('window.homeScrollCalls')
        page.evaluate('window.scrollTo=window.originalScrollTo;void 0')
        assert page.locator('iframe,a[href^="tel:"],a[href^="mailto:"],.social-card').count()==0
        assert not posted and not errors,(posted,errors)
        assert page.evaluate('localStorage.length===0 && sessionStorage.length===0')
        print(f'PASS enquiry {width}px: validation, labels, focus, local completion, safe text, clipboard success/failure mocks; no POST or storage',flush=True)
        context.close()
    context=browser.new_context(java_script_enabled=False)
    page=context.new_page();page.goto(url)
    assert page.locator('#review-enquiry').is_disabled()
    assert page.locator('#enquiry-name').is_disabled()
    assert page.locator('noscript').is_visible()
    context.close()
    context=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
    page=context.new_page();page.goto(url);page.wait_for_timeout(850)
    assert page.evaluate("getComputedStyle(document.documentElement).scrollBehavior==='auto'")
    assert page.locator('.contact-cta').evaluate("e=>getComputedStyle(e).animationName==='none' && getComputedStyle(e).opacity==='1'")
    page.locator('.menu-toggle').click()
    assert page.locator('nav').evaluate("e=>getComputedStyle(e).transitionDuration==='0s'")
    page.keyboard.press('Escape')
    assert page.locator('.menu-toggle').get_attribute('aria-expanded')=='false'
    page.goto((Path(__file__).resolve().parent.parent/'index.html').as_uri())
    page.wait_for_timeout(850)
    page.mouse.move(30,30)
    assert page.locator('.hero-content').evaluate("e=>!e.style.transform")
    assert page.locator('.services').evaluate("e=>getComputedStyle(e).opacity==='1'")
    context.close();browser.close()
    print('PASS: no-JavaScript fail-closed mode and reduced-motion navigation/content',flush=True)
