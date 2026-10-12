/*=========================================================
    YOLO HOUSE PRODUCTIONS
    MAIN.JS
    PART - 1
=========================================================*/

"use strict";

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

/*=========================================================
    SELECTORS
=========================================================*/

const header = document.querySelector("header");
const navLinks = document.querySelectorAll("nav ul li a");

const primaryBtn = document.querySelector(".primary-btn");
const secondaryBtn = document.querySelector(".secondary-btn");

/*=========================================================
    STICKY HEADER
=========================================================*/

function updateHeader() {
    if (header) header.classList.toggle("scrolled", window.scrollY > 50);
}
window.addEventListener("scroll", updateHeader, {passive:true});
updateHeader();
if (header) new ResizeObserver(() => {
    document.documentElement.style.setProperty("--header-height", header.getBoundingClientRect().height + "px");
}).observe(header);

/*=========================================================
    RESPONSIVE NAVBAR
=========================================================*/

const menuToggle = document.querySelector(".menu-toggle");
const nav = document.querySelector("nav");
const overlay = document.querySelector(".nav-overlay");
const mobileMenu = window.matchMedia("(max-width:992px)");
let menuScrollY = 0;

function setMenu(open) {
    if (!menuToggle || !nav) return;
    open = open && mobileMenu.matches;
    const wasOpen = document.body.classList.contains("menu-open");
    if (open && !wasOpen) {
        menuScrollY = window.scrollY;
        document.body.style.top = `-${menuScrollY}px`;
    }
    menuToggle.classList.toggle("active", open);
    nav.classList.toggle("active", open);
    if (overlay) overlay.classList.toggle("active", open);
    document.body.classList.toggle("menu-open", open);
    menuToggle.setAttribute("aria-expanded", String(open));
    menuToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    nav.inert = mobileMenu.matches && !open;
    if (!open && wasOpen) {
        document.body.style.top = "";
        const root = document.documentElement;
        const previous = root.style.scrollBehavior;
        root.style.scrollBehavior = "auto";
        window.scrollTo(0, menuScrollY);
        root.style.scrollBehavior = previous;
        menuToggle.focus({preventScroll:true});
    }
}
function closeMenu() { setMenu(false); }
if (menuToggle) menuToggle.addEventListener("click", () => setMenu(!nav.classList.contains("active")));
if (overlay) overlay.addEventListener("click", closeMenu);
navLinks.forEach(link => link.addEventListener("click", closeMenu));
document.addEventListener("keydown", event => {
    if (event.key === "Escape") closeMenu();
    if (event.key === "Tab" && document.body.classList.contains("menu-open")) {
        const items = [menuToggle, ...nav.querySelectorAll("a[href]")];
        const first = items[0], last = items[items.length - 1];
        if (event.shiftKey && document.activeElement === first) {event.preventDefault(); last.focus();}
        else if (!event.shiftKey && document.activeElement === last) {event.preventDefault(); first.focus();}
    }
});
mobileMenu.addEventListener("change", closeMenu);
closeMenu();

/*=========================================================
    SMOOTH BUTTON SCROLL
=========================================================*/

// if(primaryBtn){

// primaryBtn.addEventListener("click",(e)=>{

//     e.preventDefault();

//     const portfolio=document.querySelector(".portfolio");

//     if(portfolio){

//         portfolio.scrollIntoView({

//             behavior:"smooth"

//         });

//     }

// });

// }

// if(secondaryBtn){

// secondaryBtn.addEventListener("click",(e)=>{

//     e.preventDefault();

//     const footer=document.querySelector("footer");

//     if(footer){

//         footer.scrollIntoView({

//             behavior:"smooth"

//         });

//     }

// });

// }

/*=========================================================
    SMOOTH NAVIGATION
    Multi-page navigation handled by HTML links
=========================================================*/

// navLinks.forEach(link=>{

//     link.addEventListener("click",(e)=>{

//         e.preventDefault();

//         const target=link.getAttribute("href");

//         if(target.startsWith("#")){

//             const section=document.querySelector(target);

