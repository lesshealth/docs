import pandas as pd
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect("wallpapers.db")
cursor = conn.cursor()

# Загрузка Excel-файлов
df_products = pd.read_excel("imports/products.xlsx")
df_materials = pd.read_excel("imports/materials.xlsx")
df_prodmaterials = pd.read_excel("imports/prodmaterials.xlsx")

# Переименование столбцов под названия таблиц в базе
df_products.rename(columns={"name": "Name"}, inplace=True)
df_materials.rename(columns={"name": "Name", "price": "Cost"}, inplace=True)

# Переименование столбцов
# df_products.rename(columns={
#     "name": "Name",
#     "description": "Description",
#     "category": "Category",
#     "width": "Width",
#     "height": "Height"
# }, inplace=True)

# Загрузка продукции с новыми полями
# for _, row in df_products.iterrows():
#     cursor.execute("""
#         INSERT INTO Product (Name, Description, Category, Width, Height)
#         VALUES (?, ?, ?, ?, ?)
#     """, (row["Name"], row["Description"], row["Category"], row["Width"], row["Height"]))
# # Загрузка продукции
# for _, row in df_products.iterrows():
#     cursor.execute("INSERT INTO Product (Name) VALUES (?)", (row["Name"],))

# Загрузка материалов
for _, row in df_materials.iterrows():
    cursor.execute("INSERT INTO Material (Name, Cost) VALUES (?, ?)", (row["Name"], row["Cost"]))

# df_materials.rename(columns={"name": "Name", "price": "Cost", "description": "Description", "manufacturer": "Manufacturer"}, inplace=True)

# for _, row in df_materials.iterrows():
#     cursor.execute("""
#         INSERT INTO Material (Name, Cost, Description, Manufacturer)
#         VALUES (?, ?, ?, ?)
#     """, (row["Name"], row["Cost"], row["Description"], row["Manufacturer"]))



# Создание словарей для получения ID по названию
cursor.execute("SELECT ID, Name FROM Product")
product_dict = {name: id for id, name in cursor.fetchall()}

cursor.execute("SELECT ID, Name FROM Material")
material_dict = {name: id for id, name in cursor.fetchall()}

# Загрузка связей ProductMaterial
for _, row in df_prodmaterials.iterrows():
    product_id = product_dict[row["product_name"]]
    material_id = material_dict[row["material_name"]]
    quantity = row["quantity"]
    cursor.execute("""
        INSERT INTO ProductMaterial (ProductID, MaterialID, Quantity)
        VALUES (?, ?, ?)
    """, (product_id, material_id, quantity))

# Сохраняем и закрываем
conn.commit()
conn.close()

print("Данные успешно загружены в базу данных.")
