from django.db import models
from urllib.parse import urlparse, parse_qs

# Create your models here.
from ckeditor_uploader.fields import RichTextUploadingField

class Profile(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)




class Section(models.Model):  # Раздел
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class SubSection(models.Model):  # Подраздел
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="subsections")
    title = models.CharField(max_length=200)
    

    def __str__(self):
        return f"{self.section.title} → {self.title}"

class Lesson(models.Model):  # Урок
    subsection = models.ForeignKey(SubSection, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()  # CKEditor
    video_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0, verbose_name="Реті")

    class Meta:
        ordering = ['order']

    

    def youtube_id(self):
        """Извлекает ID видео из URL YouTube"""
        if "youtube.com" in self.video_url:
            query = parse_qs(urlparse(self.video_url).query)
            return query.get("v", [None])[0]
        elif "youtu.be" in self.video_url:
            return self.video_url.split("/")[-1]
        return None

    def thumbnail_url(self):
        """Формирует URL для превью"""
        vid = self.youtube_id()
        if vid:
            return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        return None

    def embed_url(self):
        """Формирует embed-ссылку"""
        vid = self.youtube_id()
        if vid:
            return f"https://www.youtube.com/embed/{vid}"
        return None

    def __str__(self):
        return self.title
    


    def __str__(self):
        return f"{self.subsection.title} → {self.title}"


# users/models.py (или туда, где у тебя Section/SubSection/Lesson)

class Quiz(models.Model):
    subsection = models.ForeignKey(SubSection, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"Тест: {self.title} ({self.subsection.title})"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    image = models.ImageField(upload_to="questions/", blank=True, null=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'правильный' if self.is_correct else 'неправильный'})"



#models.py
class FlashCard(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="flashcards")
    title = models.CharField(default="Флэш-карты", max_length=200)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    question_image = models.ImageField(upload_to="flashcards/questions/", blank=True, null=True)
    answer_image = models.ImageField(upload_to="flashcards/answers/", blank=True, null=True)

    def __str__(self):
        return f"{self.lesson.title} — {self.question}"







from django.db import models
from django.contrib.auth.models import User


class LessonLike(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("lesson", "user")  # чтобы один пользователь лайкал только один раз
