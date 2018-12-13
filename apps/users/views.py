# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse

import bcrypt

from .models import User

def index(request):
    if 'id' in request.session:
        return redirect(reverse('books:index'))
    if 'first_name' not in request.session:
        request.session['first_name'] = ''
    if 'last_name' not in request.session:
        request.session['last_name'] = ''
    if 'email' not in request.session:
        request.session['email'] = ''
    return render(request, 'users/index.html')

def register(request):
    if request.method == 'POST':
        # FORM VALIDATION
        errors = User.objects.basic_validator(request)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')

        # CHECK IF EMAIL IS ALREADY IN DATABASE
        found_users = User.objects.filter(email=request.POST['email'])
        if found_users.count() > 0:
            messages.error(request, 'Email already taken', extra_tags='email')
            return redirect('/')

        # ADD USER TO DATABASE
        pw_hashed = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        new_user_id = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], pw=pw_hashed).id

        request.session['last_name'] = ''
        request.session['email'] = ''
        request.session['id'] = new_user_id

        return redirect(reverse('books:index'))
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        pw = request.POST['pw']
        request.session['login_email'] = email

        # FORM VALIDATION
        if len(email) < 1 or len(pw) < 1:
            messages.error(request, 'Email and/or password fields cannot be blank!')
            return redirect('/')
        
        # USER LOGIN
        users = User.objects.filter(email=email)
        if len(users) < 1:
            messages.error(request, 'No user with that email!')
            return redirect(reverse('users:index'))
        for user in users:
            if bcrypt.checkpw(pw.encode(), user.pw.encode()):
                request.session['login_email'] = ''
                request.session['id'] = user.id
                request.session['first_name'] = user.first_name
                return redirect(reverse('books:index'))
        messages.error(request, 'Wrong email/password combination!')
        return redirect('/')
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def user(request, id):
    if 'id' not in request.session:
        messages.error(request, 'Must be logged in to view')
        return redirect('/')
    user = User.objects.get(id=id)
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'total_reviews': user.reviews.count(),
        'reviews': []
    }
    reviews = user.reviews.all()
    for review in reviews:
        context['reviews'].append({
            'book_id': review.book.id,
            'book_title': review.book.title
        })
    return render(request, 'users/user.html', context)
