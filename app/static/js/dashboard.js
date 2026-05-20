document.addEventListener('DOMContentLoaded', function () {
    const stats = document.querySelectorAll('.stat-value');
    stats.forEach(stat => {
        const target = parseInt(stat.textContent, 10);
        if (!isNaN(target)) {
            let current = 0;
            const increment = Math.ceil(target / 30);
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                stat.textContent = current;
            }, 30);
        }
    });
});
