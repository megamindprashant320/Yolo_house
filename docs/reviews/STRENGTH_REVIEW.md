# About — Why Choose Us review

The original numbered feature list was readable but static. It had no selection, larger editorial presentation, progress state or feature-specific graphic. This stage changes only that component.

## Implementation

- about.html: replaced the list with four native feature-selector buttons and associated editorial panels. Preserved Creative Storytelling, Professional Production, Fast Delivery and Client First in their original order, with every original title and description unchanged.
- style.css: replaced obsolete feature-list/Why Choose Us layout rules with scoped .why-us styles. Desktop uses vertical navigation and a larger panel; mobile uses a compact two-column selector above the content. A shared grid row reserves the tallest panel's natural height, preventing shifts when switching without a fixed pixel content height.
- Graphics: storyboard frames for storytelling, a viewfinder for production, a staged directional path for delivery, and connected circles for collaboration. These explain creative relationships rather than assert capabilities or achievements. Selected graphics draw once; the gold desktop marker moves to the selected row. No automatic cycling, particle system, pointer loop or new image asset.
- main.js: added only initStrengthShowcase. Native buttons become an accessible tab interface with role/aria associations, selected state, roving tabindex, inactive-panel inert/aria-hidden state, and visible panel focus. Desktop orientation is vertical; mobile is horizontal across the compact selector. Arrow keys, Home/End and native activation work; tab keys stop propagation to avoid the existing page Home shortcut. Selection persists across breakpoints.
- Without JavaScript, controls stay hidden and all four statements are readable. Reduced motion disables indicator, panel and line animation. Initialization has an explicit guard against duplicate listeners.

Runtime files changed: about.html, style.css, main.js. Added check_strength.py, .preview baseline/screenshots, and these notes. Existing JavaScript is preserved byte-for-byte before the scoped addition.

## Claims requiring owner confirmation

Existing copy has been retained, not independently verified:
- “Why Brands Trust YOLO House” needs support or owner-approved wording.
- Professional Production: confirm equipment/capability availability and the universal cinematic-quality statement; no ownership is inferred by the new graphic.
- Fast Delivery: confirm deadlines/process and the “without compromising” claim; the graphic represents a sequence, not a turnaround guarantee.
- Client First: substantiate “complete client satisfaction” or approve less absolute wording.
- Creative Storytelling describes creative intent; the promise of an emotional connection/lasting impression still needs owner-approved marketing wording.

No awards, clients, testimonials, equipment ownership, metrics or new guarantees were invented. See also the existing OWNER_REVIEW.md.

## Actual testing

Installed headless Chrome with existing Google Fonts at 1440, 1024, 768, 430, 390 and 375px:
- All four controls clicked/tapped; exact titles/descriptions and four distinct graphic paths confirmed.
- One active/visible panel and one selected control; other panels inert and hidden.
- Section height and following statistics offset stable across selections.
- Text/SVG bounds, graphic separated from prose, no document horizontal overflow, and at least 44px control heights.
- Gold vertical marker aligned with each selected desktop row.
- Arrow wrap, Home/End, selected-control focus and Tab into the active panel with a visible outline.
- Desktop/mobile resizing retains selection and correct orientation.
- Our Story reveal/image handling and Mission/Vision selection exercised; mobile menu open/Escape close and actual logo navigation to Home checked.
- No JavaScript page errors in completed runs.

At 390px, reduced-motion selection remained readable with panel transitions and SVG animation disabled; no-JavaScript showed all four statements with controls hidden. Chrome listener inspection confirmed one click listener before and after calling initialization twice more.

Exact comparisons confirm all About markup outside Why Choose Us, the other four HTML pages and every existing image unchanged. All previous JavaScript remains intact. Syntax and whitespace checks passed. Desktop and mobile screenshots inspected.

## Remaining limits

Physical phones, Safari/Firefox, screen readers, slow hardware and live deployment were not tested. Touch checks used browser emulation. This is not a formal WCAG conformance audit. Owner confirmation of the existing marketing claims remains outstanding.

No commit, push or deployment. Stop here for owner review; no other section was redesigned.
