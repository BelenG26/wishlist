#from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseForbidden
from django.contrib import messages




# Create your views here.
@login_required
def place_list(request): # called by django

    if request.method == 'POST':
        # create new place, from request
        form = NewPlaceForm(request.POST) # creating a form from data
        place = form.save(commit=False)# creating a model object
        place.user = request.user
        if form.is_valid(): # validation againsts Db constraints
            place.save() # saves place to db
            return redirect('place_list') # reloads home page

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})# combine all to create web

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        #place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk) # if not found would return a 404 error
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list') # redirects to wishlist places

@login_required
def place_details(request, place_pk):
    place =get_object_or_404(Place,pk=place_pk)
    #place belongs to current user?
    if place.user != request.user:
        return HttpResponseForbidden()
    # if POST request, validates form date and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place) #put data user has sent, to update model
        if form.is_valid(): #are all files required filled in by database
            form.save()
            messages.info(request, 'Trip information uodated!')# temporary message for user
        else:
            messages.error(request, form.errors) # temporary

        return redirect('place_details', place_pk=place_pk)
        #if GET request, show place info and form. Form shown only if place is visited
    else:
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk) # would get a 404 error if can't find request
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()

@login_required
def about(request):
    author = 'Clara'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
