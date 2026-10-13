# Step 5 — Homepage performance, SEO and accessibility review

All changes are local. No commit, push or deployment was performed. This is a targeted optimization of the approved homepage, not a redesign.

## Audit findings

- Initial Chrome loads requested all six work images through the eager gallery, even though service images were marked lazy. Total same-origin resource transfers were approximately 11.16 MB.
- The image-reveal observer changed visibility; it did not perform lazy fetching. Most images lacked intrinsic dimensions. About's alt text was generic, gallery images had empty alternatives, and some service alternatives did not describe their actual assets.
- Google Fonts were requested both through HTML and a render-blocking CSS import, using different URL/weight combinations. All five pages already had HTML font links. Poppins weights 300–600 are used in the design; 700 is retained for bold text on shared pages. Existing display=swap behavior is retained.
- The homepage lacked a main landmark, skip link, meta description, canonical and social-preview metadata. Branding, decorative section labels and statistics were represented as headings.
- Two reveal systems ran simultaneously. Scroll handlers repeatedly measured elements, including a counter listener when no counter targets existed. Pointer handlers wrote styles for every event. The progress bar animated its width.
- Native dialog semantics, focus trapping, Escape, arrow navigation and restoration already existed; they were preserved. Mobile-menu background content remained keyboard-accessible if focused programmatically. Back to Top lacked a descriptive accessible name.
- No sitemap.xml or robots.txt exists in this project. No broad SEO files were added. No business schema was added because business credentials/contact details are unverified.

## Implemented changes

### index.html

- Added a descriptive title, description, canonical, Open Graph and Twitter card metadata. No fabricated credentials or social accounts.
- Verified HTTP 200 for https://megamindprashant320.github.io/Yolo_house/ and its existing images/hero.jpg before using them in metadata.
- Preloaded the existing CSS hero background with high priority; it is not lazy-loaded. This prioritizes the above-the-fold image without assuming it is always the browser's LCP element.
- Added gstatic preconnect; aligned the homepage font weights with the existing shared-page configuration.
- Added a main landmark and keyboard skip link. Kept one H1; represented the logo, section eyebrows and numeric statistics as styled text rather than misleading headings. Copy and values are unchanged.
- Added width/height, async decoding and native lazy loading to content images. Kept all existing image URLs and files. Updated alt text after inspecting the actual local images; the viewer inherits descriptive project alternatives.

### style.css

- Removed the duplicated Google Fonts import. All other HTML pages already request these fonts and weights; their files were not modified.
- Extended existing logo/statistic/eyebrow rules to the new semantic elements, preserving their appearance.
- Added homepage-only skip/focus styles, intrinsic About-image sizing and no-JavaScript visibility fallback. Keyboard focus reveals content without waiting for scrolling.
- Homepage progress now uses scaleX instead of changing layout width. Existing cinematic blur, shadows, cards and layout remain intact; unrelated legacy rules were not removed without evidence of safety.

### main.js

- Combined progress and Back to Top updates into a passive, requestAnimationFrame-based scroll update; added a Back to Top accessible name and marked decorative elements appropriately.
- Homepage reuses the existing IntersectionObserver for reveal and unobserves revealed elements instead of running a second scroll-based scan. Other pages retain their established reveal behavior.
- Register counter scrolling only when targets exist. No counters were added to unverified figures.
- Throttled cursor/hero pointer writes to animation frames; skip pointer effects for touch/reduced motion, and stop updating an offscreen hero. Hero scroll parallax is scheduled per frame.
- Made image reveal transitions explicitly target opacity/transform; reduced motion shows images immediately, including after preference changes.
- While the homepage drawer is open, main content, footer, skip link and Back to Top are inert. Closing restores availability and existing focus/scroll behavior.
- Lightbox implementation and visuals were preserved.

## Local lab measurements

Installed headless Chrome, fresh browser contexts, localhost under /Yolo_house/, desktop 1440×900 and emulated mobile 390×844. Each snapshot waits for page load, document.fonts.ready and five additional seconds without scrolling. No network/CPU throttling. One before and one after sample per mode; timing varies with machine load and external font delivery. Resource transfer figures exclude cross-origin resources that do not expose timing sizes.

| Measurement | Desktop before | Desktop after | Mobile before | Mobile after |
| --- | ---: | ---: | ---: | ---: |
| LCP | 1.240 s | 0.808 s | 0.504 s | 0.452 s |
| FCP | 1.240 s | 0.808 s | 0.504 s | 0.452 s |
| CLS, initial observation window | 0.0663 | 0.0663 | 0 | 0 |
| Same-origin resource transfer | 11.164 MB | 1.468 MB | 11.164 MB | 1.467 MB |
| Image URLs fetched initially | 8 | 2 | 8 | 2 |
| Total long-task duration in window | 127 ms | 73 ms | 53 ms | 61 ms |

