let isFormBlocked = false;

function updateFormState() {
    const blockedUntil = localStorage.getItem('formBlockedUntil');
    const submitBtn = document.querySelector('#form-place-an-order .submit-btn');
    
    if (blockedUntil && Date.now() < parseInt(blockedUntil)) {
        isFormBlocked = true;
        const secondsLeft = Math.ceil((parseInt(blockedUntil) - Date.now()) / 1000);
        const minutes = Math.floor(secondsLeft / 60);
        const seconds = secondsLeft % 60;
        
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = `Ждите ${minutes}:${seconds.toString().padStart(2, '0')}`;
            submitBtn.style.opacity = '0.6';
            submitBtn.style.cursor = 'not-allowed';
        }
    } else {
        isFormBlocked = false;
        localStorage.removeItem('formBlockedUntil');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Отправить';
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
        }
    }
}

async function send_order() {
    updateFormState();

    document.getElementById('form-place-an-order').addEventListener('submit', async event => {
        event.preventDefault();

        const productName = localStorage.getItem('selectedProductName') || 'Не указан';
        const formData = new FormData();

        formData.append('username', document.getElementById('user-name').value);
        formData.append('phone', document.getElementById('number-phone').value);
        formData.append('email', document.getElementById('email').value);
        formData.append('comment', document.getElementById('own_order').value);
        formData.append('product_name', productName);

        console.log('Отправляемые данные:');
        for (let [key, value] of formData.entries()) {
            console.log(key, value);
        }

        try {
            isFormBlocked = true;
            const blockUntil = Date.now() + 3 * 60 * 1000; 
            localStorage.setItem('formBlockedUntil', blockUntil.toString());
            updateFormState();

            const response = await fetch('/make-order', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (response.ok) {
                UIkit.notification({
                    message: '<p class="text-notification">Заказ успешно оформлен. Мы свяжемся с вами в ближайшее время. Следующий заказ можно будет отправить через 3 минуты.</p>',
                    status: 'success',
                    pos: 'top-center',
                    timeout: 10000
                });
                
                document.getElementById('requestOverlay').style.display = 'none';
                document.getElementById('requestPopup').style.display = 'none';
                
                document.getElementById('form-place-an-order').reset();
                localStorage.removeItem('selectedProductName');
                
            } else {
               
                isFormBlocked = false;
                localStorage.removeItem('formBlockedUntil');
                updateFormState();
                
                UIkit.notification({
                    message: 'Произошла ошибка: ' + (result.detail || 'попробуйте еще раз'),
                    status: 'danger',
                    pos: 'top-center',
                    timeout: 5000
                });
            }
        } catch (err) {
            console.error('Ошибка:', err);
        
            isFormBlocked = false;
            localStorage.removeItem('formBlockedUntil');
            updateFormState();
            
            UIkit.notification({
                message: 'Произошла ошибка сети, попробуйте еще раз',
                status: 'danger',
                pos: 'top-center',
                timeout: 5000
            });
        }
    });

}

function openOrderForm(productName) {
    localStorage.setItem('selectedProductName', productName);
    console.log('Сохранен товар:', productName);
    
    document.getElementById('requestOverlay').style.display = 'block';
    document.getElementById('requestPopup').style.display = 'block';
    
    send_order();
}


document.addEventListener('DOMContentLoaded', function() {
    updateFormState();
    setInterval(updateFormState, 1000);
});