from django.views import View
from django.shortcuts import render
from app.models import Client


class ClientListView(View):
    def get(self, request):
        clients = Client.objects.all()
        return render(request, "client_list.html", {"clients": clients})
