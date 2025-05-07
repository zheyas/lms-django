from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class ModeratorCourseLessonPermission(BasePermission):
    """
    Модератор: может читать и изменять, но не создавать и не удалять.
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name="moderators").exists():
            if request.method in ["POST", "DELETE"]:
                return False
            return True
        return True  # остальным даст право по объекту

    def has_object_permission(self, request, view, obj):
        # Модератор - только чтение/редактирование
        if request.user.groups.filter(name="moderators").exists():
            if request.method in ["DELETE"]:
                return False
            return True
        # Остальные - по владельцу
        return (
            obj.owner == request.user
            if hasattr(obj, "owner")
            else obj.course.owner == request.user
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Владельцы могут читать, редактировать и удалять только свои объекты.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(obj, "owner"):
            return obj.owner == user
        elif hasattr(obj, "course"):
            return obj.course.owner == user
        return False
