import sqlite3

class Contact:

    def __init__(self, db_file):
        self.conn = None
        self.create_connection(db_file)
        self.create_tables()

    def create_connection(self, db_file):
        """
        Create a database connection to the SQLite database

        Args:
            db_file (string): path to the SQLite database

        Returns:
            None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)

    def create_tables(self):
        """
        Create the contacts table if it does not exist

        Args:
            None
        """
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
        """
        Close the database connection
        """
        self.conn.close()

    def contact_exists(self, email):
        """
        Check if a contact exists in the database

        Args:
            email (string): email address of the contact

        Returns:
            True if the contact exists, False otherwise
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM contacts WHERE email = ?", (email,))
        contact = cur.fetchone()
        return contact is not None
    
    def add_contact(self, first_name, last_name, email, phone, category):
        """
        Add a new contact to the database

        Args:
            first_name (string): first name of the contact
            last_name (string): last name of the contact
            email (string): email address of the contact
            phone (string): phone number of the contact
            category (string): category of the contact

        Returns:
            True if the contact was added successfully, False otherwise
        """
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
        """
        Edit an existing contact in the database

        Args:
            contact_id (int): id of the contact to edit
            first_name (string): new first name of the contact
            last_name (string): new last name of the contact
            email (string): new email address of the contact
            phone (string): new phone number of the contact
            category (string): new category of the contact

        Returns:
            True if the contact was edited successfully, False otherwise
        """
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
        """
        Check if a contact exists in the database

        Args:
            contact_id (int): id of the contact

        Returns:
            True if the contact exists, False otherwise
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        contact = cur.fetchone()
        return contact is not None

    def delete_contact(self, contact_id):
        """
        Delete a contact from the database

        Args:
            contact_id (int): id of the contact to delete

        Returns:
            True if the contact was deleted successfully, False otherwise
        """
        sql = """
        DELETE FROM contacts WHERE id = ?
        """
        cur = self.conn.cursor()
        cur.execute(sql, (contact_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def search_contacts(self, search_term):
        """
        Search for contacts in the database

        Args:
            search_term (string): search term to search for

        Returns:
            A formatted string with the contact information
        """
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
        """
        Group contacts by category

        Args:
            None

        Returns:
            A list of tuples with the category and the number of contacts in that category
        """
        sql = """
        SELECT category, COUNT(*) FROM contacts
        GROUP BY category
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def print_contacts(self):
        """
        Print a list of contacts

        Args:
            None

        Returns:
            None
        """
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
