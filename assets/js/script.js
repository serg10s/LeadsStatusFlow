document.addEventListener("DOMContentLoaded", function () {
    const starsContainer = document.querySelector(".stars");
    const numberOfStars = 121; // Количество точек

    for (let i = 0; i < numberOfStars; i++) {
        const star = document.createElement("div");
        star.classList.add("star");

        // Генерация случайных координат
        const randomTop = Math.random() * 100; // Случайное значение от 0% до 100%
        const randomLeft = Math.random() * 100; // Случайное значение от 0% до 100%

        // Установка позиции
        star.style.top = `${randomTop}%`;
        star.style.left = `${randomLeft}%`;

        // Добавление точки в контейнер
        starsContainer.appendChild(star);
    }
});

 document.addEventListener("DOMContentLoaded", function () {
    const infoBoxes = document.querySelectorAll('.info-box');
    const inner = document.querySelectorAll('.inner')
    // const formContainer = document.querySelector('.form-container');
    const logo = document.querySelector('.an');

    // Функция для проверки видимости элемента
    function isElementInViewport(el) {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        const windowWidth = window.innerWidth || document.documentElement.clientWidth;

        return (
            rect.top <= windowHeight &&
            rect.bottom >= 0 &&
            rect.left <= windowWidth &&
            rect.right >= 0
        );
    }

    // Дебаунсинг функции
    function debounce(func, wait = 5) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    let allInner = [...inner]
    function checkVisibility() {
        infoBoxes.forEach((box, index) => {
            if (isElementInViewport(box)) {

                if (!box.classList.contains('fully-visible')) {

                box.classList.add('animated');
                
                setTimeout(() => {
                    box.style.background = 'linear-gradient(435deg, #2c357a, #1c1c3a)';
                    box.style.boxShadow = '0 0 10px rgba(168, 66, 172, 0.8), 0 0 20px rgba(122, 255, 158, 0.8)';
                    allInner[index].style.background = 'linear-gradient(435deg, #2c357a, #1c1c3a)';

box.classList.remove('animated')
                }, 900);
                      
                      box.classList.add('fully-visible');
                }

            }
        });

        if (logo && isElementInViewport(logo)) {
            logo.classList.add('animated');
        }
    }

    const debouncedCheckVisibility = debounce(checkVisibility, 20);

    checkVisibility();
    window.addEventListener('scroll', debouncedCheckVisibility);
});


$(document).ready(function () {
var inputElements = document.querySelectorAll('input[type="tel"]');

            inputElements.forEach(function (input) {
                var iti = window.intlTelInput(input, {
                    autoPlaceholder: "aggressive",
                    geoIpLookup: function (callback) {
                        $.get("http://ipinfo.io", function () { }, "jsonp").always(
                            function (resp) {
                                var countryCode = resp && resp.country ? resp.country : "";
                                callback(countryCode);
                            }
                        );
                    },
                    // hiddenInput: "phone_number_hidden",
                    hiddenInput: "phone_number",


                    onlyCountries: ['JP'],
                    // onlyCountries: ['AT', 'BE', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'IS', 'IE', 'IT', 'LV', 'LI', 'LT', 'LU', 'MT', 'MC', 'NL', 'NO', 'PT', 'ES', 'SE', 'CH', 'GB', "UA"],
                    preferredCountries: ["JP"],
                    separateDialCode: true,
                    utilsScript:
                        "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/11.0.14/js/utils.js",
                });
    
                $(input).on("countrychange", function (event) {
                    var selectedCountryData = iti.getSelectedCountryData();
                    var newPlaceholder = intlTelInputUtils.getExampleNumber(
                        selectedCountryData.iso2,
                        true,
                        intlTelInputUtils.numberFormat.INTERNATIONAL
                    );
                    iti.setNumber("");
                    var mask = newPlaceholder.replace(/[1-9]/g, "0");
                    $(this).mask(mask);
                });
    
                iti.promise.then(function () {
                    $(input).trigger("countrychange");
                });
            });
        });
        
   
        function checkbtn(e) {
   
          var form = e.target;
          
          var submitButton = form.querySelector('button[type="submit"]');
          
          if (submitButton) {
              submitButton.disabled = true;
          }
          
            let obj = window.intlTelInputGlobals.getInstance(form.querySelector('input[type="tel"]'))
    
            if (!obj.isValidNumber()) {
                submitButton.disabled = false;
                return false
            }
          
        } 

//const apiKey = "ba67df6a-a17c-476f-8e95-bcdb75ed3958"
//localStorage.setItem("api_key", apiKey);
//
//document.addEventListener("submit", async function (e){
//    e.preventDefault()
//
//    try {
//        const response = await fetch("http://127.0.0.1:8000/send", {
//            method: "POST",
//            headers: {
//                "Content-Type": "application/json",
//                "Authorization": localStorage.getItem('api_key')
//            }
//        })
//        let result = await response.json()
//        console.log(result)
//
//    }
//    catch (error) {
//        console.log("Error: " + error.message)
//    }
//})
