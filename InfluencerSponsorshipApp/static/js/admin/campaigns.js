document.addEventListener("DOMContentLoaded", function() {
    var filterbychoice = document.getElementById("filterbychoice");
    var filterbyvalue = document.getElementById("filterbyvalue");

    var optionsMap = {
        "category": ["Arts and Entertainment","Business","Designer","Education","Fashion and Beauty","Finance","Health and Wellness","Public Figure","Technology","Travel"],
        "visibility": ["public","private"],
        "isflagged": ["flagged","not flagged"],
        "status":["on going","finished","scheduled"]
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
            window.onload = '/admin/campaigns';
        }
    });

    formUsername.addEventListener("submit",function(event){
        event.preventDefault();
        var usernameSearch = document.getElementById("name");
        console.log(filterbyvalue.value);
    
        if(usernameSearch.value===""){
            alert("Input an username to search by filter.");
            return false;
        }

        else{
            formUsername.submit();
            window.onload = '/admin/campaigns';
        }
    });

    formNiche.addEventListener("submit",function(event){
        event.preventDefault();
        var n = document.getElementById("n");
        console.log(filterbyvalue.value);
    
        if(n.value===""){
            alert("Input niche to search by filter.");
            return false;
        }

        else{
            formNiche.submit();
            window.onload = '/amin/campaigns';
        }
    });
});



function ad_requests(){
    document.addEventListener("click",function(event){
        btn = event.target.id;
        window.location.href = "/admin/ad_requests/" + btn;
    });
    
}

function flag_campaign(){
    document.addEventListener("click",function(event){
        btn = event.target.id;
        window.location.href = '/admin/flag_campaign/' + btn;
    });
}

function unflag_campaign(){
    document.addEventListener("click",function(event){
        btn = event.target.id;
        window.location.href = '/admin/unflag_campaign/' + btn;
    });
}

function reload(){
    window.location.href = "/admin/campaigns"
}
