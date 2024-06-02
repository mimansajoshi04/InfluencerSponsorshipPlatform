function register(){
    cpassword = document.getElementById('confirm-password').value;
    password = document.getElementById('password').value;
    email = document.getElementById('email').value;
    username = document.getElementById('username').value;

    if(username.includes(" ")){
        alert("Username cannot contain spaces.");
        return false;

    }
    if(!(email.includes("@")) || !(email.includes("."))){
        alert("Email must be of the form: xyz@abc.com");
        return false;
    }

    if(password.length <8){
        alert("Length of password must be greater than or equal to 8.");
        return false;
    }

    if(password === cpassword){
        return true;
    }

    else{
        alert("Password and confirm password do not match. Try again!");
        return false;
    }
}

function login(){
    window.location.href = "/login";
}