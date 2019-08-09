function scrollIfMoreContent() {
    const body = document.body;
    const html = document.documentElement;

    window.scrollBy(0, 10000);
    
    return Math.max(
        body.scrollHeight,
        body.offsetHeight,
        html.clientHeight,
        html.scrollHeight,
        html.offsetHeight
    );
}

return scrollIfMoreContent();