//             if(section){

//                 section.scrollIntoView({

//                     behavior:"smooth"

//                 });

//             }

//         }

//     });

// });

/*=========================================================
    SCROLL PROGRESS BAR
=========================================================*/

const progress=document.createElement("div");

progress.id="progress-bar";

document.body.appendChild(progress);

window.addEventListener("scroll",()=>{

    const totalHeight=document.documentElement.scrollHeight-window.innerHeight;

    const progressHeight=totalHeight > 0 ? (window.scrollY/totalHeight)*100 : 0;

    progress.style.width=progressHeight+"%";

});

/*=========================================================
    BACK TO TOP BUTTON
=========================================================*/

const topBtn=document.createElement("button");

topBtn.innerHTML="↑";

topBtn.id="topBtn";

document.body.appendChild(topBtn);

window.addEventListener("scroll",()=>{

    if(window.scrollY>500){

        topBtn.classList.add("show");

    }

    else{

        topBtn.classList.remove("show");

    }

});

topBtn.addEventListener("click",()=>{

    window.scrollTo({

        top:0,

        behavior:reducedMotion.matches ? "instant" : "smooth"

    });

});

/*=========================================================
    SIMPLE FADE-IN ON SCROLL
=========================================================*/

const revealElements=document.querySelectorAll(

".about,.services,.portfolio,.cta,.card,.item"

);

function revealOnScroll(){

    const trigger=window.innerHeight*0.85;

    revealElements.forEach(el=>{

        const top=el.getBoundingClientRect().top;

        if(top<trigger){

            el.classList.add("visible");

        }

    });

}

window.addEventListener("scroll",revealOnScroll);

window.addEventListener("load",revealOnScroll);

/*=========================================================
    CONSOLE MESSAGE
=========================================================*/

console.log(

"%cYOLO HOUSE PRODUCTIONS",

"color:#d4af37;font-size:20px;font-weight:bold;"

);

console.log(

"%cWebsite Developed with ❤️",

"color:white;font-size:14px;"

);

/*=========================================================
    END OF PART 1
    PART 2 STARTS BELOW THIS
=========================================================*/

/*=========================================================
    COUNTER ANIMATION
=========================================================*/

const counters = document.querySelectorAll(".stats h3");

let counterStarted = false;

function runCounters() {

    if (counterStarted) return;

    const statsSection = document.querySelector(".stats");

    if (!statsSection) return;

    const triggerPoint = window.innerHeight * 0.85;

    if (statsSection.getBoundingClientRect().top < triggerPoint) {

        counterStarted = true;

        counters.forEach(counter => {

            const target = parseInt(counter.innerText);

            if (reducedMotion.matches) {
                counter.innerText = target + "+";
                return;
            }

            let count = 0;

            const speed = target / 80;

            const updateCounter = () => {

                if (count < target) {

                    count += speed;

                    counter.innerText = Math.ceil(count) + "+";

                    requestAnimationFrame(updateCounter);

                } else {

                    counter.innerText = target + "+";

                }

            };

            updateCounter();

        });

    }

}

window.addEventListener("scroll", runCounters);
window.addEventListener("load", runCounters);

/*=========================================================
    RIPPLE BUTTON EFFECT
=========================================================*/

const allButtons = document.querySelectorAll(
".primary-btn,.secondary-btn,.btn"
);

allButtons.forEach(button => {

    button.addEventListener("click", function(e){

        if (reducedMotion.matches) return;

        const ripple = document.createElement("span");

        const rect = this.getBoundingClientRect();

        const size = Math.max(rect.width, rect.height);

        ripple.style.width = size + "px";
        ripple.style.height = size + "px";

        ripple.style.left = e.clientX - rect.left - size/2 + "px";
        ripple.style.top = e.clientY - rect.top - size/2 + "px";

        ripple.classList.add("ripple");

        this.appendChild(ripple);

        setTimeout(()=>{

            ripple.remove();

        },600);

    });

});

/*=========================================================
    CARD HOVER TILT
=========================================================*/

