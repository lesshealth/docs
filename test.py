import sqlite3
import pandas as pd

# Подключение к БД
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Очистка таблиц (на всякий случай)
cur.execute('DELETE FROM ProductMaterial')
cur.execute('DELETE FROM Product')
cur.execute('DELETE FROM Material')

# === Импорт материалов ===
df_mat = pd.read_excel('materials.xlsx')

# === Импорт продукции с доп. полями ===
df_prod = pd.read_excel('products.xlsx')
cols = df_prod.columns.str.lower()

for _, row in df_prod.iterrows():
    name = row[[col for col in cols if 'name' in col][0]]
    description = row[[col for col in cols if 'desc' in col][0]] if any('desc' in col for col in cols) else None
    category = row[[col for col in cols if 'category' in col][0]] if any('category' in col for col in cols) else None
    width = row[[col for col in cols if 'width' in col][0]] if any('width' in col for col in cols) else None
    height = row[[col for col in cols if 'height' in col][0]] if any('height' in col for col in cols) else None

    cur.execute('''
        INSERT INTO Product (name, description, category, width, height)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, description, category, width, height))


# Автоматическое определение названий колонок
material_name_col = [col for col in df_mat.columns if 'name' in col.lower()][0]
material_price_col = [col for col in df_mat.columns if 'price' in col.lower()][0]

for _, row in df_mat.iterrows():
    cur.execute('INSERT INTO Material (name, price) VALUES (?, ?)',
                (row[material_name_col], row[material_price_col]))

# === Импорт продукции ===
df_prod = pd.read_excel('products.xlsx')
product_name_col = [col for col in df_prod.columns if 'name' in col.lower()][0]

for _, row in df_prod.iterrows():
    cur.execute('INSERT INTO Product (name) VALUES (?)', (row[product_name_col],))

# === Импорт связей продукции и материалов ===
df_pm = pd.read_excel('prodmaterials.xlsx')

prod_col = [col for col in df_pm.columns if 'prod' in col.lower()][0]
mat_col = [col for col in df_pm.columns if 'mat' in col.lower()][0]
qty_col = [col for col in df_pm.columns if 'quant' in col.lower()][0]

for _, row in df_pm.iterrows():
    # Получение id продукции
    cur.execute('SELECT id FROM Product WHERE name = ?', (row[prod_col],))
    prod_id = cur.fetchone()
    if not prod_id:
        continue
    # Получение id материала
    cur.execute('SELECT id FROM Material WHERE name = ?', (row[mat_col],))
    mat_id = cur.fetchone()
    if not mat_id:
        continue
    # Добавление связи
    cur.execute('INSERT INTO ProductMaterial (product_id, material_id, quantity) VALUES (?, ?, ?)',
                (prod_id[0], mat_id[0], row[qty_col]))

# Сохранение
conn.commit()
conn.close()
print("Импорт завершён.")
