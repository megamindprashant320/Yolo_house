# Featured Projects cinematic viewer

## Changes

- `index.html`: the six existing gallery tiles are semantic buttons with numbered
  accessible labels. A native modal dialog provides the preview, counter,
  optional existing title, Previous/Next, Close, and an image-error retry action.
- `style.css`: scoped trigger resets preserve the grid geometry. New dialog
  styles provide a fullscreen dark viewer, crossfading blurred backgrounds,
  contained foreground image, gold controls, safe-area spacing, and reduced
  motion behavior.
- `main.js`: one homepage-only initializer handles selection, wraparound,
  keyboard focus, backdrop/Escape closing, touch swipes, scroll restoration,
  image fitting, cancellation, error recovery, and adjacent-image preloading.
  The viewer image is excluded from the existing inline lazy-animation styles.

Only those three application files were modified. `check_lightbox.py` and the
`.preview/lightbox-*` files are verification artifacts. No dependencies, new
image assets, autoplay, continuous animation loops, commits, pushes or deployments
were added.

## Existing gallery observations

The original gallery had six image-only divs without titles, alternative text,
keyboard triggers or image-viewing click handlers. No project names or business
information were invented. The viewer displays the counter; the title stays
hidden unless a real `data-project-title` or image `title` is supplied.

The shared image observer sets inline opacity/transform values. These would
interfere with the new viewer, so its image is excluded. Existing gallery image
sizes, grid spacing, entry animation and hover behavior were preserved. The
existing interaction between the thumbnail observer's inline scale and the CSS
hover scale is unchanged.

The display size is calculated from natural image dimensions and available stage
space, capped at the original dimensions. `object-fit: contain` supplies an
additional safeguard. Only current and adjacent load metadata is retained; no
extra collection of decoded full-resolution images is stored by the controller.

## Tests actually executed

Headless Chrome through Python Playwright, with a local HTTP server under
`/Yolo_house/`. The complete matrix also passed with the existing Bebas Neue and
Poppins fonts loaded.

| Viewport | Results |
| --- | --- |
| 1440x900 | Passed mouse/keyboard, all six images, original grid/hover comparison |
| 1024x768 | Passed mouse/keyboard, all six images, original grid/hover comparison |
| 768x1024 | Passed all six images, keyboard and touch-emulated swipes |
| 430x932 | Passed all six images, keyboard and touch-emulated swipes |
| 390x844 | Passed all six images, keyboard and touch-emulated swipes |
| 375x667 | Passed all six images, keyboard and touch-emulated swipes |

Verified in the matrix:

- Selected preview and blurred background match the selected source.
- Foreground aspect ratio is preserved, image bounds fit the viewport, no
  upscaling beyond natural dimensions occurs, and controls do not overlap it.
- Button navigation, keyboard Left/Right, both wraparound directions, and rapid
  changes resolve to the latest selection. There is no autoplay.
- Close, Escape, and dark-backdrop clicks work. Clicking the image keeps it open.
- Focus enters the dialog, Tab/Shift+Tab stay within controls, and focus returns
  to the original gallery tile after closing.
- Background wheel scrolling is locked; original page scroll position restores.
- Touch swipes go both directions; vertical gestures do not change selection.
- The mobile drawer still operates after the viewer closes.
- No horizontal overflow, failed local asset responses or JavaScript runtime
  errors occur during the normal matrix.

Additional executed cases: deliberate missing-image failure and retry, continued
navigation after recovery, immediate close while loading, Enter/Space activation,
reduced-motion transitions, and resizing an open viewer to 768x540.

Preservation checks compare the existing grid's settled geometry and hover
transform with a captured pre-change baseline. Exact HTML/hash checks confirm
Home's hero, About preview, Our Services, CTA, header/footer, all four other HTML
pages, and every image file remain unchanged.

## Previews and remaining manual checks

- [Desktop viewer](.preview/lightbox-1440.png)
- [375px viewer](.preview/lightbox-375.png)

Real-device touch/pinch behavior, mobile browser toolbar resizing, Safari,
Firefox, and screen-reader announcements were not tested. Live GitHub Pages
deployment was not tested or changed. Touch tests used Chrome's emulation and
dispatched touch events, not a physical phone.
