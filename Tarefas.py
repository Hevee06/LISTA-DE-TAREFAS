import sqlite3
import os

pasta_data = 'data'

if not os.path.exists(pasta_data):
    os.makedirs(pasta_data)

caminho_db = os.path.join(pasta_data, 'tarefas.db')

conn = sqlite3.connect(caminho_db)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    custo REAL NOT NULL,
    data_limite DATE NOT NULL,
    ordem INTEGER NOT NULL UNIQUE
)
''')

conn.commit()
conn.close()
