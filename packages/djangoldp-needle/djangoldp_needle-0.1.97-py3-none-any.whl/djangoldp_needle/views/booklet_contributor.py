from django.core.exceptions import ObjectDoesNotExist
from djangoldp.serializers import LDPSerializer
from djangoldp.views import LDPViewSet

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from ..models import Booklet, Annotation, BookletContributor

def validate_user_edit_permission(user, booklet_contributor, new_attrs = None):
    booklet = booklet_contributor.booklet

    try:
        user_booklet_contributor = BookletContributor.objects.filter(user=user, booklet=booklet).get()
    except ObjectDoesNotExist:
        raise ValidationError('L\'utilisateur doit être contributeur au carnet')

    if user_booklet_contributor.role not in (BookletContributor.ROLE_ADMIN, BookletContributor.ROLE_OWNER):
        raise ValidationError('L\'utilisateur doit être au moins administrateur du carnet')

    if booklet_contributor.role == BookletContributor.ROLE_OWNER and user_booklet_contributor.role == BookletContributor.ROLE_ADMIN:
        raise ValidationError('Impossible de modifier un propriétaire en étant admin')

    if booklet_contributor.user == user \
            and booklet_contributor.role == BookletContributor.ROLE_OWNER \
            and BookletContributor.objects.filter(booklet=booklet, role=BookletContributor.ROLE_OWNER).count() <= 1:
        raise ValidationError('Un propriétaire ne peux pas se supprimer d\'un carnet')

    if new_attrs is not None and new_attrs['role'] == BookletContributor.ROLE_OWNER and user_booklet_contributor.role == BookletContributor.ROLE_ADMIN:
        raise ValidationError('Impossible d\'ajouter un propriétaire en étant admin')

class BookletContributorSerializer(LDPSerializer):
    with_cache = False

    def validate(self, attrs):
        current_user = self.context['request'].user

        validate_user_edit_permission(current_user, self.instance, attrs)

        return attrs

class BookletContributorViewset(LDPViewSet):
    serializer_class = BookletContributorSerializer

    def perform_destroy(self, instance):
        validate_user_edit_permission(self.request.user, instance)
        instance.delete()
