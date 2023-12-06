const carousel = new bootstrap.Carousel('#myCarousel')

const myCarouselElement = document.querySelector('#myCarousel')

 carousel = new bootstrap.Carousel(myCarouselElement, {
  interval: 2000,
  touch: false
})





function set_second(first_select, name){
    
    const secondSelect = document.getElementById(name +'_second_select');


    selectedValue = parseInt(first_select.value);
    secondSelect.innerHTML = '';

    for (let j = selectedValue ; j < 19; j++) {
        const option = document.createElement('option');
        option.value = j;
        option.textContent = j;
        secondSelect.appendChild(option);
        
    }
    
}


// function show_form(){
//     const formOpenBtn = document.querySelector('#form-open'),
//     home = document.querySelector(".home"),
//     formContainer = document.querySelector(".form_container"),
//     formCloseBtn = document.querySelector(".form_close"),
//     loginBtn = document.querySelector("#login"),
//     signupBtn = document.querySelector("#signup"),
//     pwShowHide = document.querySelectorAll(".pw_hide");



//     home.classlist.add("show"); 
//     formCloseBtn.addEventListener("click",() => home.classlist.remove("show"));

// }