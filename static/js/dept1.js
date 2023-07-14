
function showModal(name) {
    document.getElementById("modalNameInput").value = name;
    document.querySelector(".modal_container").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
};

function closeModal() {
    event.preventDefault();
    document.querySelector(".modal_container").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}

function handleNewStock() {
    document.querySelector(".new_stock").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
}

function closeNewStockModal() {
    event.preventDefault();
    document.querySelector(".new_stock").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}

// document.getElementById("cancelBtn").addEventListener("click", function (event) {
//     event.preventDefault();
//     document.querySelector(".modal_container").style.display = "none";
// })