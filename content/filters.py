from rest_framework import filters
from .models import UserPost


class CurrentUserFollowingFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        followed_user = [edge.to_user for edge in request.user.profile.following.all()]

        return queryset.filter(author__in=followed_user, is_published=True)