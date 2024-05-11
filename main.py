from database_handler import Database

def main():
    db = Database("database.mp3")

    while True:
        print("\nMenu:")
        print("1. Enter an entry")
        print("2. Search for an entry")
        print("3. Print all entries")
        print("4. Add a file")
        print("5. Download a file")
        print("q. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            entry = input("Enter the entry: ")
            db.add_entry(entry)
        elif choice == "2":
            search_term = input("Enter the search term: ")
            db.search_entries(search_term)
        elif choice == "3":
            db.print_all_entries()
        elif choice == "4":
            file_path = input("Enter the file path: ")
            db.add_file(file_path)
        elif choice == "5":
            file_name = input("Enter the file name: ")
            db.download_file(file_name)
        elif choice == "q":
            break
        else:
            print("Invalid choice. Please try again.")

    db.save_database()

if __name__ == "__main__":
    main()