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
    thumbnail_dim = 200
    buf = io.BytesIO()

    original_image = Image.open(original_image)
    width, height = original_image.size
    min_dim = min(width, height)
    max_dim = max(width, height)
    if min_dim > thumbnail_dim:
        conversion_ratio = (float(max_dim) / min_dim)
    # TODO Handle a file that's already smaller than minimum size
    else:
        conversion_ratio = (float(min_dim) / max_dim)

    # Scale the thumbnail dimension, rounding up and adding 1 to ensure the minimum
    # dimension will still be greater than thumbnail_dim
    new_dim = int(round(conversion_ratio * thumbnail_dim)) + 1

    size = (new_dim, new_dim)
    original_image.thumbnail(size, Image.ANTIALIAS)

    new_width, new_height = original_image.size
    left = abs(new_width - thumbnail_dim) / 2
    top = abs(new_height - thumbnail_dim) / 2
    right = (new_width + thumbnail_dim) / 2
    bottom = (new_height + thumbnail_dim) / 2
    cropped_image = original_image.crop((left, top, right, bottom))
    cropped_image.save(buf, format='JPEG', quality=100)

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

    def form_invalid(self, form):
        print('ImageCreateView form_invalid', form.errors)
        super().form_invalid(form)


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
        self.object.thumbnail.save('my_thumbnail.jpg', ContentFile(image_data.read()))
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print('ThumbnailCreateView form_invalid', form.errors)
        super().form_invalid(form)
