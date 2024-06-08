function logout(){
    window.location.href = '/logout';
}

function getToDashboard(){
    window.location.href = '/admin/dashboard';
}

function user_management(){
    window.location.href = '/admin/user_management';
}

function settings(){
    window.location.href = '/admin/settings';
}

function see_messages(){
    window.location.href = '/admin/messages';
}

document.addEventListener("DOMContentLoaded", function() {

    const toast = document.getElementById("toast");

    toast.classList.add("show");

    setTimeout(function() {
        toast.classList.remove("show");
    }, 3000); 
});

