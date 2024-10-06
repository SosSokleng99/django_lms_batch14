from django.db import models

from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse

# Create your models here.

# Create "Genre" Table for Book
class Genre(models.Model):

    # Define Fields/Attribute  of Genre Class
    name = models.CharField(unique=True, 
                            max_length=200,
                            help_text= "Enter a Book Genre(e.g Science, Fantasy, Non-fiction, History...)"
                            )
    
    def __str__(self):
        # String Representation of Genre Class and Needed for use in Django Admin Dashboard.
        return self.name
    
    class Meta:
        # ordering = ['name']
        # Use contraint to prevent Same Genre.name field Duplicate. E.g Science, science, SCIENCE 
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name = 'genre_name_case_insensitive_unique',
                violation_error_message = 'Genre already Exists. '
            )
        ]
    
    def get_absolute_url(self):
        """ Returns the URL to access particular genre Data based on ID."""
        return reverse("genre_detail", args=[str(self.id)])
    

class Book(models.Model):
    # Define BOOK Attribute
    title = models.CharField(max_length=300, help_text="Enter the Book Title.")
    summary = models.TextField( "Book Description",max_length=1500, help_text="Enter the Book Description.")
    isbn = models.CharField('ISBN-13', 
                               unique=True, 
                               max_length=13,
                               help_text='13 Characters <a href="https://isbnsearch.org/">ISBN Search </a>.')
    

    # A Book must have relation with Genre
    genre = models.ManyToManyField(Genre, help_text="Select a Genre or Many for the Book.")

    class Meta:
        ordering = ['id'] #If the Book Class has been Called the Tittle will be representer of BOOK table
    
    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])
    
    def __str__(self):
        return f'{self.id}. {self.title}' 
    
    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        genres = self.genre.all()  # Retrieve all genres associated with the book model
        # Create a list of genre names
        genre_names_list = [genre.name for genre in genres]
        # Join the list into a single string separated by commas
        return ', '.join(genre_names_list)
    

    display_genre.short_description = 'Genre List'
        

import uuid #Need for Generate Long-Random ID for a Book Instance
from datetime import date

from django.conf import settings

class BookInstance(models.Model):

    uniqueid = models.UUIDField(primary_key=True,
                                default=uuid.uuid4,
                                help_text="Unique ID for this Particular Book Copied in Library"
                                )
    
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book Availibility')

    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)

    class Meta:
        ordering = ['due_back', 'imprint']
    
    def __str__(self):
        return f'{self.uniqueid} [{self.book.title}]' 
    
    __str__.short_description = "Book Copied"
    
    def get_absolute_url(self):
        return reverse("bookinstance_detail", args=[str(self.id)])
    
    @property
    def is_over_due(self):
        """Determine if the Due Back Date is Over Due"""
        return bool(date.today() > self.due_back)
    
    