const cards = document.querySelectorAll(".card");

cards.forEach(card=>{

    card.addEventListener("mousemove",(e)=>{

        if (reducedMotion.matches) return;

        const rect = card.getBoundingClientRect();

        const x = e.clientX - rect.left;

        const y = e.clientY - rect.top;

        const rotateY = ((x / rect.width)-0.5)*18;

        const rotateX = ((y / rect.height)-0.5)*-18;

        card.style.transform =

        `perspective(900px)
        rotateX(${rotateX}deg)
        rotateY(${rotateY}deg)
        translateY(-8px)`;

    });

    card.addEventListener("mouseleave",()=>{

        card.style.transform="perspective(900px) rotateX(0) rotateY(0)";

    });

});

/*=========================================================
    PORTFOLIO IMAGE HOVER
=========================================================*/

const portfolioItems=document.querySelectorAll(".item");

portfolioItems.forEach(item=>{

    item.addEventListener("mouseenter",()=>{

        item.style.zIndex="5";

    });

    item.addEventListener("mouseleave",()=>{

        item.style.zIndex="1";

    });

});

/*=========================================================
    LAZY IMAGE LOADING
=========================================================*/

const lazyImages=document.querySelectorAll("img:not([data-viewer-image])");

const imageObserver=new IntersectionObserver((entries,observer)=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

const img=entry.target;

img.style.opacity="1";

img.style.transform="scale(1)";

observer.unobserve(img);

}

});

},{
threshold:0.2
});

lazyImages.forEach(img=>{

img.style.opacity="0";

img.style.transform="scale(.95)";

img.style.transition=reducedMotion.matches ? "none" : ".7s";

imageObserver.observe(img);

});

/*=========================================================
    PARALLAX HERO
=========================================================*/

const hero=document.querySelector(".hero");

window.addEventListener("scroll",()=>{

const offset=window.pageYOffset;

if(hero && !reducedMotion.matches){

hero.style.backgroundPositionY=offset*0.45+"px";

}

});

/*=========================================================
    RANDOM GOLD GLOW ON CARDS
=========================================================*/

cards.forEach(card=>{

card.addEventListener("mouseenter",()=>{

card.style.boxShadow=

"0 0 30px rgba(212,175,55,.25)";

});

card.addEventListener("mouseleave",()=>{

card.style.boxShadow="";

});

});

/*=========================================================
    KEYBOARD SHORTCUT
=========================================================*/

document.addEventListener("keydown",(e)=>{

if(e.key==="Home" && !e.target.closest("input,textarea,select,[contenteditable]")){

window.scrollTo({

top:0,

behavior:reducedMotion.matches ? "instant" : "smooth"

});

}

});

/*=========================================================
    PAGE LOADED
=========================================================*/

window.addEventListener("load",()=>{

document.body.classList.add("loaded");

});

/*=========================================================
    END OF PART 2
    PART 3 STARTS BELOW THIS
=========================================================*/

/*=========================================================
    PRELOADER
=========================================================*/

window.addEventListener("load", () => {

    const preloader = document.querySelector(".preloader");

    if(preloader){

        preloader.classList.add("hide");

        setTimeout(() => {

            preloader.remove();

        },700);

    }

});

/*=========================================================
    CUSTOM CURSOR
=========================================================*/

const cursor=document.createElement("div");

cursor.className="custom-cursor";

document.body.appendChild(cursor);

document.addEventListener("mousemove",(e)=>{

    cursor.style.left=e.clientX+"px";
    cursor.style.top=e.clientY+"px";

});

document.querySelectorAll("a,button,.card,.item").forEach(el=>{

    el.addEventListener("mouseenter",()=>{

        cursor.classList.add("cursor-grow");

    });

    el.addEventListener("mouseleave",()=>{

        cursor.classList.remove("cursor-grow");

    });

});

/*=========================================================
    MAGNETIC BUTTONS
=========================================================*/

