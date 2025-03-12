import streamlit as st
import os
import sqlite3

# Database file
DB_FILE = "library.db"
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

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        genre TEXT,
        read_status BOOLEAN,
        rating INTEGER,
        favorite BOOLEAN,
        cover_image TEXT
    )''')
    conn.commit()
    conn.close()

# Function to add a book
def add_book():
    st.title("Personal Library Manager")
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
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO books (title, author, year, genre, read_status, rating, favorite, cover_image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (title, author, year, genre, read_status == "Yes", rating, favorite, cover_filename))
            conn.commit()
            conn.close()
            st.success("Book added successfully!")
        else:
            st.error("Please fill in all fields.")

# Function to remove a book
def remove_book():
    st.subheader("Remove a Book")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM books")
    books = cursor.fetchall()
    conn.close()
    
    if books:
        titles = {str(book[0]) + " - " + book[1]: book[0] for book in books}
        selected_book = st.selectbox("Select a book to remove", list(titles.keys()))
        if st.button("Remove Book"):
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = ?", (titles[selected_book],))
            conn.commit()
            conn.close()
            st.success("Book removed successfully!")
    else:
        st.warning("Your library is empty.")

# Function to search for a book
def search_book():
    st.subheader("Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author", "Genre"])
    search_term = st.text_input(f"Enter the {search_by.lower()}")
    if st.button("Search"):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        query = f"SELECT * FROM books WHERE {search_by.lower()} LIKE ?"
        cursor.execute(query, (f"%{search_term}%",))
        books = cursor.fetchall()
        conn.close()
        
        if books:
            st.write("Matching Books:")
            for book in books:
                st.write(f"- {book[1]} by {book[2]} ({book[3]}) - {book[4]} - {'Read' if book[5] else 'Unread'} - Rating: {book[6]} {'(Favorite)' if book[7] else ''}")
        else:
            st.warning("No matching books found.")

# Function to display all books
def display_books():
    st.subheader("Your Library")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    
    if books:
        for i, book in enumerate(books, 1):
            st.write(f"{i}. {book[1]} by {book[2]} ({book[3]}) - {book[4]} - {'Read' if book[5] else 'Unread'} - Rating: {book[6]} {'(Favorite)' if book[7] else ''}")
    else:
        st.warning("Your library is empty.")

# Function to display statistics
def display_statistics():
    st.subheader("Library Statistics")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(read_status), SUM(favorite) FROM books")
    total_books, read_books, favorite_books = cursor.fetchone()
    conn.close()
    
    if total_books == 0:
        st.warning("No books in the library.")
        return
    
    st.write(f"Total books: {total_books}")
    st.write(f"Books read: {read_books} ({(read_books/total_books)*100:.1f}% if total_books else 0%)")
    st.write(f"Favorite books: {favorite_books}")

# Sidebar enhancements
st.sidebar.title("Navigation")
st.sidebar.markdown("**About the App**")
st.sidebar.text("This app helps you manage your personal library.")
st.sidebar.markdown("**Features:**\n- Add and remove books\n- Search books by title, author, or genre\n- View book covers\n- Track read status and favorite books\n- Rate books and view statistics")


# Main function
def main():
    init_db()
    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add a Book":
        add_book()
    elif choice == "Remove a Book":
        remove_book()
    elif choice == "Search for a Book":
        search_book()
    elif choice == "Display All Books":
        display_books()
    elif choice == "Display Statistics":
        display_statistics()

if __name__ == "__main__":
    main()
