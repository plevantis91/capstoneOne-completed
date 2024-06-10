// app.js


document.addEventListener('DOMContentLoaded', function() {
   
    document.getElementById("save-btn").addEventListener("click",function(e){
        e.preventDefault();
        axios.post("/like_recipe", { data: recipeData })
        .then(response => {
            if (response.data.msg === "Recipe already liked") {
                alert("You have already liked this recipe.");
            } else {
                alert("Recipe saved successfully");
                console.log("Recipe saved successfully", response.data);
            }
        })
        .catch(error => {
            console.error("Error saving recipe", error);
        
        })
    });
});



