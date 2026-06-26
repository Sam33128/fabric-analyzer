// ---------------------------
// Image Preview
// ---------------------------

function previewImage(event){

    const preview =
        document.getElementById("preview");

    preview.src =
        URL.createObjectURL(
            event.target.files[0]
        );

    preview.style.display = "block";

}


// ---------------------------
// Loading Screen
// ---------------------------

function showLoader(){

    document
        .getElementById("loader")
        .style.display = "block";

}


// ---------------------------
// Drag & Drop
// ---------------------------

const dropZone =
    document.querySelector(".drop-zone");

const input =
    document.getElementById("fileInput");

if(dropZone){

dropZone.addEventListener(
"dragover",

function(e){

e.preventDefault();

dropZone.style.background="#FFF1C4";

});

dropZone.addEventListener(
"dragleave",

function(){

dropZone.style.background="#FFFDF7";

});

dropZone.addEventListener(
"drop",

function(e){

e.preventDefault();

input.files=e.dataTransfer.files;

previewImage(
{
target:input
}
);

dropZone.style.background="#FFFDF7";

});

} 