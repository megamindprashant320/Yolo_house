# Services Step 1 — local review

Only the main Services Showcase was upgraded. Nothing was committed, pushed or deployed. The remaining Services sections await approval before further changes.

## Existing problems

The page had six equal service cards with the same filmstrip SVG. Titles, descriptions and Contact links were present, but there was no service selection or distinct visual storytelling. The Services-specific card rules sat alongside shared homepage card styles, so the replacement removes only the obsolete Services rules.

Existing local images were inspected and left unchanged. Abstract inline SVG compositions suit this selector without introducing photographs or implying equipment ownership.

The existing preloader depended on JavaScript to disappear. A Services-only fallback was necessary to meet the requested script-disabled/script-failure support.

## Component and content

Desktop uses a numbered vertical list, moving gold indicator and shared presentation panel. Tablet/mobile uses a two-column touch selector above the panel. Each selection shows the original title, full description and existing Contact link. All six panels share the tallest panel's layout space to prevent selection from moving the following workflow section.

| Preserved service, in original order | Preserved fragment | New symbolic composition |
| --- | --- | --- |
| Brand Films | `brand-films` | Connected storyboard frames |
| TV Commercials | `commercials` | Broadcast frame and play geometry |
| Photography | `photography` | Focus rings and framing marks |
| Documentary Films | `documentaries` | Connected interview perspectives |
| Drone Cinematography | `aerial` | Horizon, framing and flight curve |
| Post Production | `post-production` | Editing tracks and playhead |

Graphics use a brief line reveal when selected. Fine mouse pointers can move the panel's subtle illumination; touch layouts use a static background. There is no autoplay, scroll-jacking or continuous animation loop. Pointer updates use a single queued animation frame.

## Site files changed

- `services.html`: replaced the main showcase only; retained its introduction, all six descriptions, IDs and exact Contact link markup. Added a local `<noscript>` preloader fallback in the head.
- `style.css`: removed unused `.service-detail`, `.service-detail-top`, `.service-mark` and associated heading/mobile rules. Added `.services-showcase` layout, graphics, selected/focus states, responsive and reduced-motion styles. A `body:has(.services-showcase) > .preloader` rule releases static content if the script fails. Scoped heading wrapping also handles long words when web fonts are unavailable.
- `main.js`: appended guarded `initServicesShowcase()`; existing JavaScript is preserved. It handles selection, responsive tab orientation, keyboard controls, pointer illumination, media-preference changes and original service deep links.

No changes to the banner, navigation, workflow, toolkit, final CTA, footer, other HTML pages, or image assets. Source comparisons and asset hashes checked that scope.

Local review additions: `check_services_showcase.py`, this report, and `.preview/services-showcase-*` baseline/screenshots plus `.preview/services-viewport-*` screenshots. Component captures hide fixed header/cursor/back-to-top/progress controls only while capturing; viewport captures leave the page unmodified.

## Accessibility

Native buttons are progressively enhanced into tabs with labelled panels, selected states and roving tab focus. Arrow keys, Home and End select services. Mobile Up/Down moves between selector rows. Hidden panels are inert and excluded from assistive technology; Tab reaches the active panel and its Contact link. Focus outlines remain visible.

Decorative graphics are hidden from screen readers. Reduced motion disables the line reveal, panel/indicator transitions and pointer lighting. With JavaScript disabled or unavailable, the selector stays hidden and all six service articles and enquiry links remain readable. No new dependencies were added.

## Tests actually executed

Automated headless Google Chrome via the existing Playwright installation, served locally under `/Yolo_house/`. Normal responsive tests verified that Bebas Neue and Poppins loaded from the existing Google Fonts URLs.

| Viewport | Final result |
| --- | --- |
| 1440 × 900 | Passed |
| 1024 × 768 | Passed |
| 768 × 1024 | Passed, touch emulation |
| 430 × 932 | Passed, touch emulation |
| 390 × 844 | Passed, touch emulation |
| 375 × 667 | Passed, touch emulation |

At every width, all six services were selected using real mouse clicks or emulated taps. Assertions checked correct content and distinct SVG paths, selected/inert state, indicator updates, text and graphic bounds, text overflow, touch targets, keyboard wrap/Home/End, visible focus and focus order. Showcase height and the following workflow's offset stayed unchanged during selection; no horizontal overflow was detected. Resizing retained the active service.

All six Contact links were clicked at every width and reached `contact.html` under the local subpath. Desktop pointer lighting/reset and mobile static behavior passed. Reinitializing the component twice retained one click listener on the checked button. Changing the desktop motion preference while interacting disabled the lighting and graphic animation.

All six fragment URLs opened the correct panel below the fixed header. Valid, unknown and malformed hash changes were checked. Mobile drawer opening, Escape/backdrop closing, scroll restoration and navigation to About passed. Existing About story reveal, Mission/Vision and Why Choose Us selection passed. Logo navigation returned to Home; its lightbox opened, advanced using the keyboard, closed with Escape and restored trigger focus at all six widths.

Separate 390px contexts passed with JavaScript disabled, `main.js` deliberately blocked, and blocked JavaScript plus reduced motion. Reduced-motion contexts passed at 390px and 1440px. These isolated cases deliberately blocked the remote font stylesheet as well, to test fallback behavior without relying on third-party availability. That exposed a long heading overflow in the fallback font; the scoped wrapping fix passed the subsequent fallback and complete responsive runs.

Normal sessions recorded no page JavaScript errors, console errors or failed local page/asset responses. Deliberate resource blocking in fault tests produces expected network diagnostics. The local server handles Chrome's unrelated origin favicon probe separately.

JavaScript syntax (`node --check main.js`) and `git diff --check` passed. Desktop and mobile screenshots were inspected visually. Test script: `python scripts/check_services_showcase.py`; isolated fallback checks: `python scripts/check_services_showcase.py --fallback-only`; previews: `python scripts/check_services_showcase.py --preview-only`.

## Confirmation and remaining manual checks

All advertised service availability still requires owner confirmation, especially aerial filming, VFX, motion graphics and sound design. No new capabilities, equipment specifications, clients, awards, metrics or guarantees were introduced. Aerial feasibility wording remains explicitly conditional. The existing toolkit's ownership/access/availability note is unchanged; see `OWNER_REVIEW.md`.

Contact navigation was tested; actual enquiry delivery was not. Its existing form prepares a local brief and has no configured delivery handler. This stage did not change that behavior or send messages.

Physical phones, Safari, Firefox, assistive technologies and live GitHub Pages deployment were not tested. Touch results are Chrome emulation. Review those environments and the visual treatment before publication. No next Services section has been started.
