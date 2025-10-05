from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# регистрация
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу авторизуем
            return redirect('/')  # перенаправление на главную
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# вход
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# выход
def logout_view(request):
    logout(request)
    return redirect('/')


from django.shortcuts import render, get_object_or_404
from .models import Lesson



from django.shortcuts import get_object_or_404, render
from .models import Lesson




 
#viwe.py
def flashcards_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    flashcards = lesson.flashcards.all()
    return render(request, "flashcards.html", {
        "lesson": lesson,
        "flashcards": flashcards
    })


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Lesson, LessonLike

@login_required
def toggle_like(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    like, created = LessonLike.objects.get_or_create(user=request.user, lesson=lesson)
    if not created:
        # пользователь уже лайкал → удалить лайк
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({
        "liked": liked,
        "count": lesson.likes.count()
    })

from django.shortcuts import get_object_or_404, render
from users.models import Lesson

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # Ищем предыдущий и следующий урок только в этом же подразделе
    prev_lesson = (
        Lesson.objects.filter(subsection=lesson.subsection, order__lt=lesson.order)
        .order_by('-order')
        .first()
    )
    next_lesson = (
        Lesson.objects.filter(subsection=lesson.subsection, order__gt=lesson.order)
        .order_by('order')
        .first()
    )

    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
    })



from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from users.models import Section, SubSection, Lesson

# courses/views.py
def course_list(request):  # <-- точно латинская c
    sections = Section.objects.all()
    return render(request, "course_list.html", {"sections": sections})


def section_detail(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    return render(request, "section_detail.html", {"section": section})

def subsection_detail(request, subsection_id):
    subsection = get_object_or_404(SubSection, id=subsection_id)
    return render(request, "subsection_detail.html", {"subsection": subsection})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, "lesson_detail.html", {"lesson": lesson})

from django.shortcuts import render, get_object_or_404
from users.models import Section, SubSection, Lesson, Quiz

from django.shortcuts import render, get_object_or_404
from users.models import SubSection, Quiz, Answer

def quiz_view(request, subsection_id):
    subsection = get_object_or_404(SubSection, id=subsection_id)
    quiz = Quiz.objects.filter(subsection=subsection).first()

    score = None
    total = None

    if request.method == "POST":
        total = quiz.questions.count()
        score = 0

        for question in quiz.questions.all():
            selected_answer_id = request.POST.get(f"question_{question.id}")
            if selected_answer_id:
                answer = Answer.objects.get(id=selected_answer_id)
                if answer.is_correct:
                    score += 1

    return render(request, "quiz.html", {
        "subsection": subsection,
        "quiz": quiz,
        "score": score,
        "total": total,
    })