document.querySelectorAll(".btn,.primary-btn,.secondary-btn").forEach(button=>{

button.addEventListener("mousemove",(e)=>{

if(reducedMotion.matches) return;

const rect=button.getBoundingClientRect();

const x=e.clientX-rect.left-rect.width/2;
const y=e.clientY-rect.top-rect.height/2;

button.style.transform=`translate(${x*0.18}px,${y*0.18}px)`;

});

button.addEventListener("mouseleave",()=>{

button.style.transform="translate(0,0)";

});

});

/*=========================================================
    HERO PARALLAX CONTENT
=========================================================*/

const heroContent=document.querySelector(".hero-content");
window.addEventListener("resize", () => {if (heroContent) heroContent.style.transform = "";});

document.addEventListener("mousemove",(e)=>{

if(!heroContent || reducedMotion.matches || !window.matchMedia("(min-width:993px) and (hover:hover) and (pointer:fine)").matches) return;

const x=(window.innerWidth/2-e.clientX)/45;
const y=(window.innerHeight/2-e.clientY)/45;

heroContent.style.transform=

`translate(${x}px,${y}px)`;

});

/*=========================================================
    FLOATING EFFECT
=========================================================*/

const floating=document.querySelectorAll(".card");

floating.forEach(card=>{

let direction=1;

setInterval(()=>{

if(reducedMotion.matches) return;

card.style.transform=

`translateY(${direction*6}px)`;

direction*=-1;

},2500);

});

/*=========================================================
    SCROLL REVEAL
=========================================================*/

const observer=new IntersectionObserver((entries)=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.classList.add("show");

}

});

},{
threshold:.15
});

document.querySelectorAll(

".card,.item,.about,.services,.portfolio,.cta"

).forEach(el=>{

observer.observe(el);

});

/*=========================================================
    DISABLE IMAGE DRAG
=========================================================*/

document.querySelectorAll("img").forEach(img=>{

img.setAttribute("draggable","false");

});

/*=========================================================
    HOMEPAGE CINEMATIC CTA
=========================================================*/

function initHomepageCTA() {
    const section = document.querySelector(".home-project-cta");
    if (!section) return;
    const pointerAllowed = window.matchMedia("(hover:hover) and (pointer:fine)");
    let frame = 0;
    let target = {x:50, y:35};
    let current = {x:50, y:35};
    section.classList.add("cta-enhanced");
    const reveal = () => section.classList.add("is-in-view");
    if (reducedMotion.matches || !("IntersectionObserver" in window)) reveal();
    else {
        const entrance = new IntersectionObserver(entries => {
            if (entries.some(entry => entry.isIntersecting)) {reveal(); entrance.disconnect();}
        }, {threshold:0, rootMargin:"0px 0px -32px 0px"});
        entrance.observe(section);
    }
    section.addEventListener("focusin", reveal);

    function illuminate() {
        current.x += (target.x - current.x) * .2;
        current.y += (target.y - current.y) * .2;
        section.style.setProperty("--cta-spot-x", current.x.toFixed(2) + "%");
        section.style.setProperty("--cta-spot-y", current.y.toFixed(2) + "%");
        frame = Math.abs(target.x-current.x) + Math.abs(target.y-current.y) > .05 ? requestAnimationFrame(illuminate) : 0;
    }
    function resetIllumination() {
        cancelAnimationFrame(frame);
        frame = 0;
        current = {x:50, y:35};
        target = {x:50, y:35};
        section.style.removeProperty("--cta-spot-x");
        section.style.removeProperty("--cta-spot-y");
    }
    section.addEventListener("pointermove", event => {
        if (event.pointerType !== "mouse" || !pointerAllowed.matches || reducedMotion.matches) return;
        const bounds = section.getBoundingClientRect();
        target = {x:40 + Math.max(0,Math.min(1,(event.clientX-bounds.left)/bounds.width))*20, y:22 + Math.max(0,Math.min(1,(event.clientY-bounds.top)/bounds.height))*26};
        if (!frame) frame = requestAnimationFrame(illuminate);
    }, {passive:true});
    section.addEventListener("pointerleave", resetIllumination, {passive:true});
    pointerAllowed.addEventListener("change", resetIllumination);
    reducedMotion.addEventListener("change", () => {
        if (reducedMotion.matches) {resetIllumination(); reveal();}
    });
    document.addEventListener("visibilitychange", () => {if (document.hidden) resetIllumination();});
}
initHomepageCTA();

