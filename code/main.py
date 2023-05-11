import re
from contacts import Contact

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
