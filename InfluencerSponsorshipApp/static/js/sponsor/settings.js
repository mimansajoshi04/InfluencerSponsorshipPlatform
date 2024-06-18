document.addEventListener("submit",function(){
    edit.addEventListener("submit",function(event){
        if(event.target.id=="edit"){
            event.preventDefault();
            email = document.getElementById('email').value;
            username = document.getElementById('username').value;
        
            if(username.includes(" ")){
                alert("Username cannot contain spaces.");
                return false;
        
            }
            else if(!(email.includes("@")) || !(email.includes("."))){
                alert("Email must be of the form: xyz@abc.com");
                return false;
            
            }
        
            else{
                document.getElementById("edit").submit();
                window.onload="/sponsor/settings";
                return true;
            }
        }
        else{
            event.preventDefault();
        }
    });

});
function delete_account(){
    window.location.href = "/sponsor/delete_account";
}