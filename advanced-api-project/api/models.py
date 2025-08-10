from django.db import models


class Author(models.Model):
    """
    Author model representing book authors.

    This model stores basic information about authors and establishes
    a one-to-many relationship with the Book model (one author can have many books).
    """
    name = models.CharField(max_length=100, help_text="The author's full name")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing individual books in the library.

    This model stores book information and links to an Author through
    a foreign key relationship. Each book belongs to one author, but
    an author can have multiple books.
    """
    title = models.CharField(max_length=200, help_text="The book's title")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author who wrote this book"
    )

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    class Meta:
        ordering = ['title']
        unique_together = ['title', 'author']  # Prevent duplicate books by same author
