const pixelsPerScroll = 50;
const waitTimeMSPerScroll = 50;
const scrollsPerLazyScroll = 5000;
const scrollLimit = 10;

let scrollTimes = 0;

async function lazyScroll() {
    const body = document.body;
    const html = document.documentElement;

    // "Smooth" scroll to 10,000 over 10 seconds.
    let scrollCount = 0;
    while (scrollCount < scrollsPerLazyScroll) {
        scrollCount += pixelsPerScroll;
        await new Promise(resolve => setTimeout(() => {
            window.scrollBy(0, pixelsPerScroll);
            resolve();
        }, waitTimeMSPerScroll));
    }

    return Math.max(
        body.scrollHeight,
        body.offsetHeight,
        html.clientHeight,
        html.scrollHeight,
        html.offsetHeight
    );
}

function scrollForMoreContent(lastHeight = 0) {
    lazyScroll().then(currentHeight => {
        if ((window.pageYOffset + window.innerHeight != currentHeight || currentHeight != lastHeight) && scrollTimes < scrollLimit) {
            scrollForMoreContent(currentHeight);
        } else {
            const completedNode = document.createElement('div');
            completedNode.setAttribute("id", "pyproduct__scrolling-complete-node");
            document.body.appendChild(completedNode);
        }
    });
}

scrollForMoreContent();
return true;
