// Todo: Tooltips JS
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

function submitForm(event) {
    // Form Validation
    const form = document.querySelector("form")
    form.classList.add("was-validated")
    if (!form.checkValidity()) {
        console.log("Form is not valid")
        return
    }

    // Form Submission
    document.querySelector(".loader").classList.remove("d-none")
    const email = document.querySelector("input[name='email']").value,
        storeUrl = document.querySelector("input[name='storeUrl']").value

    // Async Request
    fetch(`${window.location.origin}/shopify/scrape`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "email": email,
            "storeUrl": storeUrl
        })
    }).then((response) => {
        return response.json()
    }).then((data) => {
        document.querySelector(".loader").classList.add("d-none")
        document.querySelector("#actionButtons").classList.remove("d-none")
        document.querySelectorAll("#actionButtons ul a").forEach(element => {
            element.href = element.href.replace("-1", data.id)
        });

        // update preview table
        document.getElementById("modalRecords").innerHTML = data.total
        document.getElementById("modalSite").innerHTML = data.url
        const tableContent = data?.products.map((product, index) => {
            return `<tr>
                <td>${index + 1}</td>
                <td>${product.title} <a href="${data.url}/products/${product.handle}" target="_blank"><i class="fa-solid fa-up-right-from-square"></i></a></td>
                <td>${product.images.length}</td>
                <td>${product.created_at && new Date(product.created_at).toDateString()}</td>
            </tr>`
        })
        document.querySelector("#dataPreviewTable>tbody").innerHTML = tableContent.join("")
    })
}