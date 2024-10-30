import sqlite3

from config import Database 

def create_user(db, userid):
    if db.find_user(db, userid) is None:
        db.insert_in_table(f"Basedata", (userid, 0, 0))


def add_to_wallet(db, userid, amount):
        db.update_table("Basedata", "wallet", amount, f"userid = {userid}")


def remove_from_wallet(db, userid, amount):
        db.update_table("Basedata", "wallet", -amount, f"userid = {userid}")

def  add_to_bank(db, userid, amount):
        db.update_table


def find_with_userid(db, userid):
    user = db.find_user(db, userid)
    if user is None:
        print("User  not found")
    else:
        print(f"User  info: {user}")
        

        
if __name__ == "__main__":
    db = Database("DataWarehouse.db")
    create_user(db, 69)
    add_to_wallet(db, 69, 122)
    remove_from_wallet(db, 69, 121)
    find_with_userid(db, 69)
    db.close()
