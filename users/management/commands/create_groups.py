from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from materials.models import Course, Lesson


class Command(BaseCommand):
    help = 'Create moderator group with permissions'

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderator_group, created = Group.objects.get_or_create(name='moderators')

        # Получаем контент-тайпы
        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)

        # Получаем разрешения
        view_course = Permission.objects.get(codename='view_course', content_type=course_ct)
        change_course = Permission.objects.get(codename='change_course', content_type=course_ct)
        view_lesson = Permission.objects.get(codename='view_lesson', content_type=lesson_ct)
        change_lesson = Permission.objects.get(codename='change_lesson', content_type=lesson_ct)

        # Добавляем разрешения в группу
        moderator_group.permissions.add(view_course, change_course, view_lesson, change_lesson)

        self.stdout.write(self.style.SUCCESS('Successfully created moderator group with permissions'))