const menubar = document.querySelector('.header-top i')
menubar.addEventListener("click", function(){
    document.querySelector('.header-top ul').classList.toggle('active')
})
