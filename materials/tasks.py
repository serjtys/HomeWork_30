from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import Course, Subscription
from datetime import datetime, timedelta
from django.utils.timezone import now


@shared_task
def send_course_update_notification(course_id):
    """Отправка уведомлений об обновлении курса подписчикам"""
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)

        email_count = 0
        for subscription in subscriptions:
            try:
                send_mail(
                    subject=f'Обновление курса "{course.title}"',
                    message=f'Добрый день!\n\nКурс "{course.title}" был обновлен. Проверьте новые материалы!\n\nС уважением,\nКоманда образовательной платформы',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[subscription.user.email],
                    fail_silently=False,
                )
                email_count += 1
            except Exception as e:
                print(f"Ошибка отправки email для {subscription.user.email}: {e}")

        return f"Уведомления отправлены для курса {course.title} ({email_count} писем)"
    except Course.DoesNotExist:
        return "Курс не найден"
    except Exception as e:
        return f"Ошибка: {e}"


@shared_task
def check_course_updates():
    """Проверка обновлений курсов за последние 4 часа"""
    from materials.models import Course

    four_hours_ago = now() - timedelta(hours=4)

    # Находим курсы, у которых уроки обновлялись в последние 4 часа
    # но сам курс не обновлялся (чтобы избежать дублирования)
    updated_courses = Course.objects.filter(
        lessons__updated_at__gte=four_hours_ago,
        updated_at__lt=four_hours_ago
    ).distinct()

    task_count = 0
    for course in updated_courses:
        send_course_update_notification.delay(course.id)
        task_count += 1

    return f"Запланировано уведомлений для {task_count} курсов"