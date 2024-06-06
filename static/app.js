// app.js


document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to the refresh button
    document.getElementById('refreshButton').addEventListener('click', function() {
        location.reload();  // Reload the current page
    });
    document.getElementById("save-btn").addEventListener("click",function(e){
        e.preventDefault();
        axios.post("like_recipe", { data: recipeData })
        .then(response => {
            console.log("Recipe saved successfully", response.data);
        })
        .catch(error => {
            console.error("Error saving recipe", error);
        
        })
    });
});

