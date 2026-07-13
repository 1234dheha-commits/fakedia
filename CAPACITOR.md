# Capacitor — нативний застосунок «Дія» демо

Веб-версія (Vercel) лишається. Для телефону без PWA-полосок — збірка через Capacitor.

## Що вже є
- `www/` — веб-ресурси
- `android/` — Android-проект
- плагіни: StatusBar (edge-to-edge), SplashScreen

## Android (Windows)

1. Встанови [Android Studio](https://developer.android.com/studio)
2. У терміналі в папці проекту:

```bash
npm install
npm run android
```

3. У Android Studio: підключи телефон (USB + налагодження) або емулятор → **Run**
4. Або збери APK: **Build → Build Bundle(s) / APK(s) → Build APK(s)**

Після змін у `index.html`:

```bash
npm run sync
```

потім знову Run в Android Studio.

## iOS (лише Mac)

```bash
npm install
npx cap add ios
npm run ios
```

Потрібні Xcode і Apple ID (для свого пристрою — без App Store).

## Чому це краще за «На екран Домой»
PWA в iOS малює safe-area як браузер. Capacitor — WebView як у звичайному застосунку: StatusBar overlay + нормальний `env(safe-area-inset-*)`, без бірюзової/зайвої чорної смуги від ярлика Safari.
