from rest_framework import permissions

class LessonCoursePermission(permissions.BasePermission):
    """
    Модератор
может только смотреть и редактировать любые объекты,
    обычный пользователь — только свои.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        is_moderator = user.groups.filter(name="Модераторы").exists()

        if is_moderator:
            if request.method in permissions.SAFE_METHODS or request.method in ('PUT', 'PATCH'):
                return True
            return False  # нельзя создавать и удалять
        # Не модератор: только свои объекты
        return obj.owner == user