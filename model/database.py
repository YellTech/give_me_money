import sqlite3
from tkinter import messagebox
from datetime import datetime, timedelta

class DBAccess:
    def __init__(self, db_name='database.db'):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            self.conn = None
            self.cursor = None
            messagebox.showerror("Erro", f"Erro ao conectar com o Banco de Dados: \n{str(e)}")
        self.cad_date = datetime.now().strftime('%d-%m-%Y')
    
    def close_conection(self):
        self.cursor.close()
        self.conn.close()

    def create_tables(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS clients (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            phone TEXT,
                            cad_date TEXT
                            )
                            ''')
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS debts (
                            id INTEGER PRIMARY KEY,
                            client_id INTEGER NOT NULL,
                            initial_value REAL NOT NULL,
                            interest_rate REAL,
                            number_installments INTEGER
                            FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE
                            )
                            ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS istallments(
                            id INTEGER PRIMARY KEY,
                            debts_id INTEGER NOT NULL,
                            installment INTEGER NOT NULL,
                            installment_value REAL NOT NULL,
                            pay_date TEXT NOT NULL,
                            status TEXT NOT NULL,
                            interest_rate REAL,
                            FOREIGN KEY (debts_id) REFERENCES debts (id) ON DELETE CASCADE
                            )
                            ''')
        self.conn.commit()
        self.conn.close()

    def add_client(self, name, phone):
        try:
            self.cursor.execute('INSERT INTO clients (name, phone, cad_date) VALUES (?, ?, ?)',
                                (name, phone, self.cad_date))
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao adicionar cliente: \n{str(e)}")
            return False
        finally:
            self.close_conection()
    
    def delete_client(self, client_id):
        try:
            self.cursor.execute('DELETE FROM clients WHERE id = ?',
                                (client_id,))
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao deletar cliente: \n{str(e)}")
            return False
        finally:
            self.close_conection()
    
    def update_client(self, client_id, new_name, new_phone):
        try:
            self.conn.execute('UPDATE clients SET name = ?, phone = ?, WHERE id = ?',
                              (new_name, new_phone, client_id))
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atulizar cliente:\n{str(e)}")
            return False
        finally:
            self.close_conection()