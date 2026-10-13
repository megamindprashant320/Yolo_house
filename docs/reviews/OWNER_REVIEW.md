# YOLO HOUSE — owner review before publication

These changes are local. No business facts have been independently verified.
Existing copy is retained where requested; no new clients, testimonials,
achievements or equipment specifications were added.

## Claims and figures to confirm

- About: 18+ years, 100+ completed projects, 50+ happy clients, 15+ creative
  professionals remain unverified. Step 4 removed these figures from the public
  About section; they are archived in CREDIBILITY_REVIEW.md for owner review.
- Home's hero retains 18+ years, 100+ projects and 50+ clients. These figures still
  require verification; the hero layout was explicitly excluded from changes.
  The duplicate About-preview figures have been removed. The new homepage
  creative-approach presentation contains no business metrics or animated counts.
- About's existing "Why Brands Trust YOLO House" heading, professional
  production, fast delivery and complete client satisfaction statements need
  evidence or owner-approved wording before publication. Mission and Vision
  remain statements of purpose and aspiration.
- Services: confirm availability of every advertised service, including aerial
  filming, VFX, motion graphics and sound design. Aerial feasibility is explicitly
  subject to confirmation. There is no promise of a particular specification.
- Existing toolkit: Sony cinema cameras, Canon DSLR/mirrorless, DJI drone
  systems, professional gimbals, studio lighting setup, Adobe Creative Cloud.
  Confirm ownership versus rental/partner access and project availability. The
  page groups this list for planning and marks its status visibly.
- Portfolio's existing client list and project captions were outside this
  redesign and have not been verified or changed.

## Contact details withheld from the public page

| Original content | Required owner confirmation |
| --- | --- |
| "Add Your Office Address Here" | Real office address and permission to publish it |
| "+91 XXXXX XXXXX" / `tel:+91XXXXXXXXXX` | Working business telephone number |
| `hello@yolohouse.com` | Ownership and monitored inbox; not assumed genuine |
| Monday–Saturday, 10:00 AM–7:00 PM | Actual operating hours and timezone |
| Generic New Delhi map | Actual office coordinates; no map is displayed now |
| Instagram `@yolohouse`, YouTube/Facebook/LinkedIn names with `href="#"` | Verified profile URLs |

The public page marks contact channels as awaiting confirmation. No placeholder
telephone, email, social profile or map is presented as a usable contact action.

## Form audit and setup

The old form had no action, delivery handler, field names or persistent labels.
A submit would reload the page; it could not deliver a message on GitHub Pages.

The new form prepares and validates a brief locally. Its action is labelled
"Review enquiry", not "Send". Completing the review only makes the brief ready
to copy. It does not send a request, save data to browser storage, or claim
delivery. Without JavaScript, the review button stays disabled and a visible
notice explains that local review needs JavaScript.

One optional free handler is Formspree. Its official [HTML setup guide](https://formspree.io/html/)
and [plans](https://formspree.io/plans/) describe an account-based form endpoint.
Before integration:

1. Confirm the receiving business inbox and choose a handler. Review its free
   quota, spam controls, data handling and privacy terms.
2. The owner creates a free account and a form, configures the verified recipient,
   and supplies the public endpoint (`https://formspree.io/f/FORM_ID`). There is
   no endpoint or account configured in this project.
3. Add the endpoint to a normal `method="post"` form and replace local review
   with actual submission handling. Do not put account credentials in site code.
4. Test a real submission with owner permission, rejection/network failure,
   duplicate clicks, spam controls and mobile behavior. Only a confirmed server
   response may show a delivery success state.
5. Update the public availability notice and any privacy text before enabling
   "Send enquiry". Confirm the owner can actually receive and answer messages.

No form service was integrated, account created, or test message sent.
