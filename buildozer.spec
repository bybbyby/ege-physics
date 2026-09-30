[app]
title = ЕГЭ Физика
package.name = egephysics
package.domain = org.egephysics

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js,json,txt

version = 1.0.0

# Зависимости Python
requirements = python3,kivy

# Ориентация
orientation = portrait

# Полноэкранный режим
fullscreen = 1

# Разрешения
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Версии Android
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# Иконка (положите icon.png 512x512 в корень)
# icon.filename = %(source.dir)s/icon.png

# Заставка (положите presplash.png в корень)
# presplash.filename = %(source.dir)s/presplash.png

android.allow_backup = True
android.debug = True

# Не запрашивать интерактивно
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
