from django.urls import path, include

urlpatterns = [
    path('api/', include('app.urls.livre_urls')),
]
