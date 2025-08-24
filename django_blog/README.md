# Django Blog Project

A comprehensive blogging platform built with Django, featuring user authentication, post management, commenting system, and advanced features like tagging and search functionality.

## Project Setup

This Django blog project includes the following features:
- User authentication (registration, login, logout, profile management)
- Blog post CRUD operations
- Comment system
- Tagging functionality
- Search capabilities
- Responsive design with Bootstrap

## Initial Setup Instructions

### 1. Project Structure
The project is organized as follows:
- `django_blog/` - Main project directory
- `blog/` - Main blog application
- `blog/models.py` - Contains the Post model
- `blog/templates/blog/` - HTML templates
- `blog/static/blog/` - CSS and static files

### 2. Database Models

#### Post Model
- `title`: CharField (max_length=200)
- `content`: TextField
- `published_date`: DateTimeField (auto_now_add=True)
- `author`: ForeignKey to User model

### 3. Running the Project

1. Navigate to the project directory:
   ```bash
   cd django_blog
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the application at: http://127.0.0.1:8000/

### 4. Admin Interface

The Post model is registered in the Django admin interface. You can access it at:
http://127.0.0.1:8000/admin/

Features in admin:
- List display showing title, author, and published date
- Filtering by published date and author
- Search functionality for title and content

### 5. Template Structure

- `base.html` - Base template with navigation and Bootstrap styling
- `home.html` - Homepage displaying latest blog posts
- Templates use Bootstrap 5 for responsive design

### 6. Static Files

- `style.css` - Custom CSS for blog styling
- Bootstrap CSS and JS included via CDN

## Next Steps

This completes Task 0: Initial Setup and Project Configuration. The foundation is now ready for implementing:
1. User authentication system
2. Blog post management features
3. Comment functionality  
4. Advanced features (tagging and search)

## Technology Stack

- Django 5.2.4
- SQLite (default database)
- Bootstrap 5
- HTML5/CSS3
