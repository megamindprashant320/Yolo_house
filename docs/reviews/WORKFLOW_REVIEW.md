# Services Step 2 — interactive production workflow

Completed locally on 13 October 2026. Only the Our Process section and its associated styles/JavaScript changed. No commit, push, deployment or next Services stage was performed.

## Original structure and content

The existing workflow was a static `ol.production-timeline` with five items. It used five columns on desktop and switched to a vertical layout below 1100px, with another internal layout rule below 576px. There was no workflow-specific JavaScript, selection state or stage-specific graphic.

The actual stages, order and descriptions below remain unchanged. The `process-title` heading and introductory copy also remain exact.

| Stage | Preserved explanation | New symbolic graphic |
| --- | --- | --- |
| 01 — Discovery | We understand your vision, objectives, audience, and project requirements. | Connected idea and story frames |
| 02 — Planning | Scriptwriting, storyboarding, scheduling, and production planning. | Planning grid and connected sequence |
| 03 — Production | Professional filming using cinematic cameras, lighting, and audio equipment. | Composition grid and viewfinder |
| 04 — Post Production | Editing, color grading, VFX, motion graphics, and sound design. | Editing tracks, playhead and waveform |
| 05 — Final Delivery | High-quality content optimized for television, cinema, web, and social media. | Finished frame and confirmation mark |

No services, deadlines, guarantees, equipment specifications, credentials or achievements were added.

## Layout and interaction

At 1440px and 1024px, numbered markers form a horizontal connected timeline above a split text/graphic panel. Below 900px, the timeline becomes a vertical stepper beside the panel; below 600px the panel follows the stepper in a single column. The existing black/charcoal/gold palette and Bebas Neue/Poppins typography are retained.

Clicking or tapping a stage selects its marker, shows the original explanation and changes its SVG composition. The connector uses `selectedIndex / (stageCount - 1)` and runs between the first and last marker centers. It represents selection through the described process. It is decorative, has no progress-bar semantics, and makes no assertion about a live client project.

The first stage is selected initially. Users can freely select earlier or later stages; there is no autoplay. Panels share the tallest content's grid space to avoid layout shifts. Connector motion, marker changes, content fades and line reveals are finite and driven by selection. There are no new animation loops, scroll listeners, assets or dependencies.

## Files changed

- `services.html`: replaced only the static workflow list with native stage controls and five panels. Existing Services Showcase, banner, header, toolkit, final CTA and footer markup remain exact.
- `style.css`: removed obsolete `.production-timeline` and `.timeline-number` rules and their responsive fragments, leaving adjacent toolkit rules intact. Added `.work-process`-scoped control, connector, panel, SVG, responsive, focus and reduced-motion rules. The existing workflow background/borders and Services preloader fallback remain unchanged.
- `main.js`: appended guarded `initProductionWorkflow()`. It derives the stage count from matching controls/panels, sets selection and normalized connector state, handles orientation-specific keyboard controls and responds to the 900px breakpoint. Previous JavaScript remains unchanged.

Local review additions: `check_workflow.py`, this report, `.preview/workflow-baseline.json`, and desktop/mobile component and viewport screenshots. Component screenshots temporarily hide fixed navigation/cursor/back-to-top/progress controls during capture; viewport screenshots show the normal page.

## Accessibility and fallback

Native buttons are enhanced into a labelled tablist with correctly associated tabpanels. Exactly one tab is selected and in the normal tab order. Left/Right keys operate horizontally, Up/Down vertically, with Home/End and wrap-around. Handled Home events stop before the site's global Home shortcut. Tab reaches the active panel and then the existing toolkit Contact link, skipping inert, hidden panels.

Focus outlines are visible. Decorative SVGs and connectors are hidden from assistive technologies. Reduced motion removes connector/panel/marker transitions, line animations and marker scaling. Without JavaScript or component initialization, controls stay hidden and all five explanations remain visible in order. Long headings wrap safely when web fonts are unavailable.

## Tests actually performed

The complete final suite ran in headless Google Chrome using the installed Playwright package, through a local server under `/Yolo_house/`. Normal viewport tests verified that the existing Bebas Neue and Poppins web fonts loaded.

| Viewport | Result |
| --- | --- |
| 1440 × 900 | Passed |
| 1024 × 768 | Passed |
| 768 × 1024 | Passed with touch emulation |
| 430 × 932 | Passed with touch emulation |
| 390 × 844 | Passed with touch emulation |
| 375 × 667 | Passed with touch emulation |

Every stage was clicked/tapped at each width. Assertions checked exact titles/descriptions/numbers, one selected tab, panel relationships and hidden states, five distinct SVG paths, marker color, connector endpoints/fill length, glyph and element bounds, copy/graphic separation, touch-target size, keyboard/focus behavior and no horizontal overflow. Section height and toolkit offset stayed constant during selection. Resizing retained the selected stage and updated orientation and connector geometry.

An early resize assertion measured a connector mismatch. The isolated 1024px rerun passed; the test was revised to await the actual CSS transition completion before measuring. No production layout override was introduced. The complete final suite then passed.

Workflow selection retained the selected Services Showcase service, and all six Showcase selections retained the workflow state. Repeating workflow initialization twice preserved the current stage and one click listener on each stage button. Changing reduced motion during desktop interaction removed animation and connector transition.

At all six widths, existing toolkit and final CTA links reached `contact.html`. Header navigation to About and logo navigation to Home passed. At touch widths, hamburger opening, Escape/button closing and scroll restoration passed. Existing About story reveal, Mission/Vision and Why Choose Us interactions passed. The homepage lightbox opened, advanced with ArrowRight, closed with Escape and restored trigger focus.

Additional contexts passed with JavaScript disabled, `main.js` blocked, and only the prior script served so the workflow remained uninitialized. All explanations remained readable. Reduced-motion checks passed at 375px and 1440px for all five stages. These isolated cases also blocked the remote font stylesheet to check fallback typography independently of external font availability.

Normal sessions recorded no page JavaScript errors, console errors or failed local page/asset responses. Fault tests deliberately produce blocked-resource diagnostics. The local server handles Chrome's unrelated origin favicon probe separately.

Source comparisons confirmed that everything outside the workflow in Services HTML, previous JavaScript, all other HTML pages and all image hashes was preserved. A separate static review checked CSS scope and neighboring toolkit rules. `node --check main.js` and `git diff --check` passed. Desktop/mobile screenshots were visually inspected.

Reproduce with `python scripts/check_workflow.py`. Use `--width 1024` for an isolated viewport plus fallback checks, or `--fallback-only` for the isolated fallback/motion cases. Existing Chrome and Playwright are required; no new package was installed.

## Owner confirmation and manual checks

Original filming, editing/VFX/motion graphics/sound design, and delivery-format capabilities remain unverified and require owner confirmation. The graphics are symbolic and do not claim equipment ownership. Existing toolkit ownership/access/availability notes were preserved; see `OWNER_REVIEW.md`.

Physical phones, Safari, Firefox, screen readers, live GitHub Pages hosting and mid-range device performance profiling were not tested. Touch tests are Chrome emulation. No actual enquiry was sent; existing Contact links were tested for navigation only. Review these environments and confirm the retained business copy before publication. Further Services changes await approval.
