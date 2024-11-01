import sqlite3
from typing import List, Tuple, Optional, Any

class Configs():
    def __init__(self, database_file: str):
        self.conn = sqlite3.connect(database_file)
        self.c = self.conn.cursor()

    #---------------------------Table Commands------------------------------------
    def create_table(self, table: str, columns: str) -> None:
        """Creates a table if it does not exist."""
        self.c.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns})")
        self.conn.commit()

    def insert_into_table(self, table: str, values: Tuple[Any]) -> None:
        """Inserts values into a table."""
        placeholders = ', '.join('?' for _ in values)
        self.c.execute(f"INSERT INTO {table} VALUES ({placeholders})", values)
        self.conn.commit()

    def update_table(self, table: str, column: str, value: Any, condition: str) -> None:
        """Updates a specific column in the table."""
        self.c.execute(f"UPDATE {table} SET {column} = {column} + ? WHERE {condition}", (value,))
        self.conn.commit()
        
    #---------------------------Non-commit Commands------------------------------------
    def find_user(self, table: str, userid: int) -> Optional[Tuple]:
        """Finds a user by userid."""
        self.c.execute(f"SELECT * FROM {table} WHERE userid = ?", (userid,))
        return self.c.fetchone()

    #---------------------------Fetch Commands------------------------------------
    def fetch_one(self, table: str, condition: str) -> Optional[Tuple]:
        """Fetches one record from the table based on a condition."""
        self.c.execute(f"SELECT * FROM {table} WHERE {condition}")
        return self.c.fetchone()
 
    def fetch_many(self, table: str, condition: str, limit: int = 10) -> List[Tuple]:
        """Fetches multiple records from the table based on a condition."""
        self.c.execute(f"SELECT * FROM {table} WHERE {condition} LIMIT ?", (limit,))
        return self.c.fetchmany()

    def fetch_all(self, table: str, condition: str) -> List[Tuple]:
        """Fetches all records from the table based on a condition."""
        self.c.execute(f"SELECT * FROM {table} WHERE {condition}")
        return self.c.fetchall()
    
    #-------Close--------
    def close(self) -> None:
        """Closes the database connection."""
        self.conn.close()

# Example usage
#db = Configs("DataWarehouse.db")
#db.create_table("Basedata",columns="userid INT, wallet INT,bank INT")
#result = db.fetch_all("Basedata", "userid > 0")  # Adjust condition as needed
#print( result)
#db.close()