/*=========================================================
    HOMEPAGE CREATIVE APPROACH
=========================================================*/

function initCreativeApproach() {
    const section = document.querySelector(".home-approach");
    if (!section) return;
    const steps = [...section.querySelectorAll("[data-approach-step]")];
    const nodes = [...section.querySelectorAll("[data-approach-node]")];
    const status = section.querySelector(".approach-status");

    function updateGraphic() {
        const active = steps.findIndex(step => step.open);
        section.style.setProperty("--approach-progress", active < 0 ? 0 : active * 100 / (steps.length - 1));
        nodes.forEach((node, index) => node.classList.toggle("is-active", index <= active));
        status.textContent = active < 0 ? "Choose a creative stage" : String(active + 1).padStart(2, "0") + " / " + steps[active].querySelector(".approach-step-title").textContent;
    }
    steps.forEach(step => step.addEventListener("toggle", () => {
        if (step.open) steps.forEach(other => {if (other !== step) other.open = false;});
        updateGraphic();
    }));
    updateGraphic();
    section.classList.add("approach-enhanced");
    function showApproach() {section.classList.add("is-in-view");}
    if (reducedMotion.matches || !("IntersectionObserver" in window)) showApproach();
    else {
        const entrance = new IntersectionObserver(entries => {
            if (entries.some(entry => entry.isIntersecting)) {showApproach(); entrance.disconnect();}
        }, {threshold:0, rootMargin:"0px 0px -40px 0px"});
        entrance.observe(section);
    }
    // Keyboard focus and a live preference change must never leave the component hidden.
    section.addEventListener("focusin", showApproach);
    reducedMotion.addEventListener("change", () => {if (reducedMotion.matches) showApproach();});
}
initCreativeApproach();

/*=========================================================
    FEATURED PROJECTS — CINEMATIC LIGHTBOX
=========================================================*/

