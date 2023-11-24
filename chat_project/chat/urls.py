from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('ws/', include('chat.routing')),
    path('signup/',views.UserCreate.as_view()),
    path('login/',views.LoginView.as_view()),
    path('chat/',views.RoomView.as_view()),
    path('tryToken/',views.tryToken),
    path('logout/',views.LogoutView.as_view()),
    path('searchUser/',views.searchUsers),
    path('message/<int:id_room>/',views.MessageView.as_view())

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

