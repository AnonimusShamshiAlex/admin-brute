

```markdown
# 🔍 SPA Admin Finder

Инструмент для поиска скрытых админок и путей на SPA-сайтах (React, Vue, Angular) и обычных веб-приложениях.

## 📋 Описание

Стандартные брутфорсеры (gobuster, dirb, ffuf) не работают на SPA-сайтах, потому что сервер возвращает `200 OK` на любой запрос. Этот скрипт обходит эту проблему и находит реально существующие пути.

## ✨ Возможности

- **Умное сканирование** — определяет фейковые страницы и игнорирует их
- **Анализ JavaScript** — находит скрытые маршруты в JS файлах
- **Фильтрация по**:
  - HTTP статусам (редиректы, ошибки, авторизация)
  - Размеру ответа
  - Количеству слов
  - Наличию кук и заголовков

## 🚀 Установка

```bash
# Делаем исполняемым
git clone https://github.com/AnonimusShamshiAlex/admin-brute

chmod +x admin-brute.py

# Устанавливаем зависимости
pip3 install requests
```

## 📖 Использование

### Базовое сканирование (рекомендуется)

```bash
python3 admin-brute.py https://target.com /path/to/wordlist.txt
```

**Пример:**
```bash
python3 admin-brute.py https://test.com admin_1000top.txt
```

### Продвинутое сканирование (SPA)

```bash
python3 admin-brute-spa.py
# Затем введите URL: https://habluz.base44.app
```

## 🛠️ Параметры

| Параметр | Описание |
|----------|----------|
| `URL` | Адрес целевого сайта (с http:// или https://) |
| `wordlist` | Путь к файлу со списком путей |

## 📝 Пример вывода

```
[*] Калибровка: определение фейковой страницы...
[!] Фейковая страница: размер=9157, слов=1303
[!] Статус: 200

[*] Начинаем сканирование https://test.com
------------------------------------------------------------
[+] НАЙДЕНО: https://test.com/wp-admin
    [размер 12450 (не 9157)] | Статус: 200
[+] НАЙДЕНО: https://test.com/administrator
    [статус 302] | Статус: 302
[+] НАЙДЕНО: https://test.com/api/login
    [установка cookie] | Статус: 200

============================================================
[*] Сканирование завершено. Найдено 3 потенциальных админок:
============================================================
  → https://test.com/wp-admin
  → https://test.com/administrator
  → https://test.com/api/login
```

## 📦 Создание wordlist

Используйте готовый список из 1000+ путей:

```bash
# Скачать топ-1000 путей админки
curl -o admin_top1000.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/admin-panels.txt

# Или использовать свой
nano my_wordlist.txt
```

## 🎯 Для SPA сайтов (React/Vue/Angular)

Если сайт использует клиентский роутинг:

1. **Анализируйте JavaScript файлы:**
```bash
python3 admin-brute-spa.py
```

2. **Ищите вручную через браузер:**
   - Откройте F12 → Network
   - Найдите `main.*.js` или `chunk.*.js`
   - Ищите слова: `routes`, `path`, `admin`, `dashboard`

3. **Проверьте хэш-роутинг:**
```
https://target.com/#/admin
https://target.com/#/login
https://target.com/#/dashboard
```

## ⚡ Быстрые однострочники

```bash
# Поиск JS файлов и путей в них
curl -s https://target.com/ | grep -oP 'src="\K[^"]+\.js' | while read js; do echo "=== $js ==="; curl -s "https://target.com/$js" | grep -E 'admin|login|panel' -i; done

# Поиск в JSON
curl -s https://target.com/ | grep -oP '({[^}]+})' | grep -E 'admin|login|path'
```

## 🔧 Устранение проблем

### Проблема: Все URL возвращают 200 OK
**Решение:** Используйте фильтрацию по размеру или количеству слов. Скрипт делает это автоматически.

### Проблема: Слишком много ложных срабатываний
**Решение:** Увеличьте порог разницы размера:
```python
# В коде измените 100 на большее число
elif fake_length and abs(current_length - fake_length) > 500:
```

### Проблема: Таймауты
**Решение:** Увеличьте timeout в коде:
```python
response = requests.get(test_url, verify=False, timeout=10)  # было 5
```

## 📊 Сравнение с другими инструментами

| Инструмент | Работает на SPA | Фильтрация | JS анализ |
|------------|-----------------|------------|-----------|
| **gobuster** | ❌ | ✅ | ❌ |
| **dirb** | ❌ | ❌ | ❌ |
| **ffuf** | ⚠️ (с флагами) | ✅ | ❌ |
| **Этот скрипт** | ✅ | ✅ | ✅ |

## 📜 Лицензия

MIT License - используйте свободно

## ⚠️ Предупреждение

Используйте только на сайтах, где у вас есть разрешение для тестирования на проникновение. Несанкционированное сканирование может быть незаконным.

## 🤝 Контрибьюция

Предложения и улучшения приветствуются!

## 📞 Поддержка

При проблемах проверьте:
1. Интернет соединение (`ping target.com`)
2. Доступность сайта (`curl -I https://target.com`)
3. Установлен ли `requests`: `pip3 install requests`
```

## Файл для быстрого старта:

Сохраните как `run.sh`:

```bash
#!/bin/bash

echo "=== SPA Admin Finder ==="
echo ""

# Проверка зависимостей
if ! python3 -c "import requests" 2>/dev/null; then
    echo "[!] Устанавливаем requests..."
    pip3 install requests
fi

# Создаём скрипт
cat > admin-brute.py << 'EOF'
# [вставьте сюда полный код первого скрипта из вашего сообщения]
EOF

chmod +x admin-brute.py

echo "[+] Готово! Запустите:"
echo "python3 admin-brute.py https://target.com wordlist.txt"
```

## Команды для терминала:

```bash

# Запустить скрипт
python3 admin-brute.py https://habluz.base44.app deroadmin.txt
```
