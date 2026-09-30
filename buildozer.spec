[app]
title = ЕГЭ Физика
package.name = egephysics
package.domain = org.egephysics

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js,json,txt

version = 1.0.0

# ВАЖНО: без пина версии python3 — p4a сам подставит ту, что совпадает с hostpython3
requirements = python3,kivy==2.3.1,requests,urllib3,chardet,idna,certifi,six,filetype

orientation = portrait
fullscreen = 1

android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Ключевое: фиксируем стабильную ветку p4a, где hostpython3 = 3.11.5
p4a.branch = v2024.01.21

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

android.allow_backup = True
android.debug = True
android.accept_sdk_license = True

# Исключаем мусор из APK
source.exclude_patterns = zzzz.rar,*.rar,.git*,.github*,__pycache__/*,*.pyc

[buildozer]
log_level = 2
warn_on_root = 1
