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
        "Public Figure":["Public Figure"]
    };

    // Function to update the options of the dependent select
    function updateDependentSelect() {
        var selectedValue = category.value;
        var options = optionsMap[selectedValue];

        // Clear existing options
        niche.innerHTML = '';

        var optionElement = document.createElement("option");
        optionElement.textContent = "Choose..";
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
    updateDependentSelect();

    // Add event listener to main select
    category.addEventListener("change", updateDependentSelect);

});

function finish(){
    category = document.getElementById("category");
    niche = document.getElementById("niche");
    followers = document.getElementById("followers");
    instaid = document.getElementById("instaid");

    if(category.value === "Choose..."){
        alert("Please choose a category");
        return false;
    }

    if(niche.value === "Choose.."){
        alert("Please select the niche");
        return false;
    }

    if(instaid.value.includes("@")){
        alert("Do not input the @ in instagram id!");
        return false;
    }

    if(followers.value === ""){
        alert("As you have not provided the number of followers, it is set to default as 0. This can be changed any time from settings in Dashboard.")
        followers.value = 0;
        return true;
    }

}