from django.contrib import admin
from .models import Section, SubSection, Lesson, FlashCard, Quiz, Question, Answer

# Регистрация базовых моделей
admin.site.register(Section)
admin.site.register(SubSection)

# Quiz Admin
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ('text', 'is_correct')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'text')
    inlines = [AnswerInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('text', 'image')
    show_change_link = True

class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'subsection')  # Убрал passing_score
    inlines = [QuestionInline]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

# Lesson with FlashCards
class FlashCardInline(admin.TabularInline):
    model = FlashCard
    extra = 1
    fields = ('question', 'answer',)
    can_delete = True
    show_change_link = True

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subsection')
    list_filter = ('subsection__section',)
    search_fields = ('title', 'content')
    inlines = [FlashCardInline]

@admin.register(FlashCard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'title', 'question_image', 'answer_image']
    list_filter = ('lesson__subsection',)
    search_fields = ('question', 'answer')