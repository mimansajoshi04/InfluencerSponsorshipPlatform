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

    category = document.getElementById("category").value;
    niche = document.getElementById("niche").value;

    if(category == "Choose..."){
        alert("Please choose the category.");
        return false;
    }

    if(niche == "Choose..."){
        alert("Please choose the niche.");
        return false;
    }
    return true;
}

function delete_account(){
    window.location.href = "/influencer/delete_account";
}

document.addEventListener("DOMContentLoaded", function() {
    var category = document.getElementById("category");
    var niche = document.getElementById("niche");

    // Define options for the dependent select based on the value of the main select
    var optionsMap = {
        "Arts and Entertainment": ["Storytelling", "Singer", "Dancer","Actor","Photographer","Video Editor"],
        "Business": ["Business", "Management", "Consultant"],
        "Designer": ["Graphic Designer", "Interior Designer", "Game Designer"],
        "Education": ["Commerce", "Science","Arts"],
        "Fashion and Beauty": ["Fashion Influencers", "Personal Stylists", "Hair Stylists"],
        "Finance": ["CA", "Consultant", "Tax Management"],
        "Health and Wellness": ["Aerobics", "Gym", "Meditation","Yoga"],
        "Technology": ["Tech Expert"],
        "Travel": ["Vlogger", "Blogger"],
        "Public Figure":["Public Figure","Politician"]
    };

    // Function to update the options of the dependent select
    function updateDependentSelect() {
        var selectedValue = category.value;
        var options = optionsMap[selectedValue];

        // Clear existing options
        niche.innerHTML = "";

        var optionElement = document.createElement("option");
        optionElement.textContent = "Choose...";
        niche.appendChild(optionElement);

        // Add new options
        if (options) {
            options.forEach(function(option) {
                var optionElement = document.createElement("option");
                optionElement.textContent = option;
                niche.appendChild(optionElement);
            });
        }
    }

    // Initial update of dependent select

    // Add event listener to main select
    category.addEventListener("change", updateDependentSelect);

});