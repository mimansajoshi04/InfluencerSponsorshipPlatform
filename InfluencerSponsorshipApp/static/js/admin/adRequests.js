document.addEventListener("DOMContentLoaded", function() {
    var filterbychoice = document.getElementById("filterbychoice");
    var filterbyvalue = document.getElementById("filterbyvalue");

    var optionsMap = {
        "category": ["Arts and Entertainment","Business","Designer","Education","Fashion and Beauty","Finance","Health and Wellness","Public Figure","Technology","Travel"],
        "visibility": ["public","private"],
        "isflagged": ["flagged","not flagged"],
        "status":["pending","rejected","accepted"],
        "deleted":["deleted","not deleted"]
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
            window.onload = '/admin/adRequests';
        }
    });

    formUsername.addEventListener("submit",function(event){
        event.preventDefault();
        var start = document.getElementById("start").value;
        var end = document.getElementById("end").value;

        if(parseInt(start)<=0){
            alert("Invalid payment amount!");
            return false;
        }

        if(parseInt(end)<=0){
            alert("Invalid payment amount!");
            return false;
        }

    
        if(parseInt(start)>parseInt(end)){
            alert("Invalid payment range!");
            return false;
        }

        else{
            formUsername.submit();
            window.onload = '/admin/adRequests';
        }
    });
});


