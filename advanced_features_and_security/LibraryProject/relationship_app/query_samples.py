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

    # 1. Query all books by a specific author.
    print("1. Books by a specific author:")
    author_name = 'J.R.R. Tolkien'
    author = Author.objects.get(name=author_name)
    author_books = Book.objects.filter(author=author)
    print(f"Books by {author_name}:")
    for book in author_books:
        print(f"- {book.title}")

    # 2. List all books in a library.
    print("\n2. Books in a specific library:")
    library_name = 'Central Library'
    specific_library = Library.objects.get(name=library_name)
    print(f"Books in {library_name}:")
    for book in specific_library.books.all():
        print(f"- {book.title}")

    # 3. Retrieve the librarian for a library.
    print("\n3. Librarian for a specific library:")
    # First, we still need to get the library object to filter by.
    library_object = Library.objects.get(name='Central Library')
    # Now, perform the query on the Librarian model
    librarian = Librarian.objects.get(library=library_object)
    print(f"Librarian for {library_object.name}: {librarian.name}")


if __name__ == '__main__':
    # This allows running the script directly like `python relationship_app/query_samples.py`
    # after the initial setup.
    print("Running sample queries...")
    run_queries()