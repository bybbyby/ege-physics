// ============================================================
// SERVICE WORKER ДЛЯ PWA
// ============================================================

const CACHE_VERSION = 'v3';
const CACHE_NAME = `ege-physics-${CACHE_VERSION}`;

// Файлы для кэширования
const STATIC_CACHE_URLS = [
    '/',
    '/static/style.css',
    '/static/manifest.json',
    '/static/icon-144.png',
    '/static/icon-192.png',
    '/static/icon-512.png'
];

// ============================================================
// УСТАНОВКА
// ============================================================
self.addEventListener('install', event => {
    console.log('[SW] Установка...');

    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[SW] Кэширование статических файлов');
                return cache.addAll(STATIC_CACHE_URLS);
            })
            .then(() => {
                console.log('[SW] Установка завершена');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('[SW] Ошибка кэширования:', error);
            })
    );
});

// ============================================================
// АКТИВАЦИЯ
// ============================================================
self.addEventListener('activate', event => {
    console.log('[SW] Активация...');

    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames
                        .filter(name => name !== CACHE_NAME)
                        .map(name => {
                            console.log('[SW] Удаление старого кэша:', name);
                            return caches.delete(name);
                        })
                );
            })
            .then(() => {
                console.log('[SW] Активация завершена');
                return self.clients.claim();
            })
    );
});

// ============================================================
// ПЕРЕХВАТ ЗАПРОСОВ
// ============================================================
self.addEventListener('fetch', event => {
    const request = event.request;

    // Пропускаем запросы на сервер (API)
    if (request.url.includes('/get_question') ||
        request.url.includes('/answer') ||
        request.url.includes('/start_') ||
        request.url.includes('/clear_session') ||
        request.url.includes('/offline')) {
        // Если нет интернета, показываем страницу офлайн
        event.respondWith(
            fetch(request)
                .catch(() => {
                    return caches.match('/offline');
                })
        );
        return;
    }

    // Для статических файлов — сначала кэш, потом сеть
    event.respondWith(
        caches.match(request)
            .then(cachedResponse => {
                if (cachedResponse) {
                    return cachedResponse;
                }

                return fetch(request)
                    .then(response => {
                        // Кэшируем успешные ответы
                        if (response && response.status === 200) {
                            const clone = response.clone();
                            caches.open(CACHE_NAME)
                                .then(cache => {
                                    cache.put(request, clone);
                                });
                        }
                        return response;
                    })
                    .catch(error => {
                        console.error('[SW] Ошибка загрузки:', error);

                        // Если запрашивается HTML — показываем офлайн-страницу
                        if (request.headers.get('accept').includes('text/html')) {
                            return caches.match('/offline');
                        }

                        return new Response('Офлайн-режим', {
                            status: 503,
                            statusText: 'Service Unavailable'
                        });
                    });
            })
    );
});

// ============================================================
// ОБРАБОТКА ПУШ-УВЕДОМЛЕНИЙ (опционально)
// ============================================================
self.addEventListener('push', event => {
    const data = event.data ? event.data.json() : {};

    const options = {
        body: data.body || 'Новые вопросы для подготовки!',
        icon: '/static/icon-192.png',
        badge: '/static/icon-144.png',
        vibrate: [200, 100, 200],
        data: {
            url: data.url || '/'
        }
    };

    event.waitUntil(
        self.registration.showNotification(
            data.title || 'ЕГЭ Физика',
            options
        )
    );
});

// Обработка клика по уведомлению
self.addEventListener('notificationclick', event => {
    event.notification.close();

    event.waitUntil(
        clients.openWindow(event.notification.data.url || '/')
    );
});