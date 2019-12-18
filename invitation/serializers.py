from django.utils import timezone
from django.core.mail import send_mail
from rest_framework import serializers
from invitation.models import Invitation
from invitation.common import send_mail


class InvitationSerializer(serializers.ModelSerializer):
    seconds = serializers.SerializerMethodField()
    creatorEmail = serializers.SerializerMethodField()
    creatorFullname = serializers.SerializerMethodField()
    createdTime = serializers.DateTimeField(
        source='created_time', default=timezone.now, read_only=True)

    class Meta:
        model = Invitation
        fields = ('id', 'createdTime', 'seconds', 'email',
                  'used', 'creatorEmail', 'creatorFullname')
        read_only_fields = ('id',)

    def get_seconds(self, obj):
        """
        Interval time between current and created_time in seconds.
        """
        return int((timezone.now() - obj.created_time).total_seconds())

    def get_creatorFullname(self, obj):
        """
        Get full name of authenticated user.
        """
        return obj.creator.get_full_name()

    def get_creatorEmail(self, obj):
        """
        Get email address of authenticated user.
        """
        return obj.creator.email

    def create(self, validated_data):
        """
        Create a new invitation with validated_data and send
        notification to relevant email.
        """
        auth_user = self.context.get('request').user
        invitation = Invitation.objects.create(
            creator=auth_user, **validated_data)

        if auth_user.email:
            # Send notification if user email is not empty.
            send_mail(
                'Invitation',  # Subject of message
                'You are successfuly invited!',  # Content of message
                auth_user.email, [invitation.email],
                fail_silently=True
            )
        return invitation

    def update(self, instance, validated_data):
        """
        Override update method because we need to send
        notification to updated invitaton email
        """
        old_email = instance.email
        updated_invitation = super(InvitationSerializer, self).update(
            instance, validated_data)
        new_email = updated_invitation.email

        if old_email and new_email and old_email != new_email:
            send_mail(
                'Invitation',  # Subject of message
                'You are successfuly invited!',  # Content of message
                instance.creator.email, [new_email],
                fail_silently=True
            )
        return updated_invitation
