function toggle_nav_expand() {
    let nav = document.querySelector("body>nav");
    if(nav.classList.contains("expanded")) {
        nav.classList.remove("expanded");
    } else {
        nav.classList.add("expanded");
    }
}
