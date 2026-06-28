// Socket.IO подключение
const socket = io();

// DOM элементы
const newRoomBtn = document.getElementById('3');
const createRoomForm = document.getElementById('2');
const notificationBell = document.getElementById('b11');
const notificationsPanel = document.getElementById('a33');

// Переключение формы создания комнаты
if (newRoomBtn) {
    newRoomBtn.addEventListener('click', function() {
        if (createRoomForm.style.display === 'none' || !createRoomForm.style.display) {
            createRoomForm.style.display = 'block';
        } else {
            createRoomForm.style.display = 'none';
        }
    });
}

// Переключение панели уведомлений
if (notificationBell) {
    notificationBell.addEventListener('click', function(e) {
        e.stopPropagation();
        if (notificationsPanel.style.display === 'block') {
            notificationsPanel.style.display = 'none';
        } else {
            notificationsPanel.style.display = 'block';
        }
    });
}

// Закрытие панелей при клике вне их
document.addEventListener('click', function(e) {
    if (notificationsPanel && 
        !notificationsPanel.contains(e.target) && 
        e.target !== notificationBell && 
        !notificationBell.contains(e.target)) {
        notificationsPanel.style.display = 'none';
    }
});

// Обработка форм приглашений
document.addEventListener('submit', function(e) {
    const form = e.target;
    
    // Проверяем, является ли форма формой приглашения
    if (form.action && form.action.includes('/not_panel/')) {
        e.preventDefault();
        
        // Получаем данные формы
        const formData = new FormData(form);
        const submitButton = e.submitter;
        
        // Определяем, какая кнопка была нажата
        const isAccept = submitButton && submitButton.name === 'ok';
        if(isAccept){
            formData.append('ok', 'ok')
        }
        // Отправляем AJAX-запрос
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                if (isAccept) {
                    // Если нажата кнопка "Принять", перенаправляем в комнату
                    const urlParts = form.action.split('/');
                    const roomId = urlParts[urlParts.length - 2]; // room_id из URL
                    
                    if (roomId) {
                        window.location.href = `/room/${roomId}`;
                    } else {
                        // Если не удалось получить ID комнаты, просто обновляем страницу
                        window.location.reload();
                    }
                } else {
                    // Если нажата кнопка "Отклонить", просто убираем уведомление
                    const notificationForm = form.closest('form');
                    if (notificationForm) {
                        notificationForm.style.transition = 'opacity 0.3s';
                        notificationForm.style.opacity = '0';
                        setTimeout(() => {
                            notificationForm.remove();
                            
                            // Проверяем, остались ли еще уведомления
                            const panel = document.getElementById('a33');
                            const remainingForms = panel.querySelectorAll('form');
                            if (remainingForms.length === 0) {
                                // Если уведомлений нет, закрываем панель
                                panel.style.display = 'none';
                            }
                        }, 300);
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

// Socket.IO для уведомлений
socket.on('note', function(data) {
    const [sender, roomId] = data;
    
    // Показываем уведомление
    showNotification(`${sender} приглашает вас в комнату #${roomId}`);
    
    // Обновляем страницу через 2 секунды
    setTimeout(() => {
        location.reload();
    }, 2000);
});

// Функция для показа уведомления
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
        border-left: 4px solid #667eea;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Добавляем стили для анимаций
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);
// Простой JavaScript для переключения видимости
document.addEventListener('DOMContentLoaded', function() {
    const newRoomBtn = document.getElementById('3');
    const createRoomForm = document.getElementById('2');
    const bellBtn = document.getElementById('b11');
    const notificationsPanel = document.getElementById('a33');
    
    // Переключение формы создания комнаты
    if (newRoomBtn) {
        newRoomBtn.addEventListener('click', function() {
            if (createRoomForm.classList.contains('active')) {
                createRoomForm.classList.remove('active');
            } else {
                createRoomForm.classList.add('active');
            }
        });
    }
    
    // Переключение панели уведомлений
    if (bellBtn) {
        bellBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (notificationsPanel.classList.contains('active')) {
                notificationsPanel.classList.remove('active');
            } else {
                notificationsPanel.classList.add('active');
            }
        });
    }
    
    // Закрытие панели уведомлений при клике вне её
    document.addEventListener('click', function(e) {
        if (notificationsPanel && 
            !notificationsPanel.contains(e.target) && 
            e.target !== bellBtn && 
            !bellBtn.contains(e.target)) {
            notificationsPanel.classList.remove('active');
        }
    });
    
    // Socket.IO для уведомлений (если используется)
    if (typeof io !== 'undefined') {
        const socket = io();
        socket.on('note', function(data) {
            const [sender, roomId] = data;
            alert(`${sender} invites you to join room #${roomId}`);
            setTimeout(() => {
                location.reload();
            }, 2000);
        });
    }
}); 