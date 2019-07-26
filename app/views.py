# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
import matplotlib.pyplot as plt
from PIL import Image

from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from app import models as image_models


def generate_plot():
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def crop_image(original_image):
    buf = io.BytesIO()

    original_image = Image.open(original_image)
    new_dim = 200
    size = (new_dim, new_dim)
    original_image.thumbnail(size, Image.ANTIALIAS)

    original_image.save(buf, format='JPEG', quality=100)

    buf.seek(0)
    return buf


class ImageCreateView(CreateView):
    model = image_models.ImageTest
    fields = ('name',)
    success_url = reverse_lazy('image_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        image_data = generate_plot()
        self.object.image.save('my_plot.png', ContentFile(image_data.read()))
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ImageListView(ListView):
    model = image_models.ImageTest


class ThumbnailDetailView(DetailView):
    model = image_models.ThumbnailTest
    fields = ('name', 'thumbnail')


class ThumbnailCreateView(CreateView):
    model = image_models.ThumbnailTest
    fields = ('name', 'thumbnail')

    def get_success_url(self):
        return reverse_lazy('thumbnail_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)

        image_data = crop_image(self.object.thumbnail)
        self.object.thumbnail.save('thumbnail.jpg', ContentFile(image_data.read()))
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
