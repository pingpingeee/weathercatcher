const loginButton = document.querySelector(".loginbox");
const container = document.querySelector('.container');
const logo = document.querySelector('.logo');
const loginbox = document.querySelector('.loginbox');
const box1 = document.querySelector('.box1');
const box2 = document.querySelector('.box2');

loginButton.addEventListener("click", function () {
    container.style.height = '680px';
    logo.style.position = 'absolute';
    logo.style.top = '0';

    loginbox.style.width = "275px";
    loginbox.top = -50;
    loginbox.textContent = '웨더캐쳐에 오신 것을 환영합니다!';
    loginbox.style.display = 'flex';
    loginbox.style.justifyContent = 'center';
    loginbox.style.alignItems = 'center';
    loginbox.classList.add('fade-out1');


    setTimeout(function () {
        box1.style.display = 'flex';
        box1.classList.add('fade-in');
        window.location.href = 'login';
    }, 1500)
});