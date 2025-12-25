from rest_framework import serializers
from members.models.member import Member
from datetime import date


class MemberSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,   # 🔥 NOT required on update
        min_length=6
    )

    class Meta:
        model = Member
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "date_of_birth",
            "marital_status",
            "gender",
            "occupation",
            "address",
            "password",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    # 🔐 CREATE (REGISTRATION)
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = Member.objects.create(**validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    # 🔐 UPDATE (PROFILE EDIT)
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

    # ✅ VALIDATIONS

    def validate_email(self, value):
        qs = Member.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A member with this email already exists."
            )
        return value

    def validate_date_of_birth(self, value):
        if value and value > date.today():
            raise serializers.ValidationError(
                "Date of birth can't be in the future."
            )
        return value
