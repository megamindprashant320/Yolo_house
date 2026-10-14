/*=========================================================
    YOLO HOUSE PRODUCTIONS
    MAIN.JS
    PART - 1
=========================================================*/

"use strict";

const isHomepage = document.body.classList.contains("home-page");
if (isHomepage) document.body.classList.add("motion-ready");
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
    if (header && !document.body.matches(".menu-open,.project-viewer-open")) header.classList.toggle("scrolled", window.scrollY > 50);
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
    if (isHomepage) document.querySelectorAll("main,body > footer,#topBtn,.skip-link").forEach(element => {element.inert = open;});
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

/*=========================================================
    BACK TO TOP BUTTON
=========================================================*/

const topBtn=document.createElement("button");

topBtn.innerHTML="↑";

topBtn.id="topBtn";

document.body.appendChild(topBtn);

topBtn.type = "button";
topBtn.setAttribute("aria-label", "Back to top");
progress.setAttribute("aria-hidden", "true");
let scrollUIFrame = 0;
function updateScrollUI() {
    scrollUIFrame = 0;
    const total = document.documentElement.scrollHeight - innerHeight;
    const fraction = total > 0 ? scrollY / total : 0;
    if (isHomepage) progress.style.transform = `scaleX(${fraction})`;
    else progress.style.width = fraction * 100 + "%";
    topBtn.classList.toggle("show", scrollY > 500);
}
window.addEventListener("scroll", () => {
    if (!scrollUIFrame) scrollUIFrame = requestAnimationFrame(updateScrollUI);
}, {passive:true});
window.addEventListener("resize", updateScrollUI, {passive:true});
updateScrollUI();

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

if (!isHomepage) {
    window.addEventListener("scroll",revealOnScroll,{passive:true});
    window.addEventListener("load",revealOnScroll);
}

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

if (counters.length) {
    window.addEventListener("scroll", runCounters, {passive:true});
    window.addEventListener("load", runCounters);
}

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

const lazyImages=document.querySelectorAll("img:not([data-viewer-image]):not([data-story-image])");

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

img.style.transition=reducedMotion.matches ? "none" : "opacity .7s, transform .7s";
if (reducedMotion.matches) {img.style.opacity="1";img.style.transform="scale(1)";return;}

imageObserver.observe(img);

});

/*=========================================================
    PARALLAX HERO
=========================================================*/

const hero=document.querySelector(".hero");

if (hero) {
    let parallaxFrame = 0;
    window.addEventListener("scroll", () => {
        if (reducedMotion.matches || parallaxFrame) return;
        parallaxFrame = requestAnimationFrame(() => {
            parallaxFrame = 0;
            if (!reducedMotion.matches && scrollY < hero.offsetHeight) hero.style.backgroundPositionY = scrollY * .45 + "px";
        });
    }, {passive:true});
}

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

cursor.setAttribute("aria-hidden", "true");
const finePointer = window.matchMedia("(hover:hover) and (pointer:fine)");
let cursorFrame = 0, cursorPoint = {x:0,y:0};
document.addEventListener("mousemove", event => {
    if (!finePointer.matches || reducedMotion.matches) return;
    cursorPoint = {x:event.clientX,y:event.clientY};
    if (!cursorFrame) cursorFrame = requestAnimationFrame(() => {
        cursorFrame = 0;
        cursor.style.left = cursorPoint.x + "px";
        cursor.style.top = cursorPoint.y + "px";
    });
}, {passive:true});

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

