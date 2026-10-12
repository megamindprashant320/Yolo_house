/*=========================================================
    YOLO HOUSE PRODUCTIONS
    MAIN.JS
    PART - 1
=========================================================*/

"use strict";

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

    const progressHeight=(window.scrollY/totalHeight)*100;

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

        behavior:"smooth"

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

const lazyImages=document.querySelectorAll("img");

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

img.style.transition=".7s";

imageObserver.observe(img);

});

/*=========================================================
    PARALLAX HERO
=========================================================*/

const hero=document.querySelector(".hero");

window.addEventListener("scroll",()=>{

const offset=window.pageYOffset;

if(hero){

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

if(e.key==="Home"){

window.scrollTo({

top:0,

behavior:"smooth"

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

if(!heroContent || !window.matchMedia("(min-width:993px) and (hover:hover) and (pointer:fine)").matches) return;

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
    RANDOM BACKGROUND PARTICLES
=========================================================*/

for(let i=0;i<35;i++){

const particle=document.createElement("span");

particle.className="particle";

particle.style.left=Math.random()*100+"%";

particle.style.animationDuration=

5+Math.random()*10+"s";

particle.style.animationDelay=

Math.random()*5+"s";

document.body.appendChild(particle);

}

/*=========================================================
    DISABLE IMAGE DRAG
=========================================================*/

document.querySelectorAll("img").forEach(img=>{

img.setAttribute("draggable","false");

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
