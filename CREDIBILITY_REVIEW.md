# About — Company Statistics & Credibility review

Only the About company-statistics section has changed. All work is local; no commit, push or deployment.

## Data integrity

No numerical business metric in the project has supporting owner confirmation. The following previous About figures were removed from public presentation and retained here for review:

| Previous value | Exact previous label | Status / evidence needed |
| --- | --- | --- |
| 18+ | Years of Experience | Unverified; define whose experience, start date and basis |
| 100+ | Completed Projects | Unverified; dated completed-project register and counting criteria |
| 50+ | Happy Clients | Unverified; client count plus evidence for the satisfaction wording |
| 15+ | Creative Professionals | Unverified; dated roster and definition of employee/contractor/partner |

The homepage hero still contains 18+ Years, 100+ Projects and 50+ Clients. It was explicitly excluded from this stage and remains unchanged. These homepage claims continue to need verification. No awards, testimonials, percentages, ownership claims or credentials were invented.

## Public presentation

A restrained asymmetric composition replaces the numerical display. It uses the existing studio name and creative-production description, oversized cinematic typography, a labelled Idea → Story → Final cut sequence, gold connecting lines and an actual Portfolio link. The sequence represents a creative concept, not measured business performance.

The connector draws once on viewport entrance using the existing observer, which unobserves the section after reveal. No new observer, scroll listener or background animation loop. Portfolio underline/arrow feedback provides the genuine hover/focus interaction. Text is always readable; reduced motion draws the connector immediately and disables arrow movement. No-JavaScript shows all text and the complete line.

No count-up was implemented or run because there are zero verified numerical targets. No percentage indicator, empty metric placeholder or unnecessary focusable statistic was introduced.

## Preparing verified data later

The .company-stats component and stats-title association are retained as the integration point. Before replacing the fallback with numerical content, supply each record with:

- owner-approved label and definition;
- nonnegative numeric value;
- suffix, if any, and evidence justifying a “+” threshold;
- source/evidence and an as-of date;
- explicit owner approval to publish.

Use semantic dt/dd labels and values when that data is available. Verified values should exist in HTML for no-JavaScript and screen-reader access. A later scoped, one-time counter may animate a separate aria-hidden visual value, with final values under reduced motion. Do not automatically convert these archived figures into approved targets or connect them to the legacy .stats h3 counter.

This stage establishes the safe fallback and a documented data contract; it does not claim automatic verified-data ingestion or a tested future count-up engine.

## Files

- about.html: changed only the company-statistics section.
- style.css: replaced that section's unused numerical layout rules with scoped editorial, responsive, reveal and focus styles. Shared verification-note styling retained.
- main.js: scoped credibility reveal using the existing observer; extended only its unobserve guard. Previous interactions otherwise unchanged.
- OWNER_REVIEW.md: corrected the outdated note that the About numbers still appear publicly.
- Added check_credibility.py, .preview diagnostic baseline/screenshots and this report.

## Actual tests

Installed headless Chrome at 1440, 1024, 768, 430, 390 and 375px:

- No previous business figures or counter/progress targets in this section.
- Connector reveal completes; section height and following CTA offset remain stable during animation.
- Heading, paragraph, link and sequence bounds; no document horizontal overflow.
- Visible link keyboard focus, comfortable target height; actual Portfolio navigation by desktop Enter and emulated mobile tap.
- Resizing between mobile and desktop remains free of overflow.
- Our Story reveal, Mission/Vision selection, Why Choose Us selection and mobile menu Escape behavior exercised without JavaScript page errors.
- Separate 390px reduced-motion and no-JavaScript runs confirmed visible text/link and completed connector. Reduced-motion transition is disabled.
- Exact comparison verifies About markup outside this section, other four HTML pages and all images unchanged. Previous JS preserved except the scoped observer guard. Syntax and whitespace checks passed. Desktop/mobile screenshots inspected.

Count-up triggering, numeric suffix formatting and verified-value rendering were not tested: no verified data or count-up engine exists in this stage. Chrome snapshots are not physical-device, screen-reader or formal WCAG tests.

## Remaining requirements

Owner evidence and approval are needed before publishing any numerical credibility claims. Physical phones, Safari/Firefox, screen readers, slower hardware and live GitHub Pages deployment remain untested. The homepage's unverified hero figures remain outside this change's scope.

Stop here for owner review; no other About section has been redesigned.
