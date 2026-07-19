import urllib.request
import zipfile
import io
import csv

def load_real_cwe_database():
    """
    Скачивает официальную базу Software Development CWE от MITRE,
    распаковывает ZIP в памяти и возвращает список словарей.
    """
    print("Загрузка официального справочника CWE от MITRE...")
    url = 'https://cwe.mitre.org/data/csv/699.csv.zip'
    
    rules = []
    
    try:
        # Скачиваем ZIP-архив
        response = urllib.request.urlopen(url)
        with zipfile.ZipFile(io.BytesIO(response.read())) as z:
            # Внутри ZIP лежит один CSV-файл (например, 699.csv)
            csv_filename = z.namelist()[0]
            with z.open(csv_filename) as f:
                # Читаем CSV в текстовом режиме
                reader = csv.reader(io.TextIOWrapper(f, 'utf-8'))
                
                # Читаем заголовки, чтобы найти нужные колонки
                headers = next(reader)
                id_idx = headers.index('CWE-ID')
                name_idx = headers.index('Name')
                desc_idx = headers.index('Description')
                
                # Парсим строки
                for row in reader:
                    # Некоторые строки могут быть пустыми или некорректными
                    if len(row) > desc_idx:
                        rules.append({
                            "id": f"CWE-{row[id_idx]}",
                            "name": row[name_idx],
                            "description": row[desc_idx]
                        })
                        
        print(f"Успешно загружено {len(rules)} реальных CWE-правил!")
    except Exception as e:
        print(f"Ошибка загрузки базы CWE: {e}")
        
    return rules

# Экспортируем переменную, которая подтянет базу при старте приложения
CWE_RULES = load_real_cwe_database()
