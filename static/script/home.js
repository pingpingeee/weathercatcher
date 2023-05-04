const menu = document.getElementById("menu");
const menuContainer = document.querySelector(".menu-container");
// menuhome 요소 선택
var menuhome = document.getElementById("menuhome");

// 현재 페이지 URL에서 파일명 추출
var url = window.location.href;
var filename = url.substring(url.lastIndexOf("/") + 1);

let menuOpen = false;
menuContainer.style.opacity = 0;

// 만약 현재 페이지가 home.html이면
if (filename === "home") {
    // menuhome 요소의 색상 변경
    menuhome.style.color = "rgb(31, 129, 146)";
    menuhome.style.textShadow = "0 5px 10px rgba(0, 0, 0, 0.3)";
}


menu.addEventListener("click", () => {
    if (menuOpen) {
        //메뉴 내려갈때
        menuContainer.style.animation = "menuClose 2s forwards";
        menuContainer.style.transition = "opacity 5s ease-in-out";
        menuContainer.style.opacity = 0;
        menuOpen = false;

        setTimeout(function () {
            menu.style.transition = "margin-top 0.5s ease-in-out, transform 0.5s ease-in-out";
            menu.style.marginTop = '550px';
            menu.classList.remove("fa-angle-double-down");
            menu.classList.add("fa-angle-double-up");
            menuContainer.style.display = "none";
            menu.style.animation = "";
        }, 100)
    } else {
        //메뉴 올라올때
        menuOpen = true;
        menu.style.marginTop = '280px';
        menu.classList.remove("fa-angle-double-up");
        menu.classList.add("fa-angle-double-down");
        menu.style.transition = "margin-top 0.5s ease-in-out, transform 0.5s ease-in-out";

        setTimeout(function () {
            menuContainer.style.display = "block";
            menuContainer.style.animation = "menuOpen .5s forwards";    //메뉴올라오는거
            menuContainer.style.transition = "opacity 0.5s ease-in-out";//페이드인하면서
            menuContainer.style.opacity = 1;
            menu.style.animation = "blink 1.5s infinite";
        }, 100)
    }
});

