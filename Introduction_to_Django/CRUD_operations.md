# Django ORM CRUD Operations

This document details the CRUD (Create, Retrieve, Update, Delete) operations performed on the `Book` model via the Django shell as required by the project.

---

### 1. Create Operation

**Task:** Create a `Book` instance with the title “1984”, author “George Orwell”, and publication year 1949.

**Command:**
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

**Output/Confirmation:**
The command executes successfully, creating a new `Book` object in the database. No explicit output is returned to the shell upon creation, but the object is now available for retrieval.

---

### 2. Retrieve Operation

**Task:** Retrieve and display all attributes of the book that were just created.

**Command:**
```python
from bookshelf.models import Book
retrieved_book = Book.objects.get(title="1984")
print(f"Title: {retrieved_book.title}, Author: {retrieved_book.author}, Year: {retrieved_book.publication_year}")
```

**Output/Confirmation:**
```
Title: 1984, Author: George Orwell, Year: 1949
```

---

### 3. Update Operation

**Task:** Update the title of "1984" to "Nineteen Eighty-Four" and save the changes.

**Command:**
```python
from bookshelf.models import Book
book_to_update = Book.objects.get(title="1984")
book_to_update.title = "Nineteen Eighty-Four"
book_to_update.save()

# Confirm the update
updated_book = Book.objects.get(id=book_to_update.id)
print(updated_book.title)
```

**Output/Confirmation:**
```
Nineteen Eighty-Four
```

---

### 4. Delete Operation

**Task:** Delete the book that was created and confirm the deletion by trying to retrieve all books again.

**Command:**
```python
from bookshelf.models import Book
book_to_delete = Book.objects.get(title="Nineteen Eighty-Four")
book_to_delete.delete()

# Confirm deletion by checking if any books are left
Book.objects.all()
```

**Output/Confirmation:**
The delete command returns the number of objects deleted and their types. The confirmation command shows an empty QuerySet, proving the book was removed.
