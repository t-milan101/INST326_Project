import unittest
import os

from contacts import Contact

# Define the name of the test database file
DB_FILE = "test.db"
# Create a TestContact class that inherits from the TestCase class of the unittest module
class TestContact(unittest.TestCase):
    # Define a setUp() method that will be called before each test method
    def setUp(self):
        # Create a new Contact object using the test database file
        self.contact = Contact(DB_FILE)

    # Define a tearDown() method that will be called after each test method
    def tearDown(self):
        # Close the connection to the database
        self.contact.close()
        # Delete the test database file
        os.remove(DB_FILE)

    # Define a test method to check if the connection to the database was created successfully
    def test_create_connection(self):
        self.assertIsNotNone(self.contact.conn)

    # Define a test method to check if the contacts table was created successfully
    def test_create_tables(self):
        # Create a cursor object
        cursor = self.contact.conn.cursor()
        # Execute a SQL query to check if the contacts table exists in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contacts';")
        # Check if the query returned a row, indicating that the table exists
        self.assertIsNotNone(cursor.fetchone())

    # Define a test method to check if a contact with a specific email address exists in the database
    def test_contact_exists(self):
        # Check that the method returns False for a non-existent email address
        self.assertFalse(self.contact.contact_exists("test@example.com"))
        # Add a contact to the database
        self.contact.add_contact("Test", "User", "test@example.com", "555-555-5555", "Friend")
        # Check that the method returns True for the newly added email address
        self.assertTrue(self.contact.contact_exists("test@example.com"))

    # Define a test method to check if a new contact can be added to the database
    def test_add_contact(self):
        # Check that the method returns True for a new contact with a unique email address
        self.assertTrue(self.contact.add_contact("Test", "User", "test@example.com", "555-555-5555", "Friend"))
        # Check that the method returns False for a new contact with a non-unique email address
        self.assertFalse(self.contact.add_contact("Test", "User", "test@example.com", "555-555-5555", "Friend"))

    # Define a test method to check if a contact can be edited in the database
    def test_edit_contact(self):
        # Check that the method returns False for a non-existent contact ID
        self.assertFalse(self.contact.edit_contact(1, first_name="Test", last_name="User", email="test@example.com", phone="555-555-5555", category="Friend"))
        # Add a contact to the database
        self.contact.add_contact("Test", "User", "test@example.com", "555-555-5555", "Friend")
        # Check that the method returns True for an existing contact ID and valid data
        self.assertTrue(self.contact.edit_contact(1, first_name="New", last_name="User", email="test@example.com", phone="555-555-5555", category="Friend"))

    # Define a test method to check if a contact with a specific ID exists in the database
    def test_contact_id_exists(self):
        # Check that the method returns False for a non-existent contact ID
        self.assertFalse(self.contact.contact_id_exists(1))
        # Add a contact to the database
        self.contact.add_contact("Test", "User", "test@example.com", "555-555-5555", "Friend")
        self.assertTrue(self.contact.contact_id_exists(1))

    def test_delete_contact(self):
        # This test case checks if a contact can be successfully deleted from the database.
        # It tries to delete a non-existent contact, then adds a new contact and deletes it.
        self.assertFalse(self.contact.delete_contact(1))
        self.contact.add_contact("Test", "User", "test@example.com", "555-555-5555", "Friend")
        self.assertTrue(self.contact.delete_contact(1))

    def test_search_contacts(self):
        # This test case checks if a search query returns the expected contact(s) from the database.
        # It adds a new contact, searches for its name and then checks if the returned contact info is correct.
        self.contact.add_contact("Test", "User", "test@example.com", "555-555-5555", "Friend")
        self.assertEqual(self.contact.search_contacts("Test"), "Name: Test User\nEmail: test@example.com\nPhone: 555-555-5555\nCategory: Friend\n----------------------\n")

    def test_group_contacts_by_category(self):
        # Add two contacts with the same category
        self.contact.add_contact("Test", "User", "test@example.com", "555-555-5555", "Friend")
        self.contact.add_contact("Test2", "User2", "test2@example.com", "555-555-5556", "Friend")
        
        # Check that the contacts are grouped by category
        expected_result = [("Friend", 2)]
        self.assertEqual(self.contact.group_contacts_by_category(), expected_result)


if __name__ == '__main__':
    unittest.main()
