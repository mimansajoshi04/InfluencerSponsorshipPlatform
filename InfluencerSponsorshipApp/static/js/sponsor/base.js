function logout(){
    window.location.href = '/logout';
}

function getToDashboard(){
    window.location.href = '/sponsor/dashboard';
}

function adRequests(){

}

function campaigns(){

}

function messages(){
    window.location.href = "/sponsor/messages";
}

function settings(){
    window.location.href = "/sponsor/settings";
}


document.addEventListener("DOMContentLoaded",function(){
    
    send_flag_request.addEventListener("submit",function(event){
        event.preventDefault();
        id = document.getElementById("send_flag_request");
        id.submit();
        window.onload = "/sponsor/dashboard";
        return;

    });

});


document.addEventListener("DOMContentLoaded", function() {

    const toast = document.getElementById("toast");

    toast.classList.add("show");

    setTimeout(function() {
        toast.classList.remove("show");
    }, 3000); 
});