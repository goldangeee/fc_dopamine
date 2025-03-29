from django.urls import path
from .views import crawl_player_data,save_html_to_file

urlpatterns = [
    path('crawl_player_data/', crawl_player_data, name='crawl_player_data'),
    path('save_html_to_file/', save_html_to_file, name='save_html_to_file'),
]
