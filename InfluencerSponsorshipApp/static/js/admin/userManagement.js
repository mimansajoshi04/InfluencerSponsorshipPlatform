document.addEventListener("DOMContentLoaded", function() {
    var filterbychoice = document.getElementById("filterbychoice");
    var filterbyvalue = document.getElementById("filterbyvalue");

    var optionsMap = {
        "userType" : ["admin","influencer","sponsor"],
        "isActive": ["active","inactive"],
        "isflagged": ["flagged","not flagged"]
    };

    function updateDependentSelect() {
        var selectedValue = filterbychoice.value;
        filterbyvalue.innerHTML = '';

        var defaultOption = document.createElement("option");
        defaultOption.textContent = "Choose..";
        defaultOption.value="Choose...";
        filterbyvalue.appendChild(defaultOption);

        var options = optionsMap[selectedValue];

            if (options) {
                options.forEach(function(option) {
                    var optionElement = document.createElement("option");
                    optionElement.textContent = option;

                    filterbyvalue.appendChild(optionElement);
                });
            }

    }

    updateDependentSelect();

    filterbychoice.addEventListener("change", updateDependentSelect);


    formSearchBy.addEventListener("submit",function(event){
        event.preventDefault();
        var filterbychoice = document.getElementById("filterbychoice");
        var filterbyvalue = document.getElementById("filterbyvalue");
        console.log(filterbyvalue.value);
        console.log(filterbychoice.value);
    
        if(filterbychoice.value==="Choose..."){
            alert("Choose an option to search by filter.");
            return false;
        }
    
        else if(filterbyvalue.value==="Choose..."){
            alert("Choose by which of the type you want to filter.");
            return false;
        }

        else{
            formSearchBy.submit();
            window.location.href = '/admin/user_management';
        }
    });

    formUsername.addEventListener("submit",function(event){
        event.preventDefault();
        var usernameSearch = document.getElementById("usernameSearch");
        console.log(filterbyvalue.value);
    
        if(usernameSearch.value===""){
            alert("Input an username to search by filter.");
            return false;
        }

        else{
            formUsername.submit();
            window.location.href = '/admin/user_management';
        }
    });
});


function reload(){
    window.location.href = '/admin/user_management';
}

function flag_user(){
    document.addEventListener("click",function(event){
        btn = event.target.id;
        window.location.href = '/admin/flag_user/' + btn;
    });
}

function unflag_user(){
    document.addEventListener("click",function(event){
        btn = event.target.id;
        window.location.href = '/admin/unflag_user/' + btn;
    });
}


function addUser(){
    window.location.href = "/admin/addUser";
}