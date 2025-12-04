document.addEventListener('DOMContentLoaded', function () {
    if (typeof UIkit === 'undefined') {
        console.error('UIkit не загружен');
        return;
    }

    const initProductForm = () => {
        try {
            const form = document.getElementById('create_product');
            const uploadInput = form.querySelector('input[type="file"][name="images"]');
            const previewContainer = document.getElementById('preview-container'); // исправлено
            const resetButton = form.querySelector('button[type="reset"]');

            if (!form || !uploadInput || !previewContainer || !resetButton) {
                throw new Error('Не все необходимые элементы формы найдены');
            }

            // Удаляем кастомную обработку UIkit, если она мешает
            if (uploadInput.hasAttribute('uk-form-custom')) {
                uploadInput.removeAttribute('uk-form-custom');
            }

            let selectedFiles = [];

            const createImagePreview = (file) => {
                return new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        const previewItem = document.createElement('div');
                        previewItem.className = 'uk-width-1-4';
                        previewItem.innerHTML = `
                            <div class="uk-card uk-card-small uk-card-default">
                                <div class="uk-card-media-top">
                                    <img src="${e.target.result}" alt="${file.name}" style="max-height: 100px; object-fit: cover;">
                                </div>
                                <div class="uk-card-body uk-padding-small">
                                    <p class="uk-text-small uk-text-truncate">${file.name}</p>
                                    <button class="uk-button uk-button-small uk-button-danger remove-image" type="button">
                                        <span uk-icon="trash"></span>
                                    </button>
                                </div>
                            </div>
                        `;

                        previewContainer.appendChild(previewItem);

                        previewItem.querySelector('.remove-image').addEventListener('click', () => {
                            previewItem.remove();
                            selectedFiles = selectedFiles.filter(f => f !== file);
                            updateFileInput();
                            UIkit.notification(`Изображение ${file.name} удалено`, { status: 'success' });
                        });

                        resolve();
                    };
                    reader.readAsDataURL(file);
                });
            };

            const updateFileInput = () => {
                const dataTransfer = new DataTransfer();
                selectedFiles.forEach(file => dataTransfer.items.add(file));
                uploadInput.files = dataTransfer.files;
            };

            uploadInput.addEventListener('change', async (event) => {
                try {
                    const files = Array.from(event.target.files);

                    const invalidFiles = files.filter(file => !file.type.startsWith('image/'));
                    if (invalidFiles.length > 0) {
                        UIkit.notification('Пожалуйста, загружайте только изображения', { status: 'danger' });
                        return;
                    }

                    for (const file of files) {
                        if (!selectedFiles.some(f => f.name === file.name && f.size === file.size)) {
                            selectedFiles.push(file);
                            await createImagePreview(file);
                        }
                    }

                    updateFileInput();
                } catch (error) {
                    console.error('Ошибка при обработке файлов:', error);
                    UIkit.notification('Ошибка при загрузке изображений', { status: 'danger' });
                }
            });

            resetButton.addEventListener('click', () => {
                previewContainer.innerHTML = '';
                selectedFiles = [];
                uploadInput.value = '';
            });

            form.addEventListener('submit', async function (event) {
                event.preventDefault();

                try {
                    // 1. Проверяем обязательные поля перед отправкой
                    const price = parseFloat(document.getElementById('price_product').value);
                    if (isNaN(price)) {
                        throw new Error('Укажите корректную цену');
                    }
                    if (selectedFiles.length > 0) {
                        selectedFiles.forEach((file, index) => {
                            formData.append('images', file);  // Важно: 'images' во множественном числе
                        });
                    }
                    // 2. Создаем FormData и добавляем все поля
                    const formData = new FormData(form);
                    // 3. Добавляем остальные поля с правильными типами
                    formData.append('name', document.getElementById('name_product').value);
                    formData.append('description', document.getElementById('description_product').value);
                    formData.append('specifications', document.getElementById('specifications_product').value);

                    // Числовые поля преобразуем явно
                    formData.append('price', parseFloat(document.getElementById('price_product').value).toString());

                    // Булево значение преобразуем правильно
                    formData.append('is_available', document.getElementById('is_available_product').checked.toString());

                    formData.append('advantages', document.getElementById('advantages_product').value || '');
                    // 6. Отладочный вывод
                    console.log('Отправляемые данные:');
                    for (let [key, value] of formData.entries()) {
                        console.log(key, value instanceof File ? value.name : value);
                    }

                    // 7. Отправка на сервер
                    const response = await fetch('/add_product_post', {
                        method: 'POST',
                        body: formData
                    });

                    // 8. Обработка ответа
                    if (!response.ok) {
                        const errorData = await response.json().catch(() => ({}));
                        throw new Error(errorData.detail || 'Ошибка сервера');
                    }

                    const result = await response.json();
                    UIkit.notification('Товар успешно добавлен!', { status: 'success' });

                    // 9. Очистка формы
                    form.reset();
                    previewContainer.innerHTML = '';
                    selectedFiles = [];

                } catch (error) {
                    console.error('Ошибка:', error);
                    UIkit.notification(error.message, {
                        status: 'danger',
                        timeout: 5000
                    });
                }
            });

        } catch (error) {
            console.error('Ошибка инициализации формы:', error);
            UIkit.notification('Ошибка загрузки формы добавления товара', { status: 'danger' });
        }
    };


    // Инициализация всех компонентов
    const initAll = () => {
        initProductForm();
    };

    initAll();
});


