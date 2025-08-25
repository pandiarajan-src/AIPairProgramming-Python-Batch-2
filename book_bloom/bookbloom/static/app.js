// BookBloom Frontend JavaScript

class BookBloomApp {
    constructor() {
        this.currentUser = null;
        this.authToken = localStorage.getItem('authToken');
        this.cart = [];
        this.books = [];
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.checkAuthStatus();
        this.loadBooks();
    }
    
    bindEvents() {
        // Navigation
        document.getElementById('home-link').addEventListener('click', (e) => {
            e.preventDefault();
            this.showPage('home-page');
            this.loadBooks();
        });
        
        document.getElementById('login-link').addEventListener('click', (e) => {
            e.preventDefault();
            this.showPage('login-page');
        });
        
        
        document.getElementById('profile-link').addEventListener('click', (e) => {
            e.preventDefault();
            if (this.authToken) {
                this.showPage('profile-page');
                this.loadUserProfile();
            } else {
                alert('Please login to view your profile');
                this.showPage('login-page');
            }
        });

        document.getElementById('cart-link').addEventListener('click', (e) => {
            e.preventDefault();
            if (this.authToken) {
                this.showPage('cart-page');
                this.loadCart();
            } else {
                alert('Please login to view your cart');
                this.showPage('login-page');
            }
        });
        
        document.getElementById('logout-link').addEventListener('click', (e) => {
            e.preventDefault();
            this.logout();
        });
        
        
        // Auth form switching
        document.getElementById('auth-switch-link').addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleAuthForm();
        });
        
        // Forms
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });
        
        document.getElementById('register-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleRegister();
        });
        
        
        // Search
        document.getElementById('search-btn').addEventListener('click', () => {
            this.performSearch();
        });
        
        document.getElementById('clear-search-btn').addEventListener('click', () => {
            document.getElementById('search-input').value = '';
            this.loadBooks();
        });
        
        document.getElementById('search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });
        
        // Cart actions
        document.getElementById('checkout-btn').addEventListener('click', () => {
            this.checkout();
        });
        
        document.getElementById('continue-shopping').addEventListener('click', (e) => {
            e.preventDefault();
            this.showPage('home-page');
        });
        
        // Modal
        document.getElementById('close-modal').addEventListener('click', () => {
            document.getElementById('checkout-modal').classList.add('hidden');
            this.showPage('home-page');
        });
    }
    
    async makeRequest(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (this.authToken) {
            defaultOptions.headers['Authorization'] = `Bearer ${this.authToken}`;
        }
        
        const response = await fetch(url, { ...defaultOptions, ...options });
        
        if (!response.ok) {
            let errorMessage = 'Request failed';
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || JSON.stringify(errorData);
            } catch (e) {
                // If response is not JSON, use status text
                errorMessage = response.statusText || `HTTP ${response.status}`;
            }
            throw new Error(errorMessage);
        }
        
        return response.json();
    }
    
    showPage(pageId) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        // Show selected page
        document.getElementById(pageId).classList.add('active');
        
        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        const linkId = pageId.replace('-page', '-link');
        const activeLink = document.getElementById(linkId);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }
    
    checkAuthStatus() {
        if (this.authToken) {
            this.showAuthenticatedState();
        } else {
            this.showUnauthenticatedState();
        }
    }
    
    showAuthenticatedState() {
        document.getElementById('login-link').classList.add('hidden');
        document.getElementById('profile-link').classList.remove('hidden');
        document.getElementById('logout-link').classList.remove('hidden');
        // Re-render books if they exist to update button states
        if (this.books.length > 0) {
            this.renderBooks();
        }
    }
    
    showUnauthenticatedState() {
        document.getElementById('login-link').classList.remove('hidden');
        document.getElementById('profile-link').classList.add('hidden');
        document.getElementById('logout-link').classList.add('hidden');
        // Re-render books if they exist to update button states
        if (this.books.length > 0) {
            this.renderBooks();
        }
    }
    
    async handleLogin() {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const errorDiv = document.getElementById('login-error');
        
        try {
            const response = await this.makeRequest('/api/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
            
            this.authToken = response.access_token;
            localStorage.setItem('authToken', this.authToken);
            this.showAuthenticatedState();
            this.showPage('home-page');
            this.renderBooks(); // Re-render books to update button states
            errorDiv.classList.add('hidden');
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.classList.remove('hidden');
        }
    }
    
    toggleAuthForm() {
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        const authTitle = document.getElementById('auth-title');
        const switchText = document.getElementById('auth-switch-text');
        const switchLink = document.getElementById('auth-switch-link');
        
        if (loginForm.classList.contains('hidden')) {
            // Switch to login
            loginForm.classList.remove('hidden');
            registerForm.classList.add('hidden');
            authTitle.textContent = 'Login';
            switchText.textContent = "Don't have an account?";
            switchLink.textContent = 'Register here';
            
            // Clear any errors
            document.getElementById('login-error').classList.add('hidden');
            document.getElementById('register-error').classList.add('hidden');
        } else {
            // Switch to register
            loginForm.classList.add('hidden');
            registerForm.classList.remove('hidden');
            authTitle.textContent = 'Register';
            switchText.textContent = "Already have an account?";
            switchLink.textContent = 'Login here';
            
            // Clear any errors
            document.getElementById('login-error').classList.add('hidden');
            document.getElementById('register-error').classList.add('hidden');
        }
    }
    
    async handleRegister() {
        const firstName = document.getElementById('register-first-name').value;
        const lastName = document.getElementById('register-last-name').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const socialHandle = document.getElementById('register-social').value;
        const errorDiv = document.getElementById('register-error');
        
        try {
            await this.makeRequest('/api/register', {
                method: 'POST',
                body: JSON.stringify({
                    first_name: firstName,
                    last_name: lastName,
                    email,
                    password,
                    social_handle_url: socialHandle || null
                })
            });
            
            // Auto-login after registration
            document.getElementById('login-email').value = email;
            document.getElementById('login-password').value = password;
            await this.handleLogin();
            
            errorDiv.classList.add('hidden');
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.classList.remove('hidden');
        }
    }
    
    logout() {
        this.authToken = null;
        localStorage.removeItem('authToken');
        this.showUnauthenticatedState();
        this.showPage('home-page');
        this.renderBooks(); // Re-render books to update button states
        this.updateCartCount(0);
    }
    
    async loadBooks(search = '') {
        const booksGrid = document.getElementById('books-grid');
        const loading = document.getElementById('loading');
        const noBooks = document.getElementById('no-books');
        
        try {
            loading.classList.remove('hidden');
            noBooks.classList.add('hidden');
            booksGrid.innerHTML = '';
            
            const url = search ? `/api/books?search=${encodeURIComponent(search)}` : '/api/books';
            this.books = await this.makeRequest(url);
            
            loading.classList.add('hidden');
            
            if (this.books.length === 0) {
                noBooks.classList.remove('hidden');
            } else {
                this.renderBooks();
            }
        } catch (error) {
            loading.classList.add('hidden');
            noBooks.textContent = `Error loading books: ${error.message}`;
            noBooks.classList.remove('hidden');
        }
    }
    
    renderBooks() {
        const booksGrid = document.getElementById('books-grid');
        
        booksGrid.innerHTML = this.books.map(book => `
            <div class="book-tile">
                <h3>${this.escapeHtml(book.title)}</h3>
                <p><strong>Author:</strong> ${this.escapeHtml(book.author)}</p>
                <p><strong>ISBN:</strong> ${this.escapeHtml(book.isbn || 'N/A')}</p>
                <p><strong>Year:</strong> ${book.year_of_release || 'N/A'}</p>
                <p><strong>Category:</strong> ${this.escapeHtml(book.category || 'N/A')}</p>
                <div class="price">$${parseFloat(book.price || 0).toFixed(2)}</div>
                <span class="state ${(book.state || '').replace(' ', '-')}">${this.escapeHtml(book.state || 'N/A')}</span>
                <button class="add-to-cart" onclick="app.addToCart(${book.id})" ${!this.authToken ? 'disabled' : ''}>
                    ${this.authToken ? 'Add to Cart' : 'Login to Add'}
                </button>
            </div>
        `).join('');
    }
    
    performSearch() {
        const searchTerm = document.getElementById('search-input').value.trim();
        this.loadBooks(searchTerm);
    }
    
    async addToCart(bookId) {
        if (!this.authToken) {
            alert('Please login to add items to cart');
            return;
        }
        
        try {
            await this.makeRequest('/api/cart/add', {
                method: 'POST',
                body: JSON.stringify({
                    book_id: bookId,
                    quantity: 1
                })
            });
            
            alert('Book added to cart!');
            this.updateCartCountFromServer();
        } catch (error) {
            alert('Error adding book to cart: ' + error.message);
        }
    }
    
    async loadCart() {
        if (!this.authToken) return;
        
        try {
            this.cart = await this.makeRequest('/api/cart');
            this.renderCart();
            this.updateCartCount(this.cart.length);
        } catch (error) {
            console.error('Error loading cart:', error);
        }
    }
    
    renderCart() {
        const cartItems = document.getElementById('cart-items');
        const cartTotal = document.getElementById('cart-total');
        const emptyCart = document.getElementById('empty-cart');
        
        if (this.cart.length === 0) {
            cartItems.innerHTML = '';
            cartTotal.classList.add('hidden');
            emptyCart.classList.remove('hidden');
            return;
        }
        
        cartTotal.classList.remove('hidden');
        emptyCart.classList.add('hidden');
        
        const total = this.cart.reduce((sum, item) => sum + parseFloat(item.subtotal), 0);
        document.getElementById('total-amount').textContent = total.toFixed(2);
        
        cartItems.innerHTML = this.cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-info">
                    <h4>${this.escapeHtml(item.book.title)}</h4>
                    <p>by ${this.escapeHtml(item.book.author)}</p>
                    <p><strong>Price:</strong> $${parseFloat(item.book.price || 0).toFixed(2)}</p>
                    <p><strong>Subtotal:</strong> $${parseFloat(item.subtotal).toFixed(2)}</p>
                </div>
                <div class="cart-item-controls">
                    <div class="quantity-controls">
                        <button onclick="app.updateCartQuantity(${item.book.id}, ${item.quantity - 1})">-</button>
                        <span>${item.quantity}</span>
                        <button onclick="app.updateCartQuantity(${item.book.id}, ${item.quantity + 1})">+</button>
                    </div>
                    <button class="remove-item" onclick="app.removeFromCart(${item.book.id})">Remove</button>
                </div>
            </div>
        `).join('');
    }
    
    async updateCartQuantity(bookId, quantity) {
        if (!this.authToken) return;
        
        try {
            if (quantity <= 0) {
                await this.removeFromCart(bookId);
                return;
            }
            
            await this.makeRequest(`/api/cart/${bookId}`, {
                method: 'PUT',
                body: JSON.stringify({ quantity })
            });
            
            this.loadCart();
        } catch (error) {
            alert('Error updating cart: ' + error.message);
        }
    }
    
    async removeFromCart(bookId) {
        if (!this.authToken) return;
        
        try {
            await this.makeRequest(`/api/cart/${bookId}`, {
                method: 'DELETE'
            });
            
            this.loadCart();
        } catch (error) {
            alert('Error removing item from cart: ' + error.message);
        }
    }
    
    async checkout() {
        if (!this.authToken) return;
        
        try {
            const response = await this.makeRequest('/api/checkout', {
                method: 'POST'
            });
            
            document.getElementById('order-id').textContent = response.order_id;
            document.getElementById('order-total').textContent = response.total.toFixed(2);
            document.getElementById('checkout-modal').classList.remove('hidden');
            
            this.loadCart(); // Refresh cart (should be empty now)
        } catch (error) {
            alert('Checkout failed: ' + error.message);
        }
    }
    
    async updateCartCountFromServer() {
        if (!this.authToken) return;
        
        try {
            const cart = await this.makeRequest('/api/cart');
            this.updateCartCount(cart.length);
        } catch (error) {
            console.error('Error updating cart count:', error);
        }
    }
    
    async loadUserProfile() {
        if (!this.authToken) return;
        
        try {
            this.currentUser = await this.makeRequest('/api/me');
            this.renderProfile();
        } catch (error) {
            console.error('Error loading profile:', error);
            alert('Error loading profile: ' + error.message);
        }
    }
    
    renderProfile() {
        const profileContainer = document.getElementById('profile-content');
        if (!this.currentUser) return;
        
        profileContainer.innerHTML = `
            <div class="profile-info">
                <h3>User Information</h3>
                <div class="profile-field">
                    <label>Name:</label>
                    <span>${this.escapeHtml(this.currentUser.first_name)} ${this.escapeHtml(this.currentUser.last_name)}</span>
                </div>
                <div class="profile-field">
                    <label>Email:</label>
                    <span>${this.escapeHtml(this.currentUser.email)}</span>
                </div>
                <div class="profile-field">
                    <label>Social Handle:</label>
                    <span>${this.currentUser.social_handle_url ? `<a href="${this.escapeHtml(this.currentUser.social_handle_url)}" target="_blank">${this.escapeHtml(this.currentUser.social_handle_url)}</a>` : 'Not provided'}</span>
                </div>
                <div class="profile-field">
                    <label>Member Since:</label>
                    <span>${new Date(this.currentUser.created_at).toLocaleDateString()}</span>
                </div>
            </div>
            <div class="profile-actions">
                <button id="edit-profile-btn" class="btn">Edit Profile</button>
            </div>
        `;
        
        // Add edit profile functionality (placeholder for now)
        document.getElementById('edit-profile-btn').addEventListener('click', () => {
            alert('Edit profile functionality coming soon!');
        });
    }

    updateCartCount(count) {
        document.getElementById('cart-count').textContent = count;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new BookBloomApp();
    window.app = app; // Make it globally available
});