from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape
import re

class ExampleForm(forms.Form):
    """
    Example form demonstrating security best practices including:
    - Input validation and sanitization
    - XSS prevention through proper escaping
    - CSRF protection (handled by Django when {% csrf_token %} is used)
    """
    
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        }),
        help_text="Enter your full name (letters and spaces only)"
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        help_text="Enter a valid email address"
    )
    
    message = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message'
        }),
        help_text="Enter your message (max 1000 characters)"
    )
    
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        }),
        help_text="Enter your age (optional, 1-120)"
    )

    def clean_name(self):
        """
        Custom validation for name field to prevent XSS and ensure only valid characters.
        """
        name = self.cleaned_data.get('name')
        if name:
            # Remove any HTML tags and escape special characters
            name = escape(name.strip())
            
            # Only allow letters, spaces, hyphens, and apostrophes
            if not re.match(r"^[a-zA-Z\s\-']+$", name):
                raise ValidationError(
                    "Name can only contain letters, spaces, hyphens, and apostrophes."
                )
            
            # Check for potential script injection attempts
            dangerous_patterns = ['<script', 'javascript:', 'onload=', 'onerror=']
            name_lower = name.lower()
            for pattern in dangerous_patterns:
                if pattern in name_lower:
                    raise ValidationError(
                        "Invalid characters detected in name."
                    )
        
        return name

    def clean_message(self):
        """
        Custom validation for message field to prevent XSS attacks.
        """
        message = self.cleaned_data.get('message')
        if message:
            # Escape HTML characters to prevent XSS
            message = escape(message.strip())
            
            # Check for potential script injection attempts
            dangerous_patterns = [
                '<script', '</script>', 'javascript:', 'onload=', 'onerror=',
                'onclick=', 'onmouseover=', '<iframe', '<object', '<embed'
            ]
            message_lower = message.lower()
            for pattern in dangerous_patterns:
                if pattern in message_lower:
                    raise ValidationError(
                        "Message contains potentially dangerous content."
                    )
            
            # Check for SQL injection patterns
            sql_patterns = [
                'union select', 'drop table', 'delete from', 'insert into',
                'update set', '--', ';--', '/*', '*/'
            ]
            for pattern in sql_patterns:
                if pattern in message_lower:
                    raise ValidationError(
                        "Message contains invalid content."
                    )
        
        return message

    def clean_email(self):
        """
        Additional email validation beyond Django's built-in EmailField validation.
        """
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
            
            # Additional security check for email
            if len(email) > 254:  # RFC 5321 limit
                raise ValidationError("Email address is too long.")
            
            # Check for potential injection attempts in email
            dangerous_chars = ['<', '>', '"', "'", '&', ';']
            for char in dangerous_chars:
                if char in email:
                    raise ValidationError("Email contains invalid characters.")
        
        return email

    def clean(self):
        """
        Form-level validation to ensure overall data integrity.
        """
        cleaned_data = super().clean()
        
        # Additional cross-field validation can be added here
        name = cleaned_data.get('name')
        message = cleaned_data.get('message')
        
        # Example: Ensure name and message are not identical (spam prevention)
        if name and message and name.lower() == message.lower():
            raise ValidationError(
                "Name and message cannot be identical."
            )
        
        return cleaned_data
