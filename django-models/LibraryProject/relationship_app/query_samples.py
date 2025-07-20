import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Creates sample data to query against."""
    print("Creating sample data...")
    # Create Authors
    author1 = Author.objects.create(name='J.R.R. Tolkien')
    author2 = Author.objects.create(name='George R.R. Martin')

    # Create Books
    book1 = Book.objects.create(title='The Hobbit', author=author1)
    book2 = Book.objects.create(title='The Lord of the Rings', author=author1)
    book3 = Book.objects.create(title='A Game of Thrones', author=author2)

    # Create Libraries
    library1 = Library.objects.create(name='Central Library')
    library2 = Library.objects.create(name='Community Archives')

    # Add books to libraries
    library1.books.add(book1, book2)
    library2.books.add(book3)

    # Create Librarians
    Librarian.objects.create(name='Mr. Anderson', library=library1)
    Librarian.objects.create(name='Ms. Rodriguez', library=library2)
    print("Sample data created.")

def run_queries():
    """Runs the required queries and prints the results."""
    # Check if data exists, if not, create it
    if not Author.objects.exists():
        create_sample_data()

    print("\n--- Running Queries ---\n")

    # 1. Query all books by a specific author (J.R.R. Tolkien)
    print("1. Books by J.R.R. Tolkien:")
    tolkien = Author.objects.get(name='J.R.R. Tolkien')
    tolkien_books = Book.objects.filter(author=tolkien)
    for book in tolkien_books:
        print(f"- {book.title}")

    # 2. List all books in a library (Central Library)
    print("\n2. Books in Central Library:")
    central_library = Library.objects.get(name='Central Library')
    for book in central_library.books.all():
        print(f"- {book.title}")

    # 3. Retrieve the librarian for a library (Central Library)
    print("\n3. Librarian for Central Library:")
    librarian = central_library.librarian # Accessing the one-to-one relationship
    print(f"- {librarian.name}")

if __name__ == '__main__':
    run_queries()