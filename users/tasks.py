from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()


@shared_task
def check_inactive_users():
    """Блокировка пользователей, которые не заходили более месяца"""
    one_month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True
    )

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    return f"Заблокировано {count} неактивных пользователей"