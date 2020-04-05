from django.shortcuts import render
from django.views.generic import View

import os


class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': os.environ.get('APP_TITLE', '')
        }
        return render(request, 'core/index.html', context=context)