import sqlite3


class DatabaseManager:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file, check_same_thread=False)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def execute_get(self, command):
        cursor = self.get_cursor()
        cursor.execute(command)
        return cursor.fetchall()

    def select(self, table, var_name="", var=""):
        cursor = self.get_cursor()
        if (var_name == ""):
            command = f"SELECT * FROM {table}"
            cursor.execute(command)
            return cursor.fetchall()
        command = f"SELECT * FROM {table} WHERE {var_name}=?"
        cursor.execute(command, (var,))
        return cursor.fetchone()

    def select_col(self, table, col_name, var_name="", var=""):
        cursor = self.get_cursor()
        if (var_name == ""):
            command = f"SELECT {col_name} FROM {table}"
            cursor.execute(command)
            return cursor.fetchall()
        command = f"SELECT {col_name} FROM {table} WHERE {var_name}=?"
        cursor.execute(command, (var,))
        return cursor.fetchall()

    def select_subtable(self, table, var_name, in_table, in_select, in_var_name, in_var):
        cursor = self.get_cursor()
        command = f"SELECT * FROM {table} WHERE {var_name} IN (SELECT {in_select} FROM {in_table} WHERE {in_var_name}=?)"
        cursor.execute(command, (in_var,))
        return cursor.fetchall()

    def insert(self, table, var_name, var, commit=True):
        if len(var_name) != len(var):
            raise RuntimeError(
                "variable names and variables must have same size")
        cursor = self.get_cursor()
        command = f"INSERT INTO {table}(" + ", ".join(var_name) + \
            ") VALUES (" + ", ".join(["?"] * len(var)) + ")"
        cursor.execute(command, var)
        rows_changed = cursor.rowcount
        row_id = None
        if commit:
            self.conn.commit()
            row_id = cursor.lastrowid
        return row_id, rows_changed

    def update(self, table, var_changed, var_name, var, commit=True):
        cursor = self.get_cursor()
        command = "UPDATE tasks SET " + \
            ", ".join([f"{key}=\"{var_changed[key]}\"" for key in var_changed]
                      ) + f" WHERE {var_name}={var}"
        cursor.execute(command)
        if commit:
            self.conn.commit()

    def delete(self, table, var_name, var, op=" AND ", commit=True):
        cursor = self.get_cursor()
        command = f"DELETE FROM {table} WHERE (" + op.join(
            [f"{var_name[v]}={var[v]}" for v in range(len(var_name))]) + ")"
        cursor.execute(command)
        rows_changed = cursor.rowcount
        if commit:
            self.conn.commit()
        return rows_changed
