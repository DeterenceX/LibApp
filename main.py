import json
import os
from isbn_lookup import fetch_book_info

# duplicates before library overloads with HAIL REAPER!



current_library = "library.json"
# --- Function definitions ---
def divider():
	print("---------------------------------")	
def load_library(filename = current_library):
	if os.path.exists(filename):
		with open(filename, "r") as file:
			try:
				library = json.load(file)
				if not isinstance(library, list):
					return []
				return library
			except (json.JSONDecodeError):
				return []
	return []
		
	return library
def save_library(library, filename = current_library):
	with open(filename, "w") as file:
		json.dump(library, file, indent = 4)
def save_to_library(book,  filename = current_library):
	library = load_library(filename)
	for entry in library:
		if entry["isbn"] == book["isbn"] and entry.get("binding") == book.get("binding"):
			divider()
			print(f"Book already exists with ISBN {book['isbn']} and binding '{book.get('binding')}'. Not added.")
			divider()
			return
			
	library.append(book)
	with open(filename, "w") as file:
		json.dump(library, file, indent = 4)	
def add_book():
	user_input = input("Please scan book or enter book's ISBN: ").strip()
	# This wont catch wrong numbers, or even correct numbers.
	if user_input == "exit" or user_input == "None":
		return
	if not is_valid_isbn(user_input):
		divider()
		print("Improper ISBN format.")
		return
	book = fetch_book_info(user_input)
	if not book:
		print("Error searching for book")
		return
	# Red Risings ISBN 9781444758993. So I can stop searching it.
	if book:
		binding_types = ["HC","PB","SE"]
		binding = input("Hardcover, Paperback, Special Edition? (HC/PB/SE): ")
		if binding.upper() not in binding_types:
			book["binding"] = None
		else:
			book["binding"] = binding
		save_to_library(book, filename = current_library)
		divider()
		print("Book added to library:")
		print(f"  Title:  {book['title']}")
		print(f"  Author:  {book['author']}")
		print(f"  Cover:  {book['cover_url']}")
		print(f"  Binding: {book['binding']}")
	else:
		print("Book not found.")
def is_valid_isbn(query):
	return query.isdigit() and len(query) in [10,13]
def search_books(query, filename = current_library):
	library = load_library(current_library)
	query = query.lower().strip()
	matches = []
		
	for book in library:
		isbn = book.get('isbn', '').lower()	
		title = book.get('title', '').lower()
		author = book.get('author', '').lower()	
		if is_valid_isbn(query) and isinstance(isbn, str) and query == isbn.lower():
			matches.append(book)
			continue
		if query in title or query in author:
			matches.append(book)
	return matches		
def delete_book(filename = current_library):
	library = load_library(filename)
	if not library:
		divider()
		print("Your library is empty!")
		divider()
		return
	isbn_input = input("Please enter ISBN to delete: ").strip()
	book_to_delete = search_books(isbn_input)
	if book_to_delete:
		confirmation = input(f"{book_to_delete['title']} by {book_to_delete['author']} -- Delete? Y/N: ")
		if confirmation.upper() == "Y":
			library.remove(book_to_delete)
			save_library(library,filename)
			divider()
			print("Book deleted.")
		elif confirmation.upper() == "N":
			divider()
			print("Deletion canceled.")
			delete_book()
	else:
		divider()
		print("Book not found.")
		divider()
def view_library(filename = current_library):
	library = load_library(filename)
	if not library:
		divider()
		print("Your library is empty")
		divider()
		return
	
	# Sorting options
	divider()
	print("Books in your library:")
	print("1. Title (A-Z)")
	print("2. Author (A-Z)")
	print("3. ISBN")
	sort_choice = input("Choose sort method (1-3): ").strip()
	
	match sort_choice:
		case "1":
			library.sort(key = lambda book: book.get("title", "").lower())
		case "2":
			library.sort(key = lambda book: book.get("author", "").lower())
		case "3":
			library.sort(key = lambda book: book.get("isbn", ""))
		case _:
			print("Invalid choice. Showing unsorted library.")
	divider()
	print(f" There are currrently {len(library)} books in your library.")
	divider()
	for i, book in enumerate(library, start = 1):
		print(f"{i}. {book['title']} by {book['author']} {book['binding'].upper()} (ISBN: {book['isbn']}) ")
		divider()
def edit_book(filename = current_library):
	library = load_library(filename)
	if not library:
		divider()
		print("Your library is empty")
		divider()
		return
	
	query = input("Enter the ISBN of the book to edit: ").strip()
	matches = search_books(query, filename)
	if not matches:
		divider()
		print("No matching book found.")
		divider()
		return
		
	if len(matches) > 1:
		divider()
		print(f"Found {len(matches)} matching book(s).")  # debug
		for i, book in enumerate(matches, start = 1):
			print(f"{i}. {book['title']} by {book['author']} (ISBN: {book['isbn']})")
		choice = input("Enter number of book to edit: ").strip()
		if not choice.isdigit() or not (1 <= int(choice) <= len(matches)):
			print("Invalid selection.")
			return
		book = matches[int(choice) - 1]
	else:
		book = matches[0]
		
	divider()
	print("Editing Book:")
	print(f"1. Title:     {book.get('title', 'unknown')}")
	print(f"2. Author:    {book.get('author', 'unknown')}") 
	print(f"3. Binding:   {book.get('binding', 'N/A')} ")
	print(f"4. Condition: {book.get('condition', 'N/A')}")
	print(f"5. Rating:    {book.get('rating', 'N/A')}")
	print(f"6. Status:    {book.get('status', 'unread')}")
	print("7. Cancel")
	
	choice = input("Which field would you like to edit (1-6)? ").strip()
	match choice:
		case "1":
			new_title = input("Enter new title: ").strip()
			if new_title:
				book["title"] = new_title
		case "2":
			new_author = input("Enter new author: ").strip()
			if new_author:
				book["author"] = new_author
		case "3":
			new_binding = input("Enter new binding type: ").strip()
			if new_binding in ["HC", "PB", "SE"]:
				book["binding"] = new_binding
		case "4":
			new_condition = input("Enter new condition: ").strip()
			if new_condition:
				book["condition"] = new_condition			
		case "5":
			new_rating = input("Enter new rating: ").strip()
			if new_rating:
				book["rating"] = new_rating
		case "6":
			new_status = input("Enter new status (ex. Read,Unread,TBR): ").strip()
			if new_status:
				book["status"] = new_status
		case "7":
			print("Edit cancelled.")
			return
		case _:
			print("Invalid choice.")
			return
			
	save_library(library, filename)
	divider()
	print("Book updated.")
# --- Main loop ---

def main():
	print("Welcome to your personal library database!")
	while True:
			divider()
			print("1. Add Book (by ISBN)")
			print("2. Show current library")
			print("3. Search your library")
			print("4. Remove Book")
			print("5. Edit Book")
			print("6. Save & Exit")
			divider()
			
			menu_input = input("Select option: ")
			match menu_input:
				case "1": # Add book
					add_book()
				case "2": # View library
					view_library()
				case "3": # Search library
					search_input = input("Enter ISBN, Title, or Author: ").strip()
					found_books = search_books(search_input)
					if found_books:
						divider()
						for book in found_books:
							print(f"{book['title']} by {book['author']} {book['binding']} {book['binding'].upper()} (ISBN: {book['isbn']}) ")
					else:
						divider()
						print("No books in your library match your search.")
				case "4": # Delete book
					delete_book()
				case "5":
					edit_book()
				case "6": # Exit
					return
				case _: # Invalid input
					continue
						

if __name__ == "__main__":
	main()