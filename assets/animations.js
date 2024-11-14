document.addEventListener('DOMContentLoaded', function() {
    const fadeInElements = document.querySelectorAll('.fade-in-text, .fade-in-element, .fade-in-card');
    fadeInElements.forEach(element => {
        element.style.opacity = 0;
        element.style.transform = 'translateY(20px)';
        setTimeout(() => {
            element.style.transition = 'opacity 2s, transform 2s';
            element.style.opacity = 1;
            element.style.transform = 'translateY(0)';
        }, 100);
    });

    const zoomInImages = document.querySelectorAll('.zoom-in-image');
    zoomInImages.forEach(image => {
        image.style.transform = 'scale(0.5)';
        setTimeout(() => {
            image.style.transition = 'transform 1s';
            image.style.transform = 'scale(1)';
        }, 100);
    });
});