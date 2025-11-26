const mainRequestBtn = document.querySelectorAll('.btn_send');

const formPopup = document.getElementById('requestPopup');
const formOverlay = document.getElementById('requestOverlay');
const formCloseBtn = document.querySelector('.close-popup');

mainRequestBtn.forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        formPopup.classList.add('active');
        formOverlay.classList.add('active');
    })
})

function formClosePopup(){
    formPopup.classList.remove('active');
    formOverlay.classList.remove('active');
}

formCloseBtn.addEventListener('click', formClosePopup);
formOverlay.addEventListener('click', formClosePopup);

document.addEventListener('keydown',function(e){
    if(e.key === 'Escape') formClosePopup();
});
