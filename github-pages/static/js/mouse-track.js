/*
 Mouse movement jiggle layers.

 - on mouse move
 - Track distance from center
 - offset layer position
    - relative to z-index for parallax.
*/

console.log('mouse-track.js loaded');

// layers to track mouse movement
const layers = {
    sun: {
        zIndex: 1,
        offsetX: 0,
        offsetY: 0,
        selector: '.sun',
        multiplier: -1.5
    }
    , 
    dog: {
        zIndex: 2,
        offsetX: 0,
        offsetY: 0,
        selector: '.dog-container',
        multiplier: 1.7
    }
}

// Thing to track the center center
const center_layer = {
    selector: '.dog-container',
}

const mousePosition = {
    x: 0,
    y: 0
};

document.addEventListener('mousemove', (event) => {
    const deltaX = event.clientX ;
    const deltaY = event.clientY ;

    mousePosition.x = deltaX;
    mousePosition.y = deltaY;
});

const getCenter = () => {
    const element = document.querySelector(center_layer.selector);
    const rect = element.getBoundingClientRect();
    return {
        x: rect.left + rect.width / 2,
        y: rect.top + rect.height / 2
    };
};

var tick = 0;
function updateLayers() {
    // Iter each layer,
    // Get offset. 
    // Apply transformations.
    tick++;

    if(tick % 10 == 0) {
        shuffleLayers();
    }

    requestAnimationFrame(updateLayers);
}

const shuffleLayers = () => {

    let mp = mousePosition;
    // console.log('tick')
    let center = getCenter()
    for (const key in layers) {
        const layer = layers[key];
        const element = document.querySelector(layer.selector);
        
        const offsetX = mp.x - center.x;
        const offsetY = mp.y - center.y;
        const x = (offsetX * layer.multiplier * .01).toFixed(0)
        const y = (offsetY * layer.multiplier * .01).toFixed(0)
        element.style.transform = `translate(${x}px, ${y}px)`
    }
}

const shuffleLayersRelVersion = () => {

    let mp = mousePosition;
    // console.log('tick')
    let center = getCenter()
    for (const key in layers) {
        const layer = layers[key];
        const element = document.querySelector(layer.selector);
        
        const offsetX = mp.x - center.x;
        const offsetY = mp.y - center.y;
        const x = (offsetX * layer.multiplier * .01).toFixed(0)
        const y = (offsetY * layer.multiplier * .01).toFixed(0)
        // let s =  `left=${x}px top=${y}px`
        element.style.top = `${y}px`
        element.style.left = `${x}px`
    }
}

requestAnimationFrame(updateLayers);
