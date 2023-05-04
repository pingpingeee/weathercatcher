// 쿠키 설정 함수
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// 쿠키 가져오기 함수
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// 체크박스 상태에 따라 쿠키 설정
var rememberCheckbox = document.getElementById("remember");
var usernameInput = document.getElementById("account");
var passwordInput = document.getElementById("password");

if (rememberCheckbox.checked && usernameInput.value && passwordInput.value) {
    setCookie("account", usernameInput.value, 7);
    setCookie("password", passwordInput.value, 7);
} else {
    setCookie("account", "", -1);
    setCookie("password", "", -1);
}

// 페이지 로드 시 쿠키 가져와서 폼에 입력
window.onload = function () {
    var rememberedUsername = getCookie("account");
    var rememberedPassword = getCookie("password");
    if (rememberedUsername && rememberedPassword) {
        usernameInput.value = rememberedUsername;
        passwordInput.value = rememberedPassword;
        rememberCheckbox.checked = true;
    }
};