function initProjectLightbox() {
    const dialog = document.querySelector("#project-lightbox");
    const triggers = [...document.querySelectorAll("#portfolio .project-trigger")];
    if (!dialog || !triggers.length) return;

    const projects = triggers.map(trigger => {
        const thumbnail = trigger.querySelector("img");
        return {
            src: thumbnail.currentSrc || thumbnail.src,
            alt: thumbnail.alt,
            title: trigger.dataset.projectTitle || thumbnail.getAttribute("title") || ""
        };
    });
    const image = dialog.querySelector("[data-viewer-image]");
    const stage = dialog.querySelector(".viewer-stage");
    const layers = [...dialog.querySelectorAll(".viewer-background-layer")];
    const counter = dialog.querySelector(".viewer-counter");
    const title = dialog.querySelector(".viewer-title");
    const loading = dialog.querySelector(".viewer-loading");
    const error = dialog.querySelector(".viewer-error");
    const closeButton = dialog.querySelector("[data-viewer-close]");
    const imageLoads = new Map();
    let selected = 0;
    let selectionVersion = 0;
    let activeLayer = -1;
    let dimensions = null;
    let returnFocus = null;
    let scrollState = null;
    let swipe = null;
    let ignoreBackdropUntil = 0;

    // Retain only metadata promises, not a collection of decoded full-resolution images.
    function loadImage(src) {
        if (imageLoads.has(src)) return imageLoads.get(src);
        const promise = new Promise((resolve, reject) => {
            const probe = new Image();
            probe.onload = () => {
                const result = {src, width: probe.naturalWidth, height: probe.naturalHeight};
                probe.onload = probe.onerror = null;
                if (result.width && result.height) resolve(result);
                else reject(new Error("Image dimensions unavailable"));
            };
            probe.onerror = () => {
                probe.onload = probe.onerror = null;
                reject(new Error("Project image unavailable"));
            };
            probe.src = src;
        });
        imageLoads.set(src, promise);
        promise.catch(() => {
            if (imageLoads.get(src) === promise) imageLoads.delete(src);
        });
        return promise;
    }

    function fitImage() {
        if (!dialog.open || !dimensions) return;
        const scale = Math.min(1, stage.clientWidth / dimensions.width, stage.clientHeight / dimensions.height);
        image.style.width = Math.floor(dimensions.width * scale) + "px";
        image.style.height = Math.floor(dimensions.height * scale) + "px";
    }

    function changeBackground(src) {
        const nextLayer = (activeLayer + 1) % layers.length;
        layers[nextLayer].style.backgroundImage = `url(${JSON.stringify(src)})`;
        layers.forEach((layer, index) => layer.classList.toggle("is-visible", index === nextLayer));
        activeLayer = nextLayer;
    }

    function preloadAdjacent() {
        const neighbours = [selected, (selected + 1) % projects.length, (selected - 1 + projects.length) % projects.length];
        const keep = new Set(neighbours.map(index => projects[index].src));
        for (const src of imageLoads.keys()) {
            if (!keep.has(src)) imageLoads.delete(src);
        }
        neighbours.slice(1).forEach(index => loadImage(projects[index].src).catch(() => {}));
    }

    async function selectProject(index) {
        selected = (index + projects.length) % projects.length;
        const version = ++selectionVersion;
        const project = projects[selected];
        dialog.dataset.state = "loading";
        counter.textContent = String(selected + 1).padStart(2, "0") + " / " + String(projects.length).padStart(2, "0");
        title.textContent = project.title;
        title.hidden = !project.title;
        if (error.contains(document.activeElement)) closeButton.focus({preventScroll:true});
        error.hidden = true;
        loading.hidden = false;
        try {
            const [metadata] = await Promise.all([
                loadImage(project.src),
                new Promise(resolve => window.setTimeout(resolve, reducedMotion.matches ? 0 : 140))
            ]);
            if (version !== selectionVersion || !dialog.open) return;
            dimensions = metadata;
            image.alt = project.alt || project.title || `Featured project image ${selected + 1} of ${projects.length}`;
            image.src = metadata.src;
            image.hidden = false;
            fitImage();
            if (image.decode) await image.decode();
            if (version !== selectionVersion || !dialog.open) return;
            changeBackground(metadata.src);
            loading.hidden = true;
            dialog.dataset.state = "ready";
        } catch {
            if (version !== selectionVersion || !dialog.open) return;
            dimensions = null;
            image.hidden = true;
            image.removeAttribute("src");
            loading.hidden = true;
            error.hidden = false;
            layers.forEach(layer => {
                layer.classList.remove("is-visible");
                layer.style.backgroundImage = "";
            });
            activeLayer = -1;
            dialog.dataset.state = "error";
        }
        if (version === selectionVersion && dialog.open) preloadAdjacent();
    }

    function restorePage() {
        if (!scrollState) return;
        ++selectionVersion;
        const saved = scrollState;
        scrollState = null;
        swipe = null;
        document.body.classList.remove("project-viewer-open");
        document.body.style.top = saved.top;
        document.body.style.paddingRight = saved.paddingRight;
        const root = document.documentElement;
        const previousBehaviour = root.style.scrollBehavior;
        root.style.scrollBehavior = "auto";
        window.scrollTo(0, saved.y);
        root.style.scrollBehavior = previousBehaviour;
        if (returnFocus && returnFocus.isConnected) returnFocus.focus({preventScroll:true});
        image.hidden = true;
        image.removeAttribute("src");
        dimensions = null;
        layers.forEach(layer => {
            layer.classList.remove("is-visible");
            layer.style.backgroundImage = "";
        });
        activeLayer = -1;
    }

    function closeViewer() {
        if (!dialog.open) return;
        dialog.close();
        restorePage();
    }

    triggers.forEach((trigger, index) => trigger.addEventListener("click", () => {
        if (dialog.open) return;
        if (document.body.classList.contains("menu-open")) closeMenu();
        returnFocus = trigger;
        const scrollbar = window.innerWidth - document.documentElement.clientWidth;
        scrollState = {y: window.scrollY, top: document.body.style.top, paddingRight: document.body.style.paddingRight};
        document.body.style.top = `-${scrollState.y}px`;
        if (scrollbar > 0) document.body.style.paddingRight = (parseFloat(getComputedStyle(document.body).paddingRight) + scrollbar) + "px";
        document.body.classList.add("project-viewer-open");
        dialog.showModal();
        closeButton.focus({preventScroll:true});
        selectProject(index);
    }));

    closeButton.addEventListener("click", closeViewer);
    dialog.querySelector("[data-viewer-previous]").addEventListener("click", () => selectProject(selected - 1));
    dialog.querySelector("[data-viewer-next]").addEventListener("click", () => selectProject(selected + 1));
    dialog.querySelector("[data-viewer-retry]").addEventListener("click", () => selectProject(selected));
    dialog.addEventListener("cancel", event => {event.preventDefault(); closeViewer();});
    dialog.addEventListener("close", () => {if (!dialog.open) restorePage();});
    dialog.addEventListener("click", event => {
        if (performance.now() < ignoreBackdropUntil) return;
        if (!event.target.closest("button,[data-viewer-image],.viewer-meta,.viewer-error")) closeViewer();
    });
    dialog.addEventListener("keydown", event => {
        if (event.key === "Tab") {
            const focusable = [...dialog.querySelectorAll("button:not([disabled])")].filter(button => button.getClientRects().length && !button.closest("[hidden]"));
            const first = focusable[0], last = focusable[focusable.length - 1];
            if (!focusable.includes(document.activeElement)) {event.preventDefault(); (event.shiftKey ? last : first).focus();}
            else if (event.shiftKey && document.activeElement === first) {event.preventDefault(); last.focus();}
            else if (!event.shiftKey && document.activeElement === last) {event.preventDefault(); first.focus();}
            return;
        }
        if (event.target.closest("input,textarea,select,[contenteditable]")) return;
        if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
            event.preventDefault();
            event.stopPropagation();
            selectProject(selected + (event.key === "ArrowRight" ? 1 : -1));
        }
    });

    // Let the browser keep vertical/pinch gestures; recognize only clear horizontal swipes.
    stage.addEventListener("pointerdown", event => {
        if (event.pointerType !== "touch") return;
        if (!event.isPrimary || event.target.closest("button")) {swipe = null; return;}
        swipe = {id: event.pointerId, x: event.clientX, y: event.clientY, time: performance.now()};
    }, {passive:true});
    stage.addEventListener("pointerup", event => {
        if (!swipe || event.pointerId !== swipe.id) return;
        const dx = event.clientX - swipe.x, dy = event.clientY - swipe.y;
        const elapsed = performance.now() - swipe.time;
        swipe = null;
        if (elapsed < 900 && Math.abs(dx) >= 50 && Math.abs(dx) > Math.abs(dy) * 1.5) {
            ignoreBackdropUntil = performance.now() + 450;
            selectProject(selected + (dx < 0 ? 1 : -1));
        }
    }, {passive:true});
    stage.addEventListener("pointercancel", () => {swipe = null;}, {passive:true});
    new ResizeObserver(fitImage).observe(stage);
}
initProjectLightbox();

