from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.exceptions import ValidationError

SCHOOL_SUBJECTS_CHOICES = [
    ("Mathematics", "Mathematics"),
    ("English", "English"),
    ("Literature", "Literature"),
    ("History", "History"),
    ("Sciences", "Sciences"),
    ("Arts", "Arts"),
    ("Chemistry", "Chemistry"),
    ("Physics", "Physics"),
    ("Biology", "Biology"),
    ("Philosophy", "Philosophy"),
    ("Computer Science", "Computer Science"),
    ("Geography", "Geography"),

]


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, default=None)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    school_subject = models.CharField(
        max_length=50, choices=SCHOOL_SUBJECTS_CHOICES)
    photo = models.ImageField(
        upload_to='teachers/', null=True, blank=True, default='teachers/default.jpg')

    def __str__(self):
        return f'Teacher {self.name} - Subject {self.school_subject}'

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return '/media/teachers/default.jpg'


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, default=None)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    photo = models.ImageField(
        upload_to='students/', null=True, blank=True, default='students/default.jpg')

    teachers = models.ManyToManyField(
        Teacher, related_name='students')
    student_status = models.BooleanField(default=False)

    def total_score(self):
        """Calculates the sum of all grades and ensures that it does not exceed 100."""
        total = sum(exam.grade for exam in self.exam.all())
        return min(total, 100)

    def total_score_by_subject(self):
        """Returns a dictionary with the sum of grades per subject."""
        subject_scores = {subject[0]: 0 for subject in SCHOOL_SUBJECTS_CHOICES}

        exams = self.exams.values('subject').annotate(total=Sum('grade'))

        for exam in exams:
            subject_scores[exam['subject']] = min(exam['total'], 100)

        return subject_scores

    @property
    def status(self):
        """Returns the student's status based on the accumulated grade."""
        return self.total_score() >= 70

    def update_status(self):
        """Updates the student's status in the database."""
        self.student_status = self.total_score() >= 70
        self.save()

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return '/media/students/default.jpg'

    def __str__(self):
        return self.name


class Exam(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="exams")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, choices=SCHOOL_SUBJECTS_CHOICES)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.student.name}: {self.grade}"

    def save(self, *args, **kwargs):
        """Ensure that teacher's subject matches the exam subject before saving."""
        if self.teacher.school_subject != self.subject:
            raise ValidationError(
                f'Teacher {self.teacher.name} is not allowed to grade {self.subject}.')
        super().save(*args, **kwargs)
