#!/usr/bin/env python3
"""
Специально для SPA: ищет пути в JavaScript файлах
"""

import requests
import re
from urllib.parse import urljoin, urlparse

def extract_js_paths(url):
    """
    Извлекает возможные пути из JS файлов
    """
    print(f"[*] Анализируем {url}")
    
    # Скачиваем главную страницу
    response = requests.get(url, verify=False)
    html = response.text
    
    # Находим все JS файлы
    js_files = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', html)
    js_files = [urljoin(url, js) for js in js_files]
    
    print(f"[*] Найдено JS файлов: {len(js_files)}")
    
    all_paths = set()
    
    # Паттерны для поиска в JS
    patterns = [
        r'path:\s*["\']([^"\']+)["\']',
        r'route:\s*["\']([^"\']+)["\']',
        r'to:\s*["\']([^"\']+)["\']',
        r'redirect:\s*["\']([^"\']+)["\']',
        r'["\'](/[a-zA-Z0-9/_-]+)["\']',
        r'admin|login|dashboard|panel|manage',  # ключевые слова
    ]
    
    for js_url in js_files:
        try:
            js_content = requests.get(js_url, verify=False, timeout=10).text
            
            # Ищем пути
            for pattern in patterns:
                matches = re.findall(pattern, js_content, re.IGNORECASE)
                for match in matches:
                    if match.startswith('/') and len(match) > 1:
                        all_paths.add(match)
            
            # Ищем с большой буквы
            for match in re.findall(r'["\'](/[A-Z][a-zA-Z0-9/_-]+)["\']', js_content):
                all_paths.add(match)
                
        except Exception as e:
            print(f"[!] Ошибка загрузки {js_url}: {e}")
    
    print(f"\n[*] Найдено потенциальных путей: {len(all_paths)}")
    print("=" * 50)
    
    for path in sorted(all_paths):
        # Проверяем админские пути
        if any(keyword in path.lower() for keyword in ['admin', 'login', 'panel', 'dashboard', 'manage', 'console']):
            print(f"[+] ВАЖНО: {path}")
        else:
            print(f"    {path}")

def main():
    url = input("Введите URL сайта: ").strip()
    if not url.startswith('http'):
        url = 'https://' + url
    
    extract_js_paths(url)

if __name__ == "__main__":
    main()