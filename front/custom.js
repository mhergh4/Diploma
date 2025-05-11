$(document).on("click", ".product-link", function (event) {
    console.log("[DEBUG] Element clicked:", this);

    const productName = $(this).attr("data-product-name") || $(this).attr("data-title");
    const productBrand = $(this).attr("data-product-brand") || $(this).attr("data-brand");

    if (!productName || !productBrand) {
        const parent = $(this).closest(".product-card");
        productName = productName || parent.find("[data-product-name], [data-title]").attr("data-product-name") || parent.find("[data-product-name], [data-title]").attr("data-title");
        productBrand = productBrand || parent.find("[data-product-brand], [data-brand]").attr("data-product-brand") || parent.find("[data-product-brand], [data-brand]").attr("data-brand");
    }

    if (!productName || !productBrand) {
        console.error("[ERROR] Can't get product_name or product_brand!", this);
        return;
    }

    const productData = {
        product_name: productName,
        product_brand: productBrand
    };

    console.log("[DEBUG] Sending product_click:", productData);

    $.ajax({
        url: "/product_click",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(productData),
        success: function (response) {
            console.log("[SUCCESS] Data was successfully sent:", response);
        },
        error: function (xhr, status, error) {
            console.error("[ERROR] Error while sending data:", status, error);
            console.log("[DEBUG] Server response:", xhr.responseText);
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    let buttons = document.querySelectorAll('.add-to-cart');

    buttons.forEach(button => {
        button.addEventListener('click', async function () {
            console.log("[DEBUG] Button clicked!", this);

            if (this.disabled) return;

            const data = {
                title: this.getAttribute("data-title"),
                price: parseFloat(this.getAttribute("data-price")) || 0,
                image_url: this.getAttribute("data-image-url"),
                link: this.getAttribute("data-link"),
                brand: this.getAttribute("data-brand"),
                description: this.getAttribute("data-description")
            };

            console.log("[DEBUG] Sending data:", data);

            this.disabled = true;
            this.innerText = "Adding...";
            this.classList.remove('btn-primary');
            this.classList.add('btn-secondary');

            try {
                const response = await fetch('/add_to_cart', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const responseData = await response.json();
                console.log("[DEBUG] Server response:", responseData);

                if (responseData.status === "success") {
                    this.innerText = "Added";
                } else {
                    this.disabled = false;
                    this.innerText = "Add to Cart";
                    this.classList.remove('btn-secondary');
                    this.classList.add('btn-primary');
                    alert("Error: " + responseData.message);
                }
            } catch (error) {
                console.error("[ERROR] Request error:", error);
                this.disabled = false;
                this.innerText = "Add to Cart";
                this.classList.remove('btn-secondary');
                this.classList.add('btn-primary');
                alert("An error occurred, please try again later.");
            }
        });
    });
});



const observer = new MutationObserver(mutations => {
    console.log("[DEBUG] DOM changes detected.");
});
observer.observe(document.body, { childList: true, subtree: true });



function toggleFilters() {
    var filterContainer = document.getElementById("filter-container");
    var overlay = document.getElementById("overlay");

    if (filterContainer.classList.contains("open")) {
        filterContainer.classList.remove("open");
        overlay.classList.remove("show");

        setTimeout(() => {
            overlay.style.display = "none";
        }, 300);
    } else {
        filterContainer.classList.add("open");
        overlay.style.display = "block";
        setTimeout(() => {
            overlay.classList.add("show");
        }, 10);
    }
}

document.querySelectorAll(".carousel a").forEach(function(brandLink) {
    brandLink.addEventListener("click", function(event) {
        event.stopPropagation();
        window.open(this.href, '_blank');
    });
});