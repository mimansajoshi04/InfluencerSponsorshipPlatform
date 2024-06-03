function finish(){
    industry = document.getElementById("industry");
    budget = document.getElementById("budget");

    console.log(industry.value);
    console.log(budget.value);

    if(industry.value === "Choose..."){
        alert("Please select the industry. You may change it later!");
        return false;
    }
    if(budget.value === ""){
        alert("Please add budget!");
        return false;
    }
    return true;
}