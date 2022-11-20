from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm

# Create your views here.


@login_required
def image_create(request):
    if request.method == "POST":
        # If form data is posted
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # When form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, "Image added successfully")
            # Redirect to the newly created item detail view
            return redirect(new_image.get_absolute_url())
        else:
            # Build form with data
            form = ImageCreateForm(data=request.GET)
        return render(
            request, "images/image/create.html", {"section": "images", "form": form}
        )
