from datasets import load_dataset

ds = load_dataset("claudios/DiverseVul", split="test")

# Смотрим структуру
print("=== СТРУКТУРА ДАТАСЕТА ===")
print(ds)
print()
print("=== КОЛОНКИ ===")
print(ds.column_names)
print()

# Смотрим первую запись
print("=== ПЕРВАЯ ЗАПИСЬ ===")
row = ds[0]
for key, value in row.items():
    print(f"[{key}]: {str(value)[:100]}")   # обрезаем длинные строки
print()

# Считаем сколько уязвимых (target=1) и безопасных (target=0)
print("=== РАСПРЕДЕЛЕНИЕ TARGET ===")
targets = ds["target"]
vuln_count = sum(1 for t in targets if t == 1)
safe_count = sum(1 for t in targets if t == 0)
print(f"Уязвимых (target=1): {vuln_count}")
print(f"Безопасных (target=0): {safe_count}")
