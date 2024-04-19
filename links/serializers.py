from rest_framework import serializers

from links.models import UserLink, UserLinkCollection


class UserLinkSerializer(serializers.ModelSerializer):
    """
    User link serializer
    """
    class Meta:
        model = UserLink
        fields = ('id', 'user', 'title', 'description', 'url', 'image', 'link_type', 'creation_date', 'change_date')


class UserLinkCollectionSerializer(serializers.ModelSerializer):
    """
    User link collections serializer
    """
    class Meta:
        model = UserLinkCollection
        fields = ('id', 'user', 'title', 'description', 'user_links', 'creation_date', 'change_date')
