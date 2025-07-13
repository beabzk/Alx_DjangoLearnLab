# Create Operation

**Command:**
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

**Output:**

This command creates a new Book object and saves it to the database.