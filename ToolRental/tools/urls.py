from django.urls import path
from . import views

app_name = 'tools'

urlpatterns = [
    path('', views.home, name='home'),
    path('tools/', views.tool_list, name='list'),
    path('tools/<int:tool_id>/', views.tool_detail, name='detail'),
    path('tools/add/', views.add_tool, name='add'),
    path('my-tools/', views.my_tools, name='my_tools'),
    path('tools/<int:tool_id>/edit/', views.edit_tool, name='edit'),
    path('categories/', views.category_list, name='categories'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('search/', views.tool_list, name='search'),
    path('detail/<int:tool_id>/', views.detail, name='detail'),
    
    # Pages statiques
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('faq/', views.faq, name='faq'),
]