/*=========================================================
    LOCAL PROJECT ENQUIRY REVIEW
=========================================================*/

const enquiryForm = document.querySelector("#project-form");
if (enquiryForm) {
    const reviewButton = document.querySelector("#review-enquiry");
    const errorSummary = document.querySelector("#enquiry-errors");
    const review = document.querySelector("#enquiry-review");
    const status = document.querySelector("#enquiry-status");
    const brief = document.querySelector("#enquiry-brief");
    const copyButton = document.querySelector("#copy-brief");
    const copyStatus = document.querySelector("#copy-status");
    const fields = [...enquiryForm.querySelectorAll("fieldset input,fieldset select,fieldset textarea")];
    enquiryForm.querySelector("fieldset").disabled = false;
    reviewButton.disabled = false;

    function fieldError(field) {
        field.setCustomValidity("");
        const value = field.value.trim();
        if (field.required && !value) return "Please enter " + (field.id === "enquiry-details" ? "your project details." : field.id === "enquiry-service" ? "a service." : field.id === "enquiry-email" ? "your email address." : "your name.");
        if (field.type === "email" && field.validity.typeMismatch) return "Enter a valid email address, such as name@example.com.";
        if (field.id === "enquiry-details" && value.length < 20) return "Add at least 20 characters describing your project.";
        if (field.validity.tooLong) return "Please shorten this entry.";
        return "";
    }

    function markField(field, message) {
        const error = document.getElementById(field.id + "-error");
        field.setAttribute("aria-invalid", String(Boolean(message)));
        error.textContent = message;
        error.hidden = !message;
    }

    function reviewEnquiry(event) {
        event.preventDefault();
        errorSummary.querySelector("ul").replaceChildren();
        const invalid = [];
        fields.forEach(field => {
            const message = fieldError(field);
            markField(field, message);
            if (message) {
                invalid.push(field);
                const item = document.createElement("li");
                const link = document.createElement("a");
                link.href = "#" + field.id;
                link.textContent = message;
                link.addEventListener("click", event => {event.preventDefault(); field.focus();});
                item.appendChild(link);
                errorSummary.querySelector("ul").appendChild(item);
            }
        });
        errorSummary.hidden = !invalid.length;
        if (invalid.length) {
            review.hidden = true;
            errorSummary.focus();
            return;
        }
        const value = name => enquiryForm.elements.namedItem(name).value.trim();
        brief.value = ["YOLO HOUSE — PROJECT BRIEF (NOT SENT)", "", "Name: " + value("name"), "Email: " + value("email"), "Company: " + (value("company") || "Not specified"), "Service: " + value("service"), "Ideal timeline: " + (value("timeline") || "Not specified"), "", "Project details:", value("details")].join("\n");
        status.textContent = "Your brief is ready to copy. Nothing has been sent; online enquiries are not available yet.";
        copyStatus.textContent = "";
        review.hidden = false;
        status.focus();
    }

    enquiryForm.addEventListener("submit", reviewEnquiry);
    reviewButton.addEventListener("click", reviewEnquiry);
    fields.forEach(field => field.addEventListener("input", () => {
        if (field.getAttribute("aria-invalid") === "true") markField(field, fieldError(field));
        // Hide the previous brief so edited details cannot be mistaken for a current review.
        review.hidden = true;
        if (!fields.some(item => item.getAttribute("aria-invalid") === "true")) errorSummary.hidden = true;
    }));
    copyButton.addEventListener("click", async () => {
        try {
            if (!navigator.clipboard) throw new Error("Clipboard unavailable");
            await navigator.clipboard.writeText(brief.value);
            copyStatus.textContent = "Brief copied. It has not been sent.";
        } catch {
            brief.focus();
            brief.select();
            copyStatus.textContent = "Automatic copying is unavailable. Your brief is selected; use your device’s copy command.";
        }
    });
}

reducedMotion.addEventListener("change", () => {
    if (reducedMotion.matches) {
        if (heroContent) heroContent.style.transform = "";
        if (hero) hero.style.backgroundPositionY = "";
        document.querySelectorAll(".btn,.primary-btn,.secondary-btn,.card").forEach(element => element.style.transform = "");
        lazyImages.forEach(img => img.style.transition = "none");
    }
});

/*=========================================================
    CONSOLE BRANDING
=========================================================*/

console.clear();

console.log(

"%cYOLO HOUSE PRODUCTIONS",

"font-size:28px;color:#d4af37;font-weight:bold;"

);

console.log(

"%cPremium Website Developed ❤️",

"font-size:15px;color:white;"

);

/*=========================================================
    END OF MAIN.JS
=========================================================*/

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
