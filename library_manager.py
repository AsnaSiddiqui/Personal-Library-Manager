import streamlit as st
import os
import json

# File to store the library data
LIBRARY_FILE = "library.json"
COVER_DIR = "covers"
DEFAULT_COVER = {
    "Fiction": "default_fiction.jpg",
    "Non-Fiction": "default_nonfiction.jpg",
    "Mystery": "default_mystery.jpg",
    "Fantasy": "default_fantasy.jpg",
    "Science": "default_science.jpg",
    "Other": "default_other.jpg"
}

# Ensure cover directory exists
if not os.path.exists(COVER_DIR):
    os.makedirs(COVER_DIR)

# Function to load the library from a file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save the library to a file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Function to add a book
def add_book(library):
    st.title("Personal Library Manager ")
    st.subheader("Add a Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
    genre = st.text_input("Genre")
    read_status = st.radio("Have you read this book?", ["Yes", "No"])
    rating = st.slider("Rate this book (1-5)", 1, 5, 3)
    favorite = st.checkbox("Mark as Favorite")
    cover_image = st.file_uploader("Upload Book Cover (Optional)", type=["jpg", "png", "jpeg"])
    
    if st.button("Add Book"):
        if title and author and genre:
            cover_filename = ""
            if cover_image:
                cover_filename = os.path.join(COVER_DIR, cover_image.name)
                with open(cover_filename, "wb") as f:
                    f.write(cover_image.getbuffer())
            else:
                cover_filename = os.path.join(COVER_DIR, DEFAULT_COVER.get(genre, DEFAULT_COVER["Other"]))

            book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read_status": read_status == "Yes",
                "rating": rating,
                "favorite": favorite,
                "cover_image": cover_filename
            }
            library.append(book)
            save_library(library)
            st.success("Book added successfully!")
        else:
            st.error("Please fill in all fields.")

# Function to remove a book
def remove_book(library):
    st.subheader("Remove a Book")
    if library:
        titles = [book["title"] for book in library]
        title_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            library[:] = [book for book in library if book["title"] != title_to_remove]
            save_library(library)
            st.success("Book removed successfully!")
    else:
        st.warning("Your library is empty.")

# Function to search for a book
def search_book(library):
    st.subheader("Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author", "Genre"])
    search_term = st.text_input(f"Enter the {search_by.lower()}")
    if st.button("Search"):
        if search_term:
            matching_books = [book for book in library if search_term.lower() in book[search_by.lower()].lower()]
            if matching_books:
                st.write("Matching Books:")
                for book in matching_books:
                    status = "Read" if book["read_status"] else "Unread"
                    favorite = " (Favorite)" if book.get("favorite") else ""
                    if os.path.exists(book["cover_image"]):
                        st.image(book["cover_image"], width=100)
                    st.write(f"- {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status} - Rating: {book['rating']}{favorite}")
            else:
                st.warning("No matching books found.")
        else:
            st.error("Please enter a search term.")

# Function to display all books
def display_books(library):
    st.subheader("Your Library")
    if library:
        for i, book in enumerate(library, 1):
            status = "Read" if book["read_status"] else "Unread"
            favorite = " (Favorite)" if book.get("favorite") else ""
            if os.path.exists(book["cover_image"]):
                st.image(book["cover_image"], width=100)
            st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status} - Rating: {book['rating']}{favorite}")
    else:
        st.warning("Your library is empty.")

# Function to display statistics
def display_statistics(library):
    st.subheader("Library Statistics")
    total_books = len(library)
    if total_books == 0:
        st.warning("No books in the library.")
        return

    read_books = sum(book["read_status"] for book in library)
    favorite_books = sum(1 for book in library if book.get("favorite"))
    percentage_read = (read_books / total_books) * 100
    
    st.write(f"Total books: {total_books}")
    st.write(f"Books read: {read_books} ({percentage_read:.1f}%)")
    st.write(f"Favorite books: {favorite_books}")

# Sidebar enhancements
st.sidebar.title("Navigation")
st.sidebar.markdown("**About the App**")
st.sidebar.text("This app helps you manage your personal library.")
st.sidebar.markdown("**Features:**\n- Add and remove books\n- Search books by title, author, or genre\n- View book covers\n- Track read status and favorite books\n- Rate books and view statistics")


# Main function
def main():
    library = load_library()
    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add a Book":
        add_book(library)
    elif choice == "Remove a Book":
        remove_book(library)
    elif choice == "Search for a Book":
        search_book(library)
    elif choice == "Display All Books":
        display_books(library)
    elif choice == "Display Statistics":
        display_statistics(library)

if __name__ == "__main__":
    main()
