from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ('id', 'username', 'email', 'gender', 'date_of_birth', 'is_verified',)
