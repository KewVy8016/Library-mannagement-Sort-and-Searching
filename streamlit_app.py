import streamlit as st
import json
import sys
import os
from pathlib import Path

# Add LibraryManagement directory to path
sys.path.insert(0, str(Path(__file__).parent / "LibraryManagement"))

from models.book import Book
from algorithms.sorting import SortingAlgorithms
from algorithms.searching import SearchAlgorithms

# Page Configuration
st.set_page_config(
    page_title="📚 Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .book-card {
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #1f77b4;
        margin: 10px 0;
        background-color: #f0f8ff;
    }
    .book-title {
        font-size: 18px;
        font-weight: bold;
        color: #1f77b4;
    }
    .book-info {
        font-size: 14px;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_resource
def load_library_data():
    """Load library data from JSON file"""
    data_file = Path(__file__).parent / "library_data.json"
    
    if data_file.exists():
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                books = [Book(**book_data) for book_data in data]
                return books
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return []
    return []

# Save data function
def save_library_data(books):
    """Save library data to JSON file"""
    data_file = Path(__file__).parent / "library_data.json"
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            data = [book.to_dict() for book in books]
            json.dump(data, f, ensure_ascii=False, indent=2)
        st.success("✅ Data saved successfully!")
        st.cache_resource.clear()  # Clear cache to reload data
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Display book card
def display_book_card(book):
    """Display individual book information"""
    st.markdown(f"""
    <div class="book-card">
        <div class="book-title">📖 {book.title}</div>
        <div class="book-info">
            <b>ISBN:</b> {book.isbn}<br>
            <b>Author:</b> {book.author}<br>
            <b>Published Year:</b> {book.publish_year}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main App
st.title("📚 Library Management System")
st.markdown("---")

# Initialize books from session state
if 'books' not in st.session_state:
    st.session_state.books = load_library_data()

# Sidebar Navigation
with st.sidebar:
    st.header("🔍 Navigation")
    page = st.radio(
        "Select Page:",
        ["📊 Dashboard", "🔍 Search Books", "📑 Sort Books", "➕ Add Book", "📖 All Books"]
    )

# Dashboard Page
if page == "📊 Dashboard":
    st.header("Dashboard")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Books", len(st.session_state.books))
    
    with col2:
        unique_authors = len(set(book.author for book in st.session_state.books))
        st.metric("Authors", unique_authors)
    
    with col3:
        if st.session_state.books:
            latest_year = max(book.publish_year for book in st.session_state.books)
            st.metric("Latest Year", latest_year)
        else:
            st.metric("Latest Year", "N/A")
    
    st.markdown("---")
    st.subheader("📊 Statistics")
    
    if st.session_state.books:
        # Books by year
        years = {}
        for book in st.session_state.books:
            year = book.publish_year
            years[year] = years.get(year, 0) + 1
        
        st.bar_chart(years)
    else:
        st.info("No books in the library yet!")

# Search Books Page
elif page == "🔍 Search Books":
    st.header("Search Books")
    
    search_type = st.selectbox(
        "Search by:",
        ["Title", "Author", "ISBN", "Year"]
    )
    
    search_term = st.text_input("Enter search term:")
    
    if search_term:
        results = []
        search_term_lower = search_term.lower()
        
        for book in st.session_state.books:
            if search_type == "Title" and search_term_lower in book.title.lower():
                results.append(book)
            elif search_type == "Author" and search_term_lower in book.author.lower():
                results.append(book)
            elif search_type == "ISBN" and book.isbn == search_term:
                results.append(book)
            elif search_type == "Year" and str(book.publish_year) == search_term:
                results.append(book)
        
        st.subheader(f"Search Results ({len(results)} found)")
        
        if results:
            for book in results:
                display_book_card(book)
        else:
            st.warning(f"No books found matching '{search_term}'")
    else:
        st.info("Enter a search term to find books")

# Sort Books Page
elif page == "📑 Sort Books":
    st.header("Sort Books")
    
    if st.session_state.books:
        sort_by = st.selectbox(
            "Sort by:",
            ["Title (A-Z)", "Author (A-Z)", "Year (Oldest)", "Year (Newest)", "ISBN"]
        )
        
        sorted_books = st.session_state.books.copy()
        
        if sort_by == "Title (A-Z)":
            sorted_books.sort(key=lambda x: x.title)
        elif sort_by == "Author (A-Z)":
            sorted_books.sort(key=lambda x: x.author)
        elif sort_by == "Year (Oldest)":
            sorted_books.sort(key=lambda x: x.publish_year)
        elif sort_by == "Year (Newest)":
            sorted_books.sort(key=lambda x: x.publish_year, reverse=True)
        elif sort_by == "ISBN":
            sorted_books.sort(key=lambda x: x.isbn)
        
        st.subheader(f"Total Books: {len(sorted_books)}")
        
        for book in sorted_books:
            display_book_card(book)
    else:
        st.info("No books in the library to sort!")

# Add Book Page
elif page == "➕ Add Book":
    st.header("Add New Book")
    
    with st.form("add_book_form"):
        isbn = st.text_input("ISBN:", placeholder="e.g., 0001")
        title = st.text_input("Title:", placeholder="e.g., Python Programming")
        author = st.text_input("Author:", placeholder="e.g., John Doe")
        publish_year = st.number_input("Publish Year:", min_value=1900, max_value=2100, value=2024)
        
        submit_button = st.form_submit_button("➕ Add Book", use_container_width=True)
        
        if submit_button:
            # Validate ISBN is unique
            if any(book.isbn == isbn for book in st.session_state.books):
                st.error("❌ ISBN already exists!")
            elif not isbn or not title or not author:
                st.error("❌ Please fill in all fields!")
            else:
                new_book = Book(isbn, title, author, publish_year)
                st.session_state.books.append(new_book)
                save_library_data(st.session_state.books)
                st.success(f"✅ Book '{title}' added successfully!")

# All Books Page
elif page == "📖 All Books":
    st.header("All Books in Library")
    
    if st.session_state.books:
        st.subheader(f"Total: {len(st.session_state.books)} books")
        
        # Create a table view
        cols = st.columns([2, 2, 2, 1])
        with cols[0]:
            st.write("**Title**")
        with cols[1]:
            st.write("**Author**")
        with cols[2]:
            st.write("**ISBN**")
        with cols[3]:
            st.write("**Year**")
        
        st.divider()
        
        for book in st.session_state.books:
            cols = st.columns([2, 2, 2, 1])
            with cols[0]:
                st.write(book.title)
            with cols[1]:
                st.write(book.author)
            with cols[2]:
                st.write(book.isbn)
            with cols[3]:
                st.write(book.publish_year)
        
        # Export option
        st.markdown("---")
        if st.button("📥 Export as JSON"):
            json_data = json.dumps([book.to_dict() for book in st.session_state.books], ensure_ascii=False, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="library_data.json",
                mime="application/json"
            )
    else:
        st.info("📭 No books in the library yet! Go to 'Add Book' to add your first book.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    Library Management System | Powered by Streamlit
</div>
""", unsafe_allow_html=True)
