const sliders = document.querySelectorAll('.product_slider');

sliders.forEach(slider => {
    const slides = slider.querySelectorAll('.slide');
    const prevBtn = slider.querySelector('.slider-prev');
    const nextBtn = slider.querySelector('.slider-next');

    let currentSlide = 0;


    function showSlide(index){
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
    }
    
    prevBtn.addEventListener('click', function(){
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    });
    
    nextBtn.addEventListener('click', function(){
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    });
    
    showSlide(currentSlide);
});