
function swipeRight() {
    alert("Followed!");
    current = document.getElementsByClassName("newfriend")[0];
    current.style.left = "2000px";
}

function swipeLeft() {
    alert("Ignored...");
    current = document.getElementsByClassName("newfriend")[0];
    current.style.right = "2000px";
}