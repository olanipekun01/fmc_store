
function showIssueModal(name) {
    document.getElementById("modalNameInput").value = name;
    document.querySelector(".issue_modal_container").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
};

function showSupplierModal(name) {
    document.getElementById("modalNameInput").value = name;
    document.querySelector(".supplier_modal_container").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
};

function closeIssueModal() {
    event.preventDefault();
    document.querySelector(".issue_modal_container").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}

function closeSupplierModal() {
    event.preventDefault();
    document.querySelector(".supplier_modal_container").style.display = "none";
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


function showFilterModal() {
    // document.querySelector(".issue_modal_container").style.display = "block";
    document.querySelector(".filter_container").style.display = "block";
};

function closeFilterModal() {
    event.preventDefault();
    document.querySelector(".filter_container").style.display = "none";
    // document.querySelector(".background_wrapper").style.display = "none";
}

// document.getElementById("cancelBtn").addEventListener("click", function (event) {
//     event.preventDefault();
//     document.querySelector(".modal_container").style.display = "none";
// })