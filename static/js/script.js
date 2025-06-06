document.addEventListener('DOMContentLoaded', function() {
    // Glitch effect on header
    const header = document.querySelector('h1');
    if (header) {
        setInterval(() => {
            if (Math.random() > 0.7) {
                header.classList.add('glitch');
                setTimeout(() => {
                    header.classList.remove('glitch');
                }, 300);
            }
        }, 5000);
    }
    
    // Terminal scan line animation
    const terminalLine = document.querySelector('.terminal-line');
    if (terminalLine) {
        setInterval(() => {
            terminalLine.style.animation = 'none';
            setTimeout(() => {
                terminalLine.style.animation = 'terminal-line 4s linear infinite';
            }, 10);
        }, 4000);
    }
    
    // Book hover effects
    const books = document.querySelectorAll('.book-card');
    books.forEach(book => {
        book.addEventListener('mouseenter', () => {
            book.style.boxShadow = '0 5px 25px rgba(0, 255, 65, 0.4)';
        });
        
        book.addEventListener('mouseleave', () => {
            book.style.boxShadow = '';
        });
    });
    
    // Search functionality
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    
    if (searchInput && searchBtn) {
        searchBtn.addEventListener('click', function() {
            const searchTerm = searchInput.value.trim().toLowerCase();
            
            if (searchTerm) {
                const bookCards = document.querySelectorAll('.book-card');
                bookCards.forEach(card => {
                    const title = card.querySelector('.book-title').textContent.toLowerCase();
                    const author = card.querySelector('.book-author').textContent.toLowerCase();
                    const desc = card.querySelector('.book-desc').textContent.toLowerCase();
                    const category = card.querySelector('.book-meta span:first-child').textContent.toLowerCase();
                    
                    if (title.includes(searchTerm) || 
                        author.includes(searchTerm) || 
                        desc.includes(searchTerm) || 
                        category.includes(searchTerm)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                });
            }
        });
    }
    
    // Flash message timeout
    const flashMessages = document.querySelectorAll('.flash-success, .flash-danger');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => {
                msg.style.display = 'none';
            }, 500);
        }, 5000);
    });
});