// Allgemeine UI-Interaktionen
document.addEventListener('DOMContentLoaded', function() {
    // Flash Messages ausblenden nach 5 Sekunden
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-notification)');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        });
    }, 5000);

    // Tooltips aktivieren
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Warenkorb-Funktionalität
document.addEventListener('DOMContentLoaded', function() {
    // Event-Listener für "In den Warenkorb" Buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            const itemName = this.dataset.itemName;
            const itemPrice = this.dataset.itemPrice;

            // AJAX Request zum Hinzufügen des Items
            fetch('/cart/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrf_token')
                },
                body: JSON.stringify({
                    item_id: itemId,
                    quantity: 1
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Erfolgsbenachrichtigung anzeigen
                    showNotification(`${itemName} wurde zum Warenkorb hinzugefügt`, 'success');
                    // Warenkorb-Badge aktualisieren
                    updateCartCount(data.cart_count);
                } else {
                    showNotification(data.message || 'Ein Fehler ist aufgetreten', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Ein Fehler ist aufgetreten', 'danger');
            });
        });
    });

    // CSRF-Token aus Cookie auslesen
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Benachrichtigung anzeigen
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.top = '1rem';
        notification.style.right = '1rem';
        notification.style.zIndex = '1050';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        document.body.appendChild(notification);

        // Nach 3 Sekunden ausblenden
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Warenkorb-Badge aktualisieren
    function updateCartCount(count) {
        const cartCount = document.getElementById('cart-count');
        if (cartCount) {
            cartCount.textContent = count;
            cartCount.style.display = count > 0 ? 'inline' : 'none';
        }
    }

    // Initial Warenkorb-Count laden
    fetch('/cart/count')
        .then(response => response.json())
        .then(data => {
            updateCartCount(data.count);
        })
        .catch(error => console.error('Error:', error));
});

// Warenkorb Funktionen
function updateQuantity(itemId, delta) {
    const input = document.querySelector(`input[data-item-id="${itemId}"]`);
    if (input) {
        const currentValue = parseInt(input.value) || 1;
        const newValue = Math.max(1, currentValue + delta);
        input.value = newValue;
    }
}

// Adresse Validierung
function validateAddress(address) {
    return address && address.trim().length > 0;
}

// Bewertungen
function initStarRating() {
    const ratingInputs = document.querySelectorAll('.rating-input');
    ratingInputs.forEach(input => {
        input.addEventListener('change', function() {
            const stars = this.parentElement.querySelectorAll('.star');
            const rating = parseInt(this.value);
            stars.forEach((star, index) => {
                star.classList.toggle('active', index < rating);
            });
        });
    });
}

//Geolokalisierung
function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // Sende die Daten an deinen Server
    fetch('/get_location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ latitude, longitude })
    }).then(response => response.json())
        .then(data => {
            console.log('Nearby restaurants:', data);
        });
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}