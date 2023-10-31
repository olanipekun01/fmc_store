
function handleNewSupp() {
    document.querySelector(".new_supp_container").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
}


function closeSuppModal() {
    event.preventDefault();
    document.querySelector(".new_supp_container").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}