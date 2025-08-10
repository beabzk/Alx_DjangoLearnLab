from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Book model.
    
    This serializer handles the serialization and deserialization of Book instances,
    including custom validation to ensure the publication year is not in the future.
    It serializes all fields of the Book model and provides detailed validation
    for the publication_year field.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        This prevents users from entering invalid publication dates.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Author model with nested book serialization.
    
    This serializer includes the author's name and dynamically serializes
    all related books using the BookSerializer. The books field uses the
    'books' related_name from the ForeignKey relationship in the Book model.
    
    The nested serialization allows API consumers to get complete author
    information including all their books in a single API call, which is
    efficient for displaying author profiles with their complete bibliography.
    """
    
    # Nested serializer to include all books by this author
    # The 'books' field corresponds to the related_name in the Book model's ForeignKey
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def to_representation(self, instance):
        """
        Custom representation method to enhance the serialized output.
        
        This method can be used to add computed fields or modify the
        representation of the serialized data. Currently, it maintains
        the default behavior but can be extended for future requirements.
        
        Args:
            instance (Author): The Author instance being serialized
            
        Returns:
            dict: The serialized representation of the Author
        """
        representation = super().to_representation(instance)
        # Add book count for convenience
        representation['book_count'] = len(representation['books'])
        return representation
