from rest_framework import permissions

class LessonCoursePermission(permissions.BasePermission):
    """
    Модератор может только смотреть и редактировать любые объекты,
    обычный пользователь — только свои.
    """

    def has_permission(self, request, view):
        user = request.user
        is_moderator = user.groups.filter(name="Модераторы").exists()
        # Модератор не может создавать
        if is_moderator and request.method == 'POST':
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_moderator = user.groups.filter(name="Модераторы").exists()

        if is_moderator:
            # Модератор может смотреть и редактировать
            if request.method in permissions.SAFE_METHODS or request.method in ('PUT', 'PATCH'):
                return True
            return False  # нельзя удалять

        # Обычный пользователь — только свои объекты
        return hasattr(obj, 'owner') and obj.owner == user
