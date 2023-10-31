function showFilterModal() {
    // document.querySelector(".issue_modal_container").style.display = "block";
    document.querySelector(".filter_container").style.display = "block";
};

function closeFilterModal() {
    event.preventDefault();
    document.querySelector(".filter_container").style.display = "none";
    // document.querySelector(".background_wrapper").style.display = "none";
}