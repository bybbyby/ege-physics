# main.py — точка входа для Android APK
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform
import threading
import time

# Определяем платформу
IS_ANDROID = platform == 'android'


def run_flask():
    """Запускает Flask-сервер в фоновом потоке"""
    try:
        from app import app
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
    except Exception as e:
        print(f"Ошибка запуска Flask: {e}")


class EgePhysicsApp(App):
    def build(self):
        self.title = 'ЕГЭ Физика'

        # Запускаем Flask в отдельном потоке
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # Даём серверу время запуститься
        time.sleep(3)

        if IS_ANDROID:
            # Открываем WebView на Android
            Clock.schedule_once(self.open_webview, 1)
        else:
            # Для теста на компьютере — открываем в браузере
            import webbrowser
            webbrowser.open('http://127.0.0.1:5000')

        return Widget()

    def open_webview(self, dt):
        """Открывает WebView с нашим сайтом"""
        try:
            from jnius import autoclass

            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            WebSettings = autoclass('android.webkit.WebSettings')
            Activity = autoclass('org.kivy.android.PythonActivity')

            activity = Activity.mActivity

            # Создаём WebView
            webview = WebView(activity)
            settings = webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setLoadWithOverviewMode(True)
            settings.setUseWideViewPort(True)
            settings.setBuiltInZoomControls(False)
            settings.setDisplayZoomControls(False)
            settings.setCacheMode(WebSettings.LOAD_DEFAULT)

            webview.setWebViewClient(WebViewClient())
            webview.loadUrl("http://127.0.0.1:5000")

            # Устанавливаем WebView как основной вид
            activity.setContentView(webview)

        except Exception as e:
            print(f"Ошибка открытия WebView: {e}")


if __name__ == '__main__':
    EgePhysicsApp().run()