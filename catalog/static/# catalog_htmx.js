htmx.on("htmx:beforeSwap", (e) => {
    if (e.detail.xhr.status === 401) {
        window.location.replace("/auth");
    }
});
