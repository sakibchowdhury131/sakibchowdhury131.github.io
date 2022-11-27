
// Get the img object using its Id
img = document.getElementsByClassName("card");
flag = 0;
// Function to increase image size
function enlargeImg() {
    // Set image size to 1.5 times original
    if (flag == 0){
    img.style.transform = "scale(1.5)";
    // Animation effect
    img.style.transition = "transform 0.25s ease";
    flag = 1;
    } else {
    // Set image size to original
    img.style.transform = "scale(1)";
    img.style.transition = "transform 0.25s ease";
    flag = 0;
    }
    
    
    
}
// Function to reset image size
function resetImg() {
    // Set image size to original
    img.style.transform = "scale(1)";
    img.style.transition = "transform 0.25s ease";
}
