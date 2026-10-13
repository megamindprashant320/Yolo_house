from pathlib import Path
import json,hashlib,re
r=Path(__file__).resolve().parent.parent.parent
b={n:(r/asset).read_text(encoding='utf-8') for n,asset in [('index.html','index.html'),('style.css','assets/css/style.css'),('main.js','assets/js/main.js')]}
b['pages']={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in ['about.html','services.html','portfolio.html','contact.html']}
b['assets']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (r/'assets/images').iterdir() if p.is_file()}
(r/'.preview/footer-baseline.json').write_text(json.dumps(b),encoding='utf-8')
f='''<footer class="home-footer" aria-labelledby="footer-brand">
    <div class="footer-wordmark" aria-hidden="true">YOLO HOUSE</div>
    <div class="footer-layout">
        <div class="footer-column footer-brand">
            <a class="footer-logo" href="index.html" id="footer-brand">YOLO HOUSE<span>PRODUCTIONS</span></a>
            <p class="footer-tagline">Because You Only Live Once,<br>Your Content Should Be Unforgettable.</p>
            <p>Creative production for films, campaigns and visual stories.</p>
        </div>
        <nav class="footer-column footer-navigation" aria-label="Footer navigation">
            <h2>EXPLORE</h2>
            <a href="index.html" aria-current="page">Home <span aria-hidden="true">?</span></a>
            <a href="about.html">About <span aria-hidden="true">?</span></a>
            <a href="services.html">Services <span aria-hidden="true">?</span></a>
            <a href="portfolio.html">Our Work <span aria-hidden="true">?</span></a>
            <a href="contact.html">Contact <span aria-hidden="true">?</span></a>
        </nav>
        <div class="footer-column footer-contact">
            <h2>THE NEXT CONVERSATION</h2>
            <p>Bring your idea, your brief or the questions that will shape your project.</p>
            <a class="footer-contact-link" href="contact.html">Visit our Contact page <span aria-hidden="true">?</span></a>
        </div>
    </div>
    <div class="footer-bottom">
        <p>© <span data-footer-year>2026</span> YOLO HOUSE Productions.</p>
        <span class="footer-separator" aria-hidden="true"></span>
        <p>All rights reserved.</p>
    </div>
</footer>'''
p=r/'index.html';p.write_text(re.sub(r'<footer>.*?</footer>',lambda _:f,b['index.html'],flags=re.S),encoding='utf-8')
css='''
/* Homepage closing scene; other page footers retain their existing treatment. */
.home-footer{position:relative;isolation:isolate;overflow:hidden;padding:80px 8% 28px;text-align:left;background:radial-gradient(ellipse at 15% 0%,#282113 0%,transparent 60%),#080808;border-top:1px solid #554529;}
.footer-wordmark{position:absolute;bottom:42px;left:8%;z-index:-1;font-family:'Bebas Neue',sans-serif;font-size:clamp(100px,20vw,280px);line-height:1;color:#ffffff03;white-space:nowrap;pointer-events:none;user-select:none;}
.footer-layout{display:grid;grid-template-columns:1.5fr .7fr 1fr;gap:clamp(32px,5vw,80px);padding-bottom:48px;}
.home-footer .footer-column{position:relative;padding-top:24px;min-width:0;}
.footer-column::before{content:"";position:absolute;top:0;left:0;width:64px;height:1px;background:#b69851;transform-origin:left;transition:transform .7s ease;}
.home-footer.footer-enhanced .footer-column:not(.show)::before{transform:scaleX(0);}
.home-footer .footer-logo{display:inline-block;font-family:'Bebas Neue',sans-serif;font-size:48px;line-height:1;color:#e9e5da;letter-spacing:1px;}
.footer-logo span{display:block;margin-top:10px;font-family:'Poppins',sans-serif;font-size:10px;letter-spacing:5px;color:#d4af37;}
.home-footer p{font-size:13px;line-height:1.9;color:#bbb7ad;margin:20px 0 0;max-width:340px;}
.home-footer .footer-tagline{color:#e0dcd2;font-size:14px;margin-top:26px;}
.home-footer h2{font-family:'Poppins',sans-serif;font-size:11px;letter-spacing:2px;line-height:1.7;color:#d4af37;margin:0 0 18px;}
.home-footer .footer-navigation{position:relative;inset:auto;width:auto;height:auto;display:block;padding:24px 0 0;overflow:visible;transform:none;visibility:visible;background:none;border:0;z-index:auto;transition:none;}
.home-footer .footer-navigation a,.footer-contact-link{position:relative;display:flex;align-items:center;justify-content:space-between;gap:18px;min-height:44px;width:fit-content;max-width:100%;font-size:14px;color:#d7d3c9;transition:color .25s;}
.home-footer a:not(.footer-logo)::after{content:"";position:absolute;left:0;bottom:6px;width:100%;height:1px;background:#d4af37;transform:scaleX(0);transform-origin:left;transition:transform .25s;}
.home-footer a:hover,.home-footer a:focus-visible{color:#e2c263;}
.home-footer a:hover::after,.home-footer a:focus-visible::after{transform:scaleX(1);}
.home-footer a span[aria-hidden]{color:#d4af37;transition:transform .25s;}
.home-footer a:hover span[aria-hidden],.home-footer a:focus-visible span[aria-hidden]{transform:translate(2px,-2px);}
.home-footer a:focus-visible{outline:2px solid #efcf75;outline-offset:5px;border-radius:2px;}
.home-footer .footer-contact-link{margin-top:20px;}
.footer-bottom{display:flex;align-items:center;gap:20px;flex-wrap:wrap;border-top:1px solid #ffffff14;padding-top:24px;}
.home-footer .footer-bottom p{margin:0;font-size:11px;color:#aaa69c;}
.footer-separator{width:24px;height:1px;background:#8a713b;}
@media(max-width:992px){.footer-layout{grid-template-columns:1fr 1fr;gap:36px;}.footer-brand{grid-column:1/-1;}.home-footer{padding:60px 6% 28px;}}
@media(max-width:576px){.footer-layout{grid-template-columns:1fr;gap:28px;padding-bottom:32px;}.footer-brand{grid-column:auto;}.home-footer{padding-top:44px;}.footer-bottom{gap:12px;}.footer-wordmark{bottom:60px;}}
@media(prefers-reduced-motion:reduce){.home-footer .footer-column::before,.home-footer a,.home-footer a::after,.home-footer a span[aria-hidden]{transition:none;}.home-footer.footer-enhanced .footer-column:not(.show)::before{transform:none;}}
'''
p=r/'assets/css/style.css';p.write_text(b['style.css']+css,encoding='utf-8')
js='''
/* Homepage footer uses the existing reveal observer; no additional scroll listener. */
const homepageFooter = document.querySelector('.home-footer');
if (homepageFooter) {
    homepageFooter.querySelector('[data-footer-year]').textContent = new Date().getFullYear();
    homepageFooter.classList.add('footer-enhanced');
    homepageFooter.querySelectorAll('.footer-column').forEach(column => {
        if (reducedMotion.matches) column.classList.add('show');
        else observer.observe(column);
        column.addEventListener('focusin', () => column.classList.add('show'));
    });
}
'''
p=r/'assets/js/main.js';p.write_text(b['main.js']+js,encoding='utf-8')

