//Ejecutar función en el evento click
document.getElementById("btn-open").addEventListener("click", openCloseMenu);

//Declaramos variables
var sideMenu = document.getElementById("menu-side");
var body = document.getElementById("body");

//Evento para mostrar y ocultar menú
    function openCloseMenu(){
        body.classList.toggle("body-move");
        sideMenu.classList.toggle("menu-side-move");
    }

//Si el ancho de la página es menor a 760px, ocultará el menú al recargar la página

if (window.innerWidth < 760){

    body.classList.add("body-move");
    sideMenu.classList.add("menu-side-move");
}

//Haciendo el menú responsive(adaptable)

window.addEventListener("resize", function(){

    if (window.innerWidth > 760){

        body.classList.remove("body-move");
        sideMenu.classList.remove("menu-side-move");
    }

    if (window.innerWidth < 760){

        body.classList.add("body-move");
        sideMenu.classList.add("menu-side-move");
    }

});