Initial transfer fell approximately 87%. Full-resolution work images are still downloaded when reached; this change defers their cost rather than shrinking files. CLS did not improve in these samples. Long-task durations are not INP measurements.

Lighthouse was not run: no Lighthouse CLI was available in the workspace/PATH. No Lighthouse scores, field Core Web Vitals or INP values were measured. The requested score and timing targets cannot be guaranteed from these local snapshots.

Raw measurement files: .preview/optimization-before-metrics.json and .preview/optimization-after-metrics.json. Reproduction: scripts/preview/measure_home.py before|after (requires the corresponding source version and existing test dependencies).

## Tests actually performed

- Chrome at 1440, 1024, 768, 430, 390 and 375px. Compared section width/height against saved pre-change HTML/CSS/JS: hero, heading, statistics, About, services, portfolio, CTA and footer remained identical.
- Bounds checks for text/link content and no horizontal document overflow across sections. Additional hero text bounds and footer/Back to Top separation at 1440 and 390px.
- Native image loading/decoding/dimensions checked. Delayed image responses at 1440 and 390px did not change About section height. Actual Bebas Neue and Poppins loading checked in the additional runs.
- Keyboard Tab reaches the skip link first; Enter focuses main. Header logo, hero actions, CTA actions, footer logo and all footer navigation destinations were actually clicked beneath /Yolo_house/.
- Trust disclosure selection and live stage feedback; service hover zoom at desktop and visible descriptions after mobile tap.
- Gallery opens via keyboard Enter. Focus enters Close; Shift+Tab/Tab wraps inside the native modal; background remains excluded by native modal behavior. ArrowRight changes the selected image and its alt text; a separate 390px run verified ArrowLeft/ArrowRight wrapping from 1 to 6 and back; blurred image background remains active. Escape closes and restores the originating trigger's focus. Actual CDP-emulated touch swipes tested at 768, 430, 390 and 375px.
- Mobile menu expansion, background inert state, sharp drawer links, Tab wrapping, Escape and restoration checked. A separate 390px run also verified backdrop dismissal and actual drawer-link navigation to Contact. Back to Top clicked and confirmed scroll position returns to zero.
- Separate no-JavaScript and reduced-motion checks at 390px confirm visible sections; reduced motion exposes all content images immediately.
- About, Services, Portfolio and Contact smoke checks at 1440/390px: no page errors, visible branding, working mobile drawer, and Contact form initialization. This did not test every interaction on those pages.
- Exact hashes confirm all four other HTML pages and every image unchanged. Main JavaScript syntax and git diff whitespace checks passed.
- Contrast spot checks: gold on charcoal 9.36:1; CTA paragraph 10.82:1; footer paragraph 10.00:1; primary button 8.98:1. These do not constitute a full WCAG conformance audit.
- No JavaScript page errors or failed local asset responses in completed homepage regression runs.

Harness corrections were needed for baseline request handling, an asynchronous disclosure toggle assertion, and the preservation assumption that other page font links had changed. Corrected/rerun checks passed; these were test harness issues rather than production defects.

## Remaining priorities and owner input

1. High: work images remain 710–2322 KiB at 2011–4160px square; hero is 776 KiB at 4099×2302px, About is 555 KiB. No image files were created, downloaded, compressed or replaced under this stage's constraints. A later approved responsive-asset optimization would materially help slow mobile networks.
2. High: run Lighthouse and throttled/physical-device testing after review; measure real interaction responsiveness and deployment behavior. No lower-powered hardware or INP testing occurred.
3. Medium: manually test Safari/Firefox, VoiceOver/NVDA, zoom/reflow, full contrast over photographic backgrounds and user preference changes. No claim of complete WCAG 2.2 AA compliance is made.
4. Medium: confirm existing hero figures (18+ years, 100+ projects, 50+ clients), business contact information and social URLs. These figures were preserved but excluded from new SEO metadata/schema. Contact delivery remains unconfigured.
5. Medium: verify the new metadata after a separately authorized deployment; the public HTTP checks validated current destinations, not publication of these local edits. Search indexing/social-cache updates are not tested.

Runtime files changed: index.html, style.css, main.js. Added local regression script check_optimization.py, review notes and .preview diagnostic artifacts. Stop here for owner review.
