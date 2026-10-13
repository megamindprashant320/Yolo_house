# About — Mission & Vision review

The original introduction sat beside two static statements. There was no selection, connected graphic or responsive interactive behavior. Both Mission and Vision wording and headings are preserved exactly; no business claims, metrics or images were added.

## Changes

- about.html: connected two-panel composition with native Mission/Vision buttons, restrained existing numbering and an accessible section heading. Both statements are always present in the markup.
- style.css: replaced the old purpose-copy layout and obsolete Mission/Vision breakpoint rules with scoped styles. Desktop keeps both statements readable, emphasizing the selected panel through gold typography, contrast and bounded radial lighting. Mobile uses a compact selector above a shared grid row sized by its taller panel, keeping selection height stable without fixed pixel heights. Connector lines, active underline and endpoint highlights animate subtly. Reduced motion disables transitions and illumination movement.
- main.js: scoped initPurposeExperience; desktop native toggle buttons with aria-pressed; mobile tablist/tab/tabpanel roles and associations, aria-selected, roving tabindex, inactive-panel inert/aria-hidden states. Left/Right wrap, Home/End select endpoints, Enter/Space use native button behavior. Mobile tab keys stop propagation to avoid the existing page Home-key scroll shortcut. Resize retains selection and keeps focus on the active tab when converting focused desktop controls to mobile. Active tabpanel has visible keyboard focus.
- Reused the existing IntersectionObserver for one-time connector drawing; its target guard was extended to unobserve Mission/Vision after reveal. Added no scroll listener or observer. Desktop illumination uses passive pointer handling with animation-frame writes; touch/reduced motion remain static.
- Without JS the selector stays hidden and both statements remain visible, including on mobile. The existing About noscript preloader fallback remains unchanged.

Runtime files modified: about.html, style.css, main.js. Added check_purpose.py, local .preview diagnostics and these review notes.

## Tests actually executed

Installed headless Chrome with the existing web fonts at 1440, 1024, 768, 430, 390 and 375px:

- Mission/Vision selection by actual desktop clicks and emulated touch taps; selected visual/state classes and aria state confirmed.
- Desktop both statements visible, no tab roles; mobile inactive statement hidden and inert, active panel readable.
- Section height and following Why Choose Us offset unchanged across repeated selections.
- Heading/paragraph bounds, no horizontal page overflow, visible keyboard focus and minimum 44px selector height.
- Mobile Left/Right/Home/End, roving tabindex and no unintended Home-key page scroll. Desktop native Space activation.
- Desktop pointer illumination at 1440/1024px; resize in both directions retains active state and updates semantics/visibility. Existing menu opened/closed after desktop-to-mobile resizing.
- No JavaScript page errors in completed six-width runs.

Separate checks verified initial connector scale and drawing completion, resize focus correction, keyboard Tab into the active panel with its outline, static mobile illumination, and desktop/mobile reduced-motion behavior. At 390px without JS, selector hidden, both statements visible and preloader fallback functioning.

Exact comparisons confirm unchanged Mission/Vision statements, all About markup outside this section, all other HTML pages and every image. The Our Story CSS block is unchanged byte-for-byte. Existing JS is unchanged except the narrow observer target guard; all other new logic lives in the scoped initializer. JavaScript syntax and whitespace checks passed. Desktop and mobile screenshots were visually inspected.

Early assertions needed harness corrections for keyboard focus modality and allowing automatic scrolling to settle before pointer testing. No production visibility defect was found from those failures.

## Remaining manual checks

Physical phones, Safari/Firefox, screen readers and slower hardware were not tested. Touch testing was browser emulation. No live deployment test or formal WCAG audit occurred. No known failing component test remains.

Our Story, banner, Why Choose Us, statistics, final CTA, footer, navigation and other pages were not redesigned. All changes remain local; no commit, push or deployment. Stop here for owner review.
