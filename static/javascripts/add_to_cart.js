document.addEventListener("DOMContentLoaded", () => {
    const cartButtons = document.querySelectorAll(".btn-add-to-cart");

    cartButtons.forEach(button => {
        button.addEventListener("click", () => {
            const catalog_book_id = button.dataset.catalog_book_id;

            if (button.dataset.in_cart === "true") {
                window.location.href = "/cart";
                return;
            }

            console.log(JSON.stringify({ catalog_book_id: catalog_book_id }));

            fetch("/catalog", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ catalog_book_id: catalog_book_id })
            })
            .then(response => {
                if (response.status == 201) {
                    button.textContent = "Оформить";
                    button.classList.replace("btn-primary", "btn-success");
                    button.dataset.inCart = "true";
                } else {
                    /*location.reload()*/;
                }
            });
        });
    });
});
