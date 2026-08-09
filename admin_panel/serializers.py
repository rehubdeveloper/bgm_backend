from rest_framework import serializers
from .models import Role, AdminActionLog

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class AdminActionLogSerializer(serializers.ModelSerializer):
    actor_email = serializers.CharField(source='actor.email', read_only=True)
    class Meta:
        model = AdminActionLog
        fields = '__all__'
