const pixelsPerScroll = 100;
const waitTimeMSPerScroll = 100;
const scrollsPerLazyScroll = 10000;

async function lazyScroll() {
    const body = document.body;
    const html = document.documentElement;

    // "Smooth" scroll to 10,000 over 10 second.
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

function scrollMoreContent(lastHeight = 0) {
    lazyScroll().then((currentHeight) => {
        if (currentHeight != lastHeight && scrollTimes < scrollLimit) {
            scrollMoreContent(currentHeight);
        }
    });
}

return scrollMoreContent(0);
