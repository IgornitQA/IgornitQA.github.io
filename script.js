// script.js
document.addEventListener('DOMContentLoaded', () => {
    // Плавная прокрутка
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Анимация текста
    const texts = ['QA Engineer', 'Тестировщик ПО'];
    let currentText = 0;
    let currentChar = 0;
    const animatedText = document.querySelector('.animated-text');

    function typeWriter() {
        if (currentChar < texts[currentText].length) {
            animatedText.textContent += texts[currentText].charAt(currentChar);
            currentChar++;
            setTimeout(typeWriter, 100);
        } else {
            setTimeout(eraseText, 2000);
        }
    }

    function eraseText() {
        if (currentChar > 0) {
            animatedText.textContent = texts[currentText].substring(0, currentChar-1);
            currentChar--;
            setTimeout(eraseText, 50);
        } else {
            currentText = (currentText + 1) % texts.length;
            setTimeout(typeWriter, 500);
        }
    }

    typeWriter();
});