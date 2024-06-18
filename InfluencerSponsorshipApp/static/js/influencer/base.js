function logout(){
    window.location.href = '/logout';
}

function getToDashboard(){
    window.location.href = '/admin/dashboard';
}


function stats(){
    window.location.href = '/influencer/stats';
}

function settings(){
    window.location.href = '/influencer/settings';
}

function see_messages(){
    window.location.href = '/influencer/messages';
}

document.addEventListener("DOMContentLoaded", function() {

    const toast = document.getElementById("toast");

    toast.classList.add("show");

    setTimeout(function() {
        toast.classList.remove("show");
    }, 3000); 
});

