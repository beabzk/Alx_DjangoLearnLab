from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Custom ModelAdmin class that includes configurations for the additional fields
    in the custom user model.
    """
    # Add the custom fields to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

    # Add the custom fields to the add_fieldsets for creating new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

    # Display the custom fields in the list view
    list_display = UserAdmin.list_display + ('date_of_birth',)

    # Allow filtering by date_of_birth
    list_filter = UserAdmin.list_filter + ('date_of_birth',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')

# Register the custom user model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)