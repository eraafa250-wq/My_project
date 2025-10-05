from django.urls import path
from . import views
from users import views 


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("lesson/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("lesson/<int:lesson_id>/flashcards/", views.flashcards_view, name="flashcards"),
    path('lesson/<int:lesson_id>/like/', views.toggle_like, name='lesson_like'), 
    path("", views.course_list, name="course_list"),
    path("section/<int:section_id>/", views.section_detail, name="section_detail"),
    path("subsection/<int:subsection_id>/", views.subsection_detail, name="subsection_detail"),
    path("subsection/<int:subsection_id>/quiz/", views.quiz_view, name="quiz_view"),


] 





