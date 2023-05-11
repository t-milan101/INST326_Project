import sqlite3
import re

class Contact:

    def __init__(self, db_file):
        self.conn = None
        self.create_connection(db_file)
        self.create_tables()

    def create_connection(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)

    def create_tables(self):
        sql_create_contacts_table = """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            category TEXT
        );
        """
        cur = self.conn.cursor()
        cur.execute(sql_create_contacts_table)

    def close(self):
        self.conn.close()

    def contact_exists(self, email):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM contacts WHERE email = ?", (email,))
        contact = cur.fetchone()
        return contact is not None
    
    def add_contact(self, first_name, last_name, email, phone, category):
        sql = """
        INSERT INTO contacts(first_name, last_name, email, phone, category)
        VALUES(?, ?, ?, ?, ?)
        """
        if not self.contact_exists(email):
            cur = self.conn.cursor()
            cur.execute(sql, (first_name, last_name, email, phone, category))
            self.conn.commit()
            cur.close()

            return True
        
        return False
    
    def edit_contact(self, contact_id, first_name=None, last_name=None, email=None, phone=None, category=None):
        sql = """
        UPDATE contacts SET
            first_name = ?,
            last_name = ?,
            email = ?,
            phone = ?,
            category = ?
        WHERE id = ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, (first_name, last_name, email, phone, category, contact_id))
        self.conn.commit()
        return cur.rowcount > 0
    
    # a function to check if a contact id exists in the db
    def contact_id_exists(self, contact_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        contact = cur.fetchone()
        return contact is not None

    def delete_contact(self, contact_id):
        sql = """
        DELETE FROM contacts WHERE id = ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, (contact_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def search_contacts(self, search_term):
        sql = """
        SELECT * FROM contacts
        WHERE first_name LIKE ?
        OR last_name LIKE ?
        OR email LIKE ?
        OR phone LIKE ?
        OR category LIKE ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, ('%{}%'.format(search_term), '%{}%'.format(search_term), '%{}%'.format(search_term), '%{}%'.format(search_term), '%{}%'.format(search_term)))
        rows = cur.fetchall()
        # Generate a formatted string with the contact information
        result = ""
        for row in rows:
            result += "Name: {} {}\n".format(row[1], row[2])
            result += "Email: {}\n".format(row[3])
            result += "Phone: {}\n".format(row[4])
            result += "Category: {}\n".format(row[5])
            result += "----------------------\n"
        return result


    def group_contacts_by_category(self):
        sql = """
        SELECT category, COUNT(*) FROM contacts
        GROUP BY category
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def print_contacts(self):

        sql = "SELECT * FROM contacts"
        """Print a list of contacts."""
        cur = self.conn.cursor()
        cur.execute(sql)
        contacts = cur.fetchall()
        if not contacts:
            print("No contacts found.")
            return

        for contact in contacts:
            print("ID: {}".format(contact[0]))
            print("First Name: {}".format(contact[1]))
            print("Last Name: {}".format(contact[2]))
            print("Email: {}".format(contact[3]))
            print("Phone: {}".format(contact[4]))

def print_menu():
    """Print the main menu options."""
    print("\n--------------------CONTACTS DB--------------------")
    print("1. Add a new contact")
    print("2. Edit an existing contact")
    print("3. Delete a contact")
    print("4. Search for contacts")
    print("5. Group contacts by category")
    print("6. Exit")

def is_email_valid(email):
    email_reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(email_reg, email):
        return True
    return False

def is_phone_valid(phone):
    # generate a regex to check for 10 digit phone number
    phone_reg = re.compile(r'\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})')
    if re.fullmatch(phone_reg, phone):
        return True
    return False

if __name__ == "__main__":
    c = Contact("./data/contacts.db")

    while True:
        print_menu()
        choice = input("Enter your choice: ")
        print("\n-----------------------------------------")

        if choice == "1":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            if not is_email_valid(email):
                print("\n\nInvalid email. Contact not added.")
                continue
            phone = input("Enter phone number: ")
            if not is_phone_valid(phone):
                print("Invalid phone number. Contact not added.")
                continue
            category = input("Enter category: ")
            if c.add_contact( first_name, last_name, email, phone, category):
                print("\n\nContact added successfully.")
            else:
                print("\n\nDuplciate contact. Contact not added.")

        elif choice == "2":
            contact_id = input("Enter ID of contact to edit: ")
            if not c.contact_id_exists(contact_id):
                print("\n\n Contact does not exist in the database. Try again...")
                continue
            first_name = input("Enter new first name (leave blank to keep current): ")
            last_name = input("Enter new last name (leave blank to keep current): ")
            email = input("Enter new email (leave blank to keep current): ")
            if not is_email_valid(email):
                print("Invalid email. Contact not updated. Try again...")
                continue
            phone = input("Enter new phone number (leave blank to keep current): ")
            if not is_phone_valid(phone):
                print("\n\nInvalid phone number. Contact not updated.")
                continue
            category = input("Enter new category (leave blank to keep current): ")
            if c.edit_contact(contact_id, first_name, last_name, email, phone, category):
                print("\n\nContact updated successfully.")
            else:
                print("\n\nNo contact found with that ID.")

        elif choice == "3":
            contact_id = input("Enter ID of contact to delete: ")
            if c.delete_contact( contact_id):
                print("\n\nContact deleted successfully.")
            else:
                print("\n\nNo contact found with that ID.")

        elif choice == "4":
            search_term = input("Enter search term: ")
            search_result = c.search_contacts(search_term)
            print(search_result)

        elif choice == "5":
            categories = c.group_contacts_by_category()
            for category in categories:
                print("{}: {}".format(category[0], category[1]))

        elif choice == "6":
            print("\n EXITING...")
            c.close()
            break
 
        else:
            print("Invalid choice. Please try again.")
            
    c.close()
