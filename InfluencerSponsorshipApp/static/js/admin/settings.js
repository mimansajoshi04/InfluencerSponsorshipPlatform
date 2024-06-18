function edit(){
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

    return true;
}

function delete_account(){
    window.location.href = "/admin/delete_account";
}