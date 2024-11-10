document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        const messages = document.querySelectorAll('.message-container .alert');
        messages.forEach(message => {
            message.style.transition = "opacity 0.5s ease";
            message.style.opacity = "0";
            setTimeout(() => message.remove(), 500);  
        });
    }, 3000);  
});