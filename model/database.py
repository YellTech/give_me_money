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
    
    def consult(self, table, id, id_sql="id"):
        query = f'SELECT * FROM {table} WHERE {id_sql} = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()

    def close_conection(self):
        self.cursor.close()
        self.conn.close()

    def messages(self, function, table, e):
        messagebox.showerror("Erro", f"Erro ao {function} {table}:\n{str(e)}")

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
                            initial_date TEXT NOT NULL,
                            number_installments INTEGER,
                            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
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
                            FOREIGN KEY (debts_id) REFERENCES debts(id) ON DELETE CASCADE
                            )
                            ''')
        self.conn.commit()
        self.close_conection()

    def create_client(self, name, phone):
        try:
            self.cursor.execute('INSERT INTO clients (name, phone, cad_date) VALUES (?, ?, ?)',
                                (name, phone, self.cad_date))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.messages("cadastrar", "cliente", e)
            return False
        finally:
            self.close_conection()
    
    def delete_client(self, client_id):
        try:
            self.cursor.execute('DELETE FROM clients WHERE id = ?',
                                (client_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.messages("deletar", "cliente", e)
            return False
        finally:
            self.close_conection()
    
    def update_client(self, client_id, new_name, new_phone):
        try:
            self.conn.execute('UPDATE clients SET name = ?, phone = ?, WHERE id = ?',
                              (new_name, new_phone, client_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.messages("atualizar", "cliente", e)
            return False
        finally:
            self.close_conection()
    
    def create_debts(self, client_id, initial_value, interest_rate, initial_date, number_installments):
        try:
            self.conn.execute('''INSERT INTO debts (
                              client_id, initial_value, interest_rate, initial_date, number_installments)
                              VALUES (?, ?, ?, ?, ?)''',
                              (client_id, initial_value, interest_rate, initial_date, number_installments))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.messages("cadastrar", "dívida", e)
            return False
        finally:
            self.close_conection()
    
    def delete_debts(self, debts_id):
        try:
            self.conn.execute('DELETE FROM debts WHERE id = ?', (debts_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.messages("deletar", "dívida", e)
        finally:
            self.close_conection()
    
    def update_debts(self, debts_id, new_initial_value,
                     new_interest_rate, new_initial_date, new_number_installments):
        try:
            self.conn.execute('''UPDATE debts SET initial_value = ?,
                              interest_rate = ?, number_installments = ?, WHERE id = ?''',
                              (new_initial_value, new_interest_rate, new_initial_date, new_number_installments, debts_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.messages("atualizar", "dívida", e)
            return False
        finally:
            self.close_conection()

    def create_installments(self, debts_id, installment, installment_value, pay_date, status, interest_rate):
        try:
            self.conn.execute('''INSERT INTO installments (
                              debts_id, installment, installment_value, pay_date, status, interest_rate)
                              VALUES (?, ?, ?, ?, ?)''', 
                              (debts_id, installment, installment_value, pay_date, status, interest_rate))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.messages("cadastrar", "parcela", e)
            return False
        finally:
            self.close_conection()

    def delete_installments(self, debts_id):
        try:
            self.conn.execute('DELETE FROM installments WHERE debts_id = ?', (debts_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.messages("deletar", "parcelas", e)
            return False
        finally:
            self.close_conection()

if __name__ == "__main__":
    db_table = DBAccess()
    db_table.create_tables()
    db = DBAccess()
    teste = db.consult("debts", 1, "id")
    print(teste)
