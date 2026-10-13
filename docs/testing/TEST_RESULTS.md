# Local design verification

## Additional interactive design — Home stage

Home's six service cards now contain native HTML disclosures with service-specific
brief-planning prompts. Core copy and Services links stay visible when collapsed.
Hover/open states add image zoom and a gold accent; reduced motion disables zoom
and reveal animations. The existing 35 continuous background particles were
removed from the shared script and stylesheet.

`check_showcase.py` passed at 1440, 1024, 768, 430, 390 and 375px: click/tap,
Enter/Space, exclusive disclosure state, persistent copy/links, hover graphics,
Services navigation, mobile drawer availability and absence of overflow/runtime
errors. Separate no-JavaScript and reduced-motion checks passed. Home layout
checks at all six widths passed with the existing Google Fonts loaded. Featured
Projects markup remains identical to Git HEAD.

This stage changes `index.html`, `style.css` and `main.js`, plus test scripts and
review screenshots. About, Services and Contact's new interactions are proposed
but deliberately not implemented yet, pending the requested Home-stage review.
No real-device or Safari/Firefox testing was performed for this stage.

## Scope and state

Changed application files: `index.html`, `about.html`, `services.html`,
`contact.html`, `style.css`, `main.js`.

No image files, Portfolio page content, page banners, navbar structure, or logo
links were changed. Featured Projects markup was compared with the Git HEAD
version and is identical. Normal animations remain; reduced motion has a
separate accessible presentation. No commit, push or deployment was performed.

Retired component rules and their responsive variants were removed rather than
overridden repeatedly. Existing legacy global responsive overrides exclude the
new `.studio-section` components. No new `!important` declarations were added.

## Executed checks

| Check | Executed coverage | Result |
| --- | --- | --- |
| Responsive layout | Each redesigned page at 1440x900, 1024x768, 768x1024, 430x932, 390x844, 375x667 | Passed; no horizontal overflow or content escaping the new components |
| Intended typography | The full layout matrix with Bebas Neue and Poppins loaded from the existing Google Fonts imports | Passed |
| Homepage services | Six cards, relative Services links, actual click navigation | Passed |
| Featured Projects | Exact HTML section comparison against Git HEAD | Passed; unchanged |
| Multi-page navigation | Home → About → Services → Portfolio → Contact → Home at 1440, 1024, 375, 390, 430px, with scroll positions 0/400/1100 | Passed |
| Mobile drawer | Visible white hamburger bars, clickability, opening, toggle/Escape/backdrop closing, scroll restoration, active-page markers | Passed |
| Relative asset paths | Local server under `/Yolo_house/`, HTTP responses, image decoding, exact filename case | Passed |
| Enquiry validation | 1440, 768, 430, 390, 375px; empty fields, whitespace name, malformed email, missing service, short details, valid brief | Passed |
| Form accessibility | Persistent labels, field names, description associations, inline errors, summary/error-link focus, completion focus, Home key editing | Passed |
| Safe local review | User text rendered as text in a read-only textarea; no POST requests and no browser storage writes | Passed |
| Copy action | Simulated successful clipboard API and rejection/fallback to selecting the brief | Passed; no OS clipboard write was performed |
| No JavaScript | Disabled fields/button and explanatory notice | Passed |
| Reduced motion | Visible content, no CTA animation, zero drawer transition duration, no hero pointer movement | Passed |
| Form boundary contrast | Input border against both field and panel backgrounds; 3:1 minimum | Passed in final 375px check |
| JavaScript runtime and diff | Runtime error collection and `git diff --check` | Passed |

Browser: installed Chrome, headless, using Python Playwright. Mobile cases use
viewport/touch emulation. Tests are repeatable with `scripts/check_design.py`,
`scripts/check_navigation.py`, and `scripts/check_enquiry.py`; those scripts are development
checks, not website dependencies. Full intended-font checks need network access.

## Review previews

Browser screenshots, not new website assets:

- [Homepage services](../../.preview/home-1440.png) / [375px](../../.preview/home-375.png)
- [Mission and Vision](../../.preview/about-1440.png)
- [Why Choose Us](../../.preview/about-1440-2.png)
- [Statistics](../../.preview/about-1440-3.png)
- [Services](../../.preview/services-1440.png) / [375px](../../.preview/services-375.png)
- [Production timeline](../../.preview/services-1440-2.png)
- [Toolkit](../../.preview/services-1440-3.png)
- [Contact](../../.preview/contact-1440.png) / [375px](../../.preview/contact-375.png)

## Not tested or not enabled

- Real phones, mobile browser toolbar/keyboard resizing, Safari and Firefox.
- Screen-reader behavior; focus/ARIA checks do not constitute a screen-reader audit.
- Live GitHub Pages deployment; the project remains local.
- Real clipboard permission behavior on devices; success and failure were mocked.
- Enquiry delivery: no form service is configured, and no message was sent. The
  interface explicitly offers local brief review instead of a Send action.
- Business facts, equipment ownership/access, contacts, hours and location.
  See [owner review and optional form setup](../reviews/OWNER_REVIEW.md).
