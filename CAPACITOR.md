# Capacitor — нативний застосунок «Дія» демо

Веб-версія (Vercel) лишається. Для телефону без PWA-полосок — збірка через Capacitor / Codemagic.

## Codemagic (хмара)

- GitHub: https://github.com/1234dheha-commits/fakedia
- Codemagic app: https://codemagic.io/app/6a55174cd52063989deea651
- Workflows у `codemagic.yaml`:
  - `android-debug` — debug APK (без keystore)
  - `ios-release` — IPA (потрібен App Store Connect + bundle `ua.demo.fakedia`)

Артефакт APK: Codemagic → Builds → Artifacts після finish.

## Локально Android (Windows)

1. [Android Studio](https://developer.android.com/studio)
2. `npm install` → `npm run android` → Run

Після змін у `index.html`: `npm run sync`

## iOS

Лише Mac або Codemagic workflow `ios-release` (потрібні сертифікати / ASC).
