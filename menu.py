from movie_manager import view_movies, add_movie, edit_movie, remove_movie

def show_menu():
    while True:
        print("\nMovie Catalog Menu")
        print("1. View Movies")
        print("2. Add Movie")
        print("3. Edit Movie")
        print("4. Remove Movie")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            edit_movie()
        elif choice == "4":
            remove_movie()
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")