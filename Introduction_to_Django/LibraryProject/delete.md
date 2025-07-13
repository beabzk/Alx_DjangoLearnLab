# Delete Operation

**Command:**
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
```

**Output:**

This deletes the book object from the database.