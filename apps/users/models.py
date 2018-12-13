# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pw = request.POST['pw']
        pw_confirm = request.POST['pw_confirm']

        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email

        errors = {}
        if len(first_name) < 2 or len(last_name) < 2 or not first_name.isalpha() or not last_name.isalpha():
            errors['names'] = 'First and last names must be at least 2 characters and only contain letters!'
        
        if len(email) < 1:
            errors['email'] = 'Email cannot be blank!'
        elif not EMAIL_REGEX.match(email):
            errors['email'] = 'Invalid email address!'
        
        if len(pw) < 8:
            errors['pw'] = 'Password must be at least 8 characters!'
        
        if pw != pw_confirm:
            errors['pw_confirm'] = 'Passwords don\'t match!'

        return errors

class BookManager(models.Manager):
    def book_validator(self, request):
        book_title = request.POST['book_title']
        request.session['book_title'] = book_title

        errors = {}
        if len(book_title) < 1:
            errors['book_title'] = 'Book title cannot be blank!'

        if request.POST['author_name_list'] == 'custom':
            author_name = request.POST['author_name']
            request.session['author_name'] = author_name
            if len(author_name) < 2:
                errors['author_name'] = 'Author name must be at least 2 characters!'

        return errors

class ReviewManager(models.Manager):
    def review_validator(self, request):
        review = request.POST['review']
        request.session['review'] = review

        errors = {}
        if len(review) < 1:
            errors['review'] = 'Review cannot be blank!'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    objects = UserManager()
    pw = models.CharField(max_length=255)
    def __repr__(self):
        return "<User object: {} {}>".format(self.first_name, self.last_name)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    def __repr__(self):
        return "<Book object: {}>".format(self.title)

class Review(models.Model):
    review = models.TextField()
    rating = models.PositiveSmallIntegerField()
    book = models.ForeignKey(Book, related_name="reviews")
    user = models.ForeignKey(User, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()
    def __repr__(self):
        return "<Review object: {}>".format(self.book)
