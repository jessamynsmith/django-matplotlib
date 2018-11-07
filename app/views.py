# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
import matplotlib.pyplot as plt

from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from app import models as image_models


def generate_plot():
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
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
