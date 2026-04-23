#!/usr/bin/env python3
"""
Простой сканер для поиска админки на SPA сайтах
"""

import requests
import sys
from urllib.parse import urljoin

def find_admin_pages(url, wordlist):
    """
    Проверяет пути, игнорируя SPA-ловушку
    """
    
    # Отключаем SSL предупреждения (если нужно)
    requests.packages.urllib3.disable_warnings()
    
    # Сначала узнаем, как выглядит "пустая" страница
    print("[*] Калибровка: определение фейковой страницы...")
    fake_url = urljoin(url, "/ne_sushestvuet_987654321")
    
    try:
        fake_response = requests.get(fake_url, verify=False, timeout=10)
        fake_content = fake_response.text
        fake_length = len(fake_content)
        fake_words = len(fake_content.split())
        print(f"[!] Фейковая страница: размер={fake_length}, слов={fake_words}")
        print(f"[!] Статус: {fake_response.status_code}")
    except:
        print("[!] Не удалось определить фейковую страницу, продолжаем...")
        fake_length = None
        fake_words = None
    
    print(f"\n[*] Начинаем сканирование {url}")
    print("-" * 60)
    
    found = []
    
    # Читаем словарь
    try:
        with open(wordlist, 'r') as f:
            paths = [line.strip() for line in f if line.strip()]
    except:
        print(f"[!] Не могу открыть файл {wordlist}")
        return
    
    for i, path in enumerate(paths, 1):
        test_url = urljoin(url, path)
        
        try:
            response = requests.get(test_url, verify=False, timeout=5)
            
            # Анализируем ответ
            content = response.text
            current_length = len(content)
            current_words = len(content.split())
            
            # Критерии настоящей страницы:
            is_real = False
            
            # 1. Статус не 200 (редирект, ошибка, авторизация)
            if response.status_code not in [200]:
                is_real = True
                reason = f"статус {response.status_code}"
            
            # 2. Другой размер (не как у фейка)
            elif fake_length and abs(current_length - fake_length) > 100:
                is_real = True
                reason = f"размер {current_length} (не {fake_length})"
            
            # 3. Другое количество слов
            elif fake_words and current_words != fake_words:
                is_real = True
                reason = f"слов {current_words} (не {fake_words})"
            
            # 4. Заголовок Location (редирект)
            elif 'location' in response.headers:
                is_real = True
                reason = f"редирект на {response.headers['location']}"
            
            # 5. Заголовок Set-Cookie (возможно, логин)
            elif 'set-cookie' in response.headers:
                is_real = True
                reason = "установка cookie"
            
            if is_real:
                print(f"[+] НАЙДЕНО: {test_url}")
                print(f"    [{reason}] | Статус: {response.status_code}")
                found.append(test_url)
            
            # Прогресс (каждые 50 запросов)
            if i % 50 == 0:
                print(f"[*] Прогресс: {i}/{len(paths)}")
                
        except requests.exceptions.Timeout:
            print(f"[?] Таймаут: {test_url}")
        except Exception as e:
            print(f"[!] Ошибка: {test_url} - {e}")
    
    # Результаты
    print("\n" + "=" * 60)
    print(f"[*] Сканирование завершено. Найдено {len(found)} потенциальных админок:")
    print("=" * 60)
    for f in found:
        print(f"  → {f}")

def main():
    if len(sys.argv) != 3:
        print("Использование: python3 find_admin.py <URL> <wordlist>")
        print("Пример: python3 find_admin.py https://habluz.base44.app deroadmin.txt")
        sys.exit(1)
    
    url = sys.argv[1]
    if not url.endswith('/'):
        url += '/'
    
    wordlist = sys.argv[2]
    find_admin_pages(url, wordlist)

if __name__ == "__main__":
    main()