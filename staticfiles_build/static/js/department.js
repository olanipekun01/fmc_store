
function handleNewDept() {
    document.querySelector(".new_dept_container").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
}


function closeDeptModal() {
    event.preventDefault();
    document.querySelector(".new_dept_container").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}