const heroPointer = window.matchMedia("(min-width:993px) and (hover:hover) and (pointer:fine)");
let heroPointerFrame = 0, heroPointerPoint = {x:0,y:0};
document.addEventListener("mousemove", event => {
    if (!heroContent || reducedMotion.matches || !heroPointer.matches || scrollY >= hero.offsetHeight) return;
    heroPointerPoint = {x:event.clientX,y:event.clientY};
    if (!heroPointerFrame) heroPointerFrame = requestAnimationFrame(() => {
        heroPointerFrame = 0;
        if (!reducedMotion.matches) heroContent.style.transform = `translate(${(innerWidth/2-heroPointerPoint.x)/45}px,${(innerHeight/2-heroPointerPoint.y)/45}px)`;
    });
}, {passive:true});

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
if (entry.target.matches(".about-story,.mission-vision,.company-stats")) observer.unobserve(entry.target);
if (isHomepage) {entry.target.classList.add("visible");observer.unobserve(entry.target);}

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
    const triggers = [...document.querySelectorAll("#portfolio .project-trigger,.portfolio-page .portfolio-preview")];
    if (!dialog || !triggers.length) return;

    const allProjects = triggers.map(trigger => {
        const card = trigger.closest(".portfolio-card") || trigger;
        const thumbnail = card.querySelector("img");
        const cardTitle = card.querySelector("h3")?.textContent.trim();
        return {
            trigger,
            src: thumbnail.currentSrc || thumbnail.src,
            alt: thumbnail.alt || cardTitle,
            title: cardTitle || trigger.dataset.projectTitle || thumbnail.getAttribute("title") || "",
            category: card.querySelector(".portfolio-overlay span")?.textContent.trim() || ""
        };
    });
    let projects = allProjects;
    const image = dialog.querySelector("[data-viewer-image]");
    const stage = dialog.querySelector(".viewer-stage");
    const layers = [...dialog.querySelectorAll(".viewer-background-layer")];
    const counter = dialog.querySelector(".viewer-counter");
    const title = dialog.querySelector(".viewer-title");
    const category = dialog.querySelector(".viewer-category");
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
        if (category) {
            category.textContent = project.category;
            category.hidden = !project.category;
        }
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

    triggers.forEach(trigger => trigger.addEventListener("click", () => {
        if (dialog.open || trigger.closest("[hidden]")) return;
        projects = allProjects.filter(project => !project.trigger.closest("[hidden]"));
        dialog.querySelector(".viewer-navigation").hidden = projects.length < 2;
        if (document.body.classList.contains("menu-open")) closeMenu();
        returnFocus = trigger;
        const scrollbar = window.innerWidth - document.documentElement.clientWidth;
        scrollState = {y: window.scrollY, top: document.body.style.top, paddingRight: document.body.style.paddingRight};
        document.body.style.top = `-${scrollState.y}px`;
        if (scrollbar > 0) document.body.style.paddingRight = (parseFloat(getComputedStyle(document.body).paddingRight) + scrollbar) + "px";
        document.body.classList.add("project-viewer-open");
        dialog.showModal();
        closeButton.focus({preventScroll:true});
        selectProject(projects.findIndex(project => project.trigger === trigger));
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
            if (projects.length > 1) selectProject(selected + (event.key === "ArrowRight" ? 1 : -1));
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
        if (projects.length > 1 && elapsed < 900 && Math.abs(dx) >= 50 && Math.abs(dx) > Math.abs(dy) * 1.5) {
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
        if (field.maxLength >= 0 && field.value.length > field.maxLength) return "Use no more than " + field.maxLength + " characters.";
        return "";
    }

    function markField(field, message) {
        const error = document.getElementById(field.id + "-error");
        field.setAttribute("aria-invalid", String(Boolean(message)));
        error.textContent = message;
        error.hidden = !message;
    }

    function updateErrorSummary() {
        errorSummary.querySelector("ul").replaceChildren();
        const invalid = fields.filter(field => field.getAttribute("aria-invalid") === "true");
        invalid.forEach(field => {
            const item = document.createElement("li");
            const link = document.createElement("a");
            link.href = "#" + field.id;
            link.textContent = document.getElementById(field.id + "-error").textContent;
            link.addEventListener("click", event => {event.preventDefault(); field.focus();});
            item.appendChild(link);
            errorSummary.querySelector("ul").appendChild(item);
        });
        errorSummary.hidden = !invalid.length;
        return invalid.length;
    }

    function reviewEnquiry(event) {
        event.preventDefault();
        fields.forEach(field => {
            markField(field, fieldError(field));
        });
        if (updateErrorSummary()) {
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
    fields.forEach(field => field.addEventListener("input", () => {
        if (field.hasAttribute("aria-invalid")) markField(field, fieldError(field));
        // Hide the previous brief so edited details cannot be mistaken for a current review.
        review.hidden = true;
        if (!errorSummary.hidden) updateErrorSummary();
    }));
    copyButton.addEventListener("click", async () => {
        const preparedBrief = brief.value;
        copyButton.disabled = true;
        copyStatus.textContent = "Copying your brief…";
        try {
            if (!navigator.clipboard) throw new Error("Clipboard unavailable");
            await navigator.clipboard.writeText(preparedBrief);
            if (!review.hidden && brief.value === preparedBrief) copyStatus.textContent = "Brief copied. It has not been sent.";
        } catch {
            if (review.hidden || brief.value !== preparedBrief) return;
            brief.focus();
            brief.select();
            copyStatus.textContent = "Automatic copying is unavailable. Your brief is selected; use your device’s copy command.";
        } finally {
            copyButton.disabled = false;
        }
    });
}

reducedMotion.addEventListener("change", () => {
    if (reducedMotion.matches) {
        if (heroContent) heroContent.style.transform = "";
        if (hero) hero.style.backgroundPositionY = "";
        document.querySelectorAll(".btn,.primary-btn,.secondary-btn,.card").forEach(element => element.style.transform = "");
        lazyImages.forEach(img => {img.style.transition = "none";img.style.opacity="1";img.style.transform="scale(1)";});
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

if (isHomepage) {
    document.querySelectorAll(".about,.services,.portfolio,.item").forEach(element => {
        element.addEventListener("focusin", () => {element.classList.add("show","visible");});
    });
    document.querySelector(".skip-link").addEventListener("click", () => {
        document.querySelector("#main-content").focus({preventScroll:true});
    });
}

/* Our Story shares the existing one-time reveal observer and owns its image transition. */
const aboutStory = document.querySelector(".about-story");
if (aboutStory) {
    const showStory = () => aboutStory.classList.add("show");
    aboutStory.classList.add("story-enhanced");
    if (reducedMotion.matches) showStory();
    else observer.observe(aboutStory);
    aboutStory.addEventListener("focusin", showStory);
    reducedMotion.addEventListener("change", () => {if (reducedMotion.matches) showStory();});
}

function initPurposeExperience() {
    const section = document.querySelector(".mission-vision");
    if (!section) return;
    const experience = section.querySelector(".purpose-experience");
    const selector = section.querySelector(".purpose-selectors");
    const buttons = [...section.querySelectorAll("[data-purpose-select]")];
    const panels = [...section.querySelectorAll(".purpose-panel")];
    if (!experience || buttons.length !== 2 || panels.length !== 2) return;
    const compact = matchMedia("(max-width:768px)");
    const pointer = matchMedia("(hover:hover) and (pointer:fine)");
    let active = 0, frame = 0;
    let point = {x:50,y:35};
    function select(index) {
        active = index;
        experience.dataset.active = String(index);
        buttons.forEach((button,i) => {
            button.classList.toggle("is-active",i===index);
            button.tabIndex = compact.matches && i!==index ? -1 : 0;
            button.setAttribute(compact.matches ? "aria-selected" : "aria-pressed",String(i===index));
        });
        panels.forEach((panel,i) => {
            panel.classList.toggle("is-active",i===index);
            panel.inert = compact.matches && i!==index;
            if (compact.matches && i!==index) panel.setAttribute("aria-hidden","true");
            else panel.removeAttribute("aria-hidden");
        });
    }
    function adapt() {
        const focusInSelector = selector.contains(document.activeElement);
        selector.removeAttribute("role");
        if (compact.matches) selector.setAttribute("role","tablist");
        buttons.forEach((button,i) => {
            button.removeAttribute("aria-selected");button.removeAttribute("aria-pressed");
            if (compact.matches) button.setAttribute("role","tab");else button.removeAttribute("role");
            panels[i].setAttribute("aria-labelledby",compact.matches ? button.id : "purpose-heading-"+i);
            if (compact.matches) {panels[i].setAttribute("role","tabpanel");panels[i].tabIndex=0;}
            else {panels[i].removeAttribute("role");panels[i].removeAttribute("tabindex");}
        });
        select(active);
        if (compact.matches && focusInSelector) buttons[active].focus({preventScroll:true});
        resetLight();
    }
    function resetLight() {
        cancelAnimationFrame(frame);frame=0;
        experience.style.removeProperty("--purpose-x");experience.style.removeProperty("--purpose-y");
    }
    buttons.forEach((button,index) => button.addEventListener("click",() => select(index)));
    selector.addEventListener("keydown",event => {
        if (!compact.matches || !["ArrowLeft","ArrowRight","Home","End"].includes(event.key)) return;
        const current = buttons.indexOf(document.activeElement);
        if (current < 0) return;
        event.preventDefault();
        event.stopPropagation();
        const next = event.key==="Home" ? 0 : event.key==="End" ? 1 : (current+(event.key==="ArrowRight" ? 1 : -1)+2)%2;
        select(next);buttons[next].focus();
    });
    experience.addEventListener("pointermove",event => {
        if (compact.matches || !pointer.matches || reducedMotion.matches || event.pointerType!=="mouse") return;
        const rect=experience.getBoundingClientRect();
        point={x:35+Math.max(0,Math.min(1,(event.clientX-rect.left)/rect.width))*30,y:25+Math.max(0,Math.min(1,(event.clientY-rect.top)/rect.height))*30};
        if (!frame) frame=requestAnimationFrame(() => {
            frame=0;
            experience.style.setProperty("--purpose-x",point.x.toFixed(2)+"%");
            experience.style.setProperty("--purpose-y",point.y.toFixed(2)+"%");
        });
    },{passive:true});
    experience.addEventListener("pointerleave",resetLight,{passive:true});
    pointer.addEventListener("change",resetLight);
    compact.addEventListener("change",adapt);
    reducedMotion.addEventListener("change",() => {resetLight();if(reducedMotion.matches)section.classList.add("show");});
    section.addEventListener("focusin",() => section.classList.add("show"));
    section.classList.add("purpose-enhanced");selector.hidden=false;adapt();
    if (reducedMotion.matches) section.classList.add("show");else observer.observe(section);
}
initPurposeExperience();

function initStrengthShowcase() {
    const section=document.querySelector(".why-us");
    if (!section || section.dataset.strengthReady) return;
    const selector=section.querySelector(".strength-selector");
    const buttons=[...section.querySelectorAll(".strength-selector button")];
    const panels=[...section.querySelectorAll(".strength-panel")];
    if (!selector || buttons.length!==4 || panels.length!==4) return;
    section.dataset.strengthReady="true";
    const compact=matchMedia("(max-width:768px)");
    let active=0;
    function select(index) {
        active=index;section.style.setProperty("--strength-index",String(index));
        buttons.forEach((button,i)=>{button.setAttribute("aria-selected",String(i===index));button.tabIndex=i===index ? 0 : -1;});
        panels.forEach((panel,i)=>{panel.classList.toggle("is-active",i===index);panel.inert=i!==index;panel.setAttribute("aria-hidden",String(i!==index));});
    }
    selector.setAttribute("role","tablist");
    buttons.forEach((button,i)=>{button.setAttribute("role","tab");button.addEventListener("click",()=>select(i));});
    panels.forEach((panel,i)=>{panel.setAttribute("role","tabpanel");panel.setAttribute("aria-labelledby",buttons[i].id);panel.tabIndex=0;});
    function adapt(){selector.setAttribute("aria-orientation",compact.matches ? "horizontal" : "vertical");select(active);}
    selector.addEventListener("keydown",event=>{
        if (!["ArrowLeft","ArrowRight","ArrowUp","ArrowDown","Home","End"].includes(event.key)) return;
        const current=buttons.indexOf(document.activeElement);if(current<0)return;
        event.preventDefault();event.stopPropagation();
        let next;
        if(event.key==="Home")next=0;
        else if(event.key==="End")next=3;
        else {const direction=["ArrowRight","ArrowDown"].includes(event.key) ? 1 : -1;const step=compact.matches && ["ArrowUp","ArrowDown"].includes(event.key) ? 2 : 1;next=(current+direction*step+4)%4;}
        select(next);buttons[next].focus();
    });
    compact.addEventListener("change",adapt);
    section.classList.add("strength-enhanced");selector.hidden=false;adapt();
}
initStrengthShowcase();

/* No count-up targets are supplied: all historical business figures remain unverified. */
const aboutCredibility=document.querySelector(".company-stats");
if (aboutCredibility) {
    aboutCredibility.classList.add("credibility-enhanced");
    const revealCredibility=()=>aboutCredibility.classList.add("show");
    if (reducedMotion.matches) revealCredibility();else observer.observe(aboutCredibility);
    aboutCredibility.addEventListener("focusin",revealCredibility);
    reducedMotion.addEventListener("change",()=>{if(reducedMotion.matches)revealCredibility();});
}

function initServicesShowcase() {
    const section=document.querySelector(".services-showcase");
    if (!section || section.dataset.showcaseReady) return;
    const selector=section.querySelector(".service-selector");
    const stage=section.querySelector(".service-stage");
    const buttons=[...section.querySelectorAll(".service-selector button")];
    const panels=[...section.querySelectorAll(".service-presentation")];
    if (!selector || !stage || buttons.length!==6 || panels.length!==6) return;
    const compact=matchMedia("(max-width:768px)");
    const pointerAllowed=matchMedia("(hover:hover) and (pointer:fine)");
    let active=0, frame=0, point={x:0,y:0};
    function select(index) {
        active=index;section.style.setProperty("--selected-service",String(index));
        buttons.forEach((button,i)=>{button.setAttribute("aria-selected",String(i===index));button.tabIndex=i===index ? 0 : -1;});
        panels.forEach((panel,i)=>{panel.classList.toggle("is-active",i===index);panel.inert=i!==index;panel.setAttribute("aria-hidden",String(i!==index));});
    }
    function resetLight() {
        cancelAnimationFrame(frame);frame=0;
        stage.style.removeProperty("--service-light-x");stage.style.removeProperty("--service-light-y");
    }
    function adapt() {
        selector.setAttribute("aria-orientation",compact.matches ? "horizontal" : "vertical");
        select(active);resetLight();
    }
    function selectHash(scroll) {
        let id;
        try {id=decodeURIComponent(location.hash.slice(1));}catch{return;}
        const index=panels.findIndex(panel=>panel.id===id);
        if (index<0) return;
        select(index);
        if (scroll) requestAnimationFrame(()=>panels[index].scrollIntoView({block:"start",behavior:"instant"}));
    }
    selector.setAttribute("role","tablist");
    buttons.forEach((button,i)=>{button.setAttribute("role","tab");button.addEventListener("click",()=>select(i));});
    panels.forEach((panel,i)=>{panel.setAttribute("role","tabpanel");panel.setAttribute("aria-labelledby",buttons[i].id);panel.tabIndex=0;});
    selector.addEventListener("keydown",event=>{
        if (!["ArrowLeft","ArrowRight","ArrowUp","ArrowDown","Home","End"].includes(event.key)) return;
        const current=buttons.indexOf(document.activeElement);if(current<0)return;
        event.preventDefault();event.stopPropagation();
        let next;
        if(event.key==="Home")next=0;
        else if(event.key==="End")next=buttons.length-1;
        else {const direction=["ArrowRight","ArrowDown"].includes(event.key) ? 1 : -1;const step=compact.matches && ["ArrowUp","ArrowDown"].includes(event.key) ? 2 : 1;next=(current+direction*step+buttons.length)%buttons.length;}
        select(next);buttons[next].focus();
    });
    stage.addEventListener("pointermove",event=>{
        if (compact.matches || !pointerAllowed.matches || reducedMotion.matches || event.pointerType!=="mouse") return;
        point={x:event.clientX,y:event.clientY};
        if (!frame) frame=requestAnimationFrame(()=>{
            frame=0;const rect=stage.getBoundingClientRect();
            stage.style.setProperty("--service-light-x",(25+Math.max(0,Math.min(1,(point.x-rect.left)/rect.width))*50).toFixed(2)+"%");
            stage.style.setProperty("--service-light-y",(20+Math.max(0,Math.min(1,(point.y-rect.top)/rect.height))*60).toFixed(2)+"%");
        });
    },{passive:true});
    stage.addEventListener("pointerleave",resetLight,{passive:true});
    pointerAllowed.addEventListener("change",resetLight);
    compact.addEventListener("change",adapt);
    reducedMotion.addEventListener("change",resetLight);
    window.addEventListener("hashchange",()=>selectHash(true));
    section.dataset.showcaseReady="true";section.classList.add("showcase-enhanced");selector.hidden=false;
    adapt();selectHash(Boolean(location.hash));
}
initServicesShowcase();

function initProductionWorkflow() {
    const section = document.querySelector(".work-process");
    if (!section || section.dataset.workflowReady) return;
    const controls = section.querySelector(".workflow-controls");
    const hint = section.querySelector(".workflow-hint");
    const buttons = [...section.querySelectorAll(".workflow-controls button")];
    const panels = [...section.querySelectorAll(".workflow-panel")];
    if (!controls || !hint || buttons.length < 2 || buttons.length !== panels.length) return;
    const vertical = matchMedia("(max-width:900px)");
    let active = 0;

    function select(index) {
        active = index;
        section.style.setProperty("--workflow-progress", String(index / (buttons.length - 1)));
        buttons.forEach((button, i) => {
            button.setAttribute("aria-selected", String(i === index));
            button.tabIndex = i === index ? 0 : -1;
        });
        panels.forEach((panel, i) => {
            panel.classList.toggle("is-active", i === index);
            panel.inert = i !== index;
            panel.setAttribute("aria-hidden", String(i !== index));
        });
    }
    function adapt() {
        controls.setAttribute("aria-orientation", vertical.matches ? "vertical" : "horizontal");
    }

    controls.setAttribute("role", "tablist");
    buttons.forEach((button, i) => {
        button.setAttribute("role", "tab");
        button.addEventListener("click", () => select(i));
    });
    panels.forEach((panel, i) => {
        panel.setAttribute("role", "tabpanel");
        panel.setAttribute("aria-labelledby", buttons[i].id);
        panel.tabIndex = 0;
    });
    controls.addEventListener("keydown", event => {
        const arrows = vertical.matches ? ["ArrowUp", "ArrowDown"] : ["ArrowLeft", "ArrowRight"];
        if (![...arrows, "Home", "End"].includes(event.key)) return;
        const current = buttons.indexOf(document.activeElement);
        if (current < 0) return;
        event.preventDefault();
        event.stopPropagation();
        const next = event.key === "Home" ? 0 : event.key === "End" ? buttons.length - 1
            : (current + (event.key === arrows[1] ? 1 : -1) + buttons.length) % buttons.length;
        select(next);
        buttons[next].focus();
    });
    vertical.addEventListener("change", adapt);
    section.style.setProperty("--workflow-count", String(buttons.length));
    section.dataset.workflowReady = "true";
    section.classList.add("workflow-enhanced");
    controls.hidden = false;
    hint.hidden = false;
    adapt();
    select(active);
}
initProductionWorkflow();

function initPortfolioFilters() {
    const section = document.querySelector(".portfolio-page");
    if (!section) return;
    const buttons = [...section.querySelectorAll(".filter-btn")];
    const projects = section.querySelectorAll(".portfolio-card");
    buttons.forEach(button => button.addEventListener("click", () => {
        buttons.forEach(item => {
            item.classList.toggle("active", item === button);
            item.setAttribute("aria-pressed", String(item === button));
        });
        projects.forEach(project => {
            project.hidden = button.dataset.filter !== "all" && project.dataset.category !== button.dataset.filter;
        });
    }));
}
initPortfolioFilters();
