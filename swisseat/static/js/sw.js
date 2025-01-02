// Eventlistener für Push-Benachrichtigungen
self.addEventListener('push', (event) => {
    const data = event.data ? event.data.json() : {};

    const options = {
        body: data.body || 'Standard Nachrichtentext',
        icon: data.icon || '/images/default-icon.png',
        badge: data.badge || '/images/default-badge.png',
    };

    event.waitUntil(
        self.registration.showNotification(data.title || 'Benachrichtigung', options)
    );
});

// Klick-Event für Benachrichtigungen
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    // Optional: URL öffnen
    const clickActionUrl = event.notification.data?.url || '/';
    event.waitUntil(
        clients.openWindow(clickActionUrl)
    );
});
