var niche_list=[];
function edit(){
    start = document.getElementById("start_date").value;
    end = document.getElementById("end_date").value;

    d1 = new Date(start);
    d2 = new Date(end);

    if(isNaN(d1)){
      alert("Invalid start date");
      return false;
    }
    if(isNaN(d2)){
      alert("Invalid end date");
      return false;
    }

    diff = d2.getTime()-d1.getTime();
    if(diff<=0){
      alert("End date should be after start date");
      return false;
    }

    category = document.getElementById("category");
    if(category.value=="Choose..."){
      alert("Please choose the category.")
      return false;
    }

    visibility = document.getElementById("visibility");
    if(visibility.value=="Choose..."){
      alert("Please choose the visibility.")
      return false;
    }

    industry = document.getElementById("industry");
    if(industry.value=="Choose..."){
      alert("Please choose the industry.")
      return false;
    }

    if(niche_list.length==0){
      alert("Please select the niche.");
      return false;
    }

    document.getElementById("join").value = niche_list.join(",");
    return true;
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
    niche.innerHTML = '';
    niche_list=[];

    // Add new options
    if (options) {
        options.forEach(function(option) {
            var optionContainer = document.createElement("div");
                
                var optionCheckbox = document.createElement("input");
                optionCheckbox.setAttribute("type", "checkbox");
                optionCheckbox.setAttribute("id", option);
                optionCheckbox.setAttribute("name", "niche");
                optionCheckbox.setAttribute("value", option);

                var optionLabel = document.createElement("label");
                optionLabel.setAttribute("for", option);
                optionLabel.textContent = option;

                optionContainer.appendChild(optionCheckbox);
                optionContainer.appendChild(optionLabel);

                niche.appendChild(optionContainer);
        });
    }
}

// Initial update of dependent select
updateDependentSelect();

// Add event listener to main select
category.addEventListener("change", updateDependentSelect);

});

document.addEventListener("DOMContentLoaded",function(){


  niche.addEventListener("click",function(event){
    if(event.target.type === "checkbox"){
      if(event.target.checked){
        niche_list.push(event.target.value);
        console.log(niche_list);
      }
      else{
        index = niche_list.indexOf(event.target.value);
        console.log(index);
        niche_list.splice(index,1);
        console.log(niche_list);
      }
    }
  });
});