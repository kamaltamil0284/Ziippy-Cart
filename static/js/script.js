
document.addEventListener("DOMContentLoaded", function () {
    const qtyInput = document.getElementById("ProQty");
    const btnPlus = document.getElementById("btnPlus");
    const btnMinus = document.getElementById("btnMinus");
    const cartProQty = document.getElementById("cartProQty");
    const buyProQty = document.getElementById("buyProQty");
    const cartForm = document.getElementById("cartForm");
    const paymentForm = document.getElementById("paymentForm");

    // Update both hidden fields
    function updateHiddenQty() {
        const qty = parseInt(qtyInput.value) || 1;
        cartProQty.value = qty;
        buyProQty.value = qty;
    }

    btnPlus.addEventListener("click", () => {
        let qty = parseInt(qtyInput.value) || 1;
        if (qty < 10) qtyInput.value = qty + 1;
        updateHiddenQty();
    });

    btnMinus.addEventListener("click", () => {
        let qty = parseInt(qtyInput.value) || 1;
        if (qty > 1) qtyInput.value = qty - 1;
        updateHiddenQty();
    });

    qtyInput.addEventListener("input", updateHiddenQty);

    // Just in case user submits without clicking +/-
    cartForm.addEventListener("submit", updateHiddenQty);
    paymentForm.addEventListener("submit", updateHiddenQty);
});
