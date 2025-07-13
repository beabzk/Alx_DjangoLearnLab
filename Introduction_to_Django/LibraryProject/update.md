# Update Operation

**Command:**
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
```

**Output:**

This updates the title of the book and saves the change to the database.