from PIL import Image, ImageDraw, ImageFont, ImageFilter

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy

from gallery_app.forms import AddUserForm, AddPhotoForm, AddCommentForm, SearchForm, ImageFilterForm, TextForm
from gallery_app.models import Photo, Comment


def home(request):

    photo_list = Photo.objects.all().order_by('-created')
    paginator = Paginator(photo_list, 8)

    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    return render(request, "home.html", {"photos": photos,
                                         "page": page})


def add_user(request):

    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "add_user.html", {"form": form,
                                                     "message": "Użytkownik został utworzony."})
    else:
        form = AddUserForm()
    return render(request, "add_user.html", {"form": form})


@login_required
def add_photo(request):

    if request.method == "POST":
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            photo.username = request.user
            photo.save()
            return redirect(reverse_lazy('my-profile'))
    else:
        form = AddPhotoForm()
    return render(request, "add_photo.html", {"form": form})


@login_required
def my_profile(request):

    user = request.user
    photo_list = Photo.objects.filter(username=user).order_by('-created')
    paginator = Paginator(photo_list, 8)

    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    return render(request, "home.html", {"photos": photos,
                                         "page": page,
                                         "user": user})


@login_required
def photo_detail(request, id):

    photo = Photo.objects.get(id=id)
    comments = Comment.objects.filter(photo=photo).order_by('-created')

    if request.method == "POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            comment.username = request.user
            comment.photo = photo
            comment.save()
            return render(request, "photo_detail.html", {"photo": photo,
                                                         "form": form,
                                                         "comments": comments})
    else:
        form = AddCommentForm()
        return render(request, "photo_detail.html", {"photo": photo,
                                                     "form": form,
                                                     "comments": comments})


def photo_edit(request, id):

    obj = Photo.objects.get(id=id)

    if request.method == "POST":
        form_filter = ImageFilterForm(request.POST)
        if form_filter.is_valid():

            image = Image.open(obj.photo)
            path = "media/" + obj.photo.name
            edited_photo = ""

            if request.POST.get('select') == "blur":
                edited_photo = image.filter(ImageFilter.GaussianBlur(radius=2))
            elif request.POST.get('select') == "sharpen":
                edited_photo = image.filter(ImageFilter.SHARPEN)
            elif request.POST.get('select') == "edges":
                edited_photo = image.filter(ImageFilter.FIND_EDGES)
            elif request.POST.get('select') == "contour":
                edited_photo = image.filter(ImageFilter.CONTOUR)
            elif request.POST.get('select') == "modefilter":
                edited_photo = image.filter(ImageFilter.ModeFilter(size=5))

            edited_photo.save(path, format='jpeg')
            return redirect("/edytuj/{}".format(obj.id))

        return render(request, "photo_edit.html", {"obj": obj,
                                                   "form_filter": form_filter})
    else:
        form_filter = ImageFilterForm()
        return render(request, "photo_edit.html", {"obj": obj,
                                                   "form_filter": form_filter})


def photo_text(request, id):

    obj = Photo.objects.get(id=id)

    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            image = Image.open(obj.photo)
            draw = ImageDraw.Draw(image)
            color = ""

            if request.POST.get('select') == "black":
                color = (0, 0, 0)
            if request.POST.get('select') == "red":
                color = (255, 0, 0)
            if request.POST.get('select') == "white":
                color = (255, 255, 255)
            if request.POST.get('select') == "blue":
                color = (0, 0, 255)

            text_position = (20, 10)
            font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 40, encoding="unic")
            draw.text(text_position, text, fill=color, font=font)
            del draw

            path = "media/" + obj.photo.name
            image.save(path, format='jpeg')
            return redirect("/napis/{}".format(obj.id))

        return render(request, "photo_text.html", {"obj": obj,
                                                   "form": form})
    else:
        form = TextForm()
        return render(request, "photo_text.html", {"obj": obj,
                                                   "form": form})


def search_photo(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            result = Photo.objects.filter(title__icontains=key)
            return render(request, "search.html", {"form": form,
                                                   "result": result})
    else:
        form = SearchForm()
        return render(request, "search.html", {"form": form})


def photo_delete(request, id):

    Photo.objects.get(id=id).delete()
    return redirect(reverse_lazy('my-profile'))
