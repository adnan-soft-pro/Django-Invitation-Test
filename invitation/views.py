from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.permissions import IsAuthenticated

from invitation.models import Invitation
from invitation.serializers import InvitationSerializer


class InvitationList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    """
    API endpoints that allows invitation to be viewed or created.
    """
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return all the invitations for the currently authenticated user.
        """
        try:
            return self.request.user.created_invitations.order_by('id').all()
        except ObjectDoesNotExist:
            raise exceptions.NotFound('Object NotFound')

    def get(self, request, *args, **kwargs):
        """
        Show list of invitation.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create a new invitation and return it.
        """
        return self.create(request, *args, **kwargs)


class InvitationDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoints that allow invitation to be patched or deleted.
    """
    serializer_class = InvitationSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        try:
            return self.request.user.created_invitations.order_by('id').all()
        except ObjectDoesNotExist:
            raise exceptions.NotFound('Object Not found.')


class ApiHome(View):
    """
    View for rest apis.
    """

    def get(self, request):
        invitations = request.user.created_invitations.all()
        html = "<h1 align=center>API</h1><hr><br><h3 align=center><a href='/'>Go Back</a><br></h3>" \
               "<h3 align=center><a href='invitations/'>Create or List Invitation</a></h3>"

        if invitations:
            id = invitations.first().id
            html += "<h3 align=center><a href='invitations/{id}/'>Patch or Delete Invitation</a></h3>".format(
                id=id)
        else:
            html += "<h3 align=center style='color:grey;'>No invitation that can be patched or deleted</h3>"
        return HttpResponse(html)


class Home(View):
    """
    View for main page.
    """

    def get(self, request):
        html = "<h1 align=center>Invitation Application</h1><hr><br>" \
               "<h3 align=center><a href='/api'>APIs List</a></h3>" \
               "<h3 align=center><a href='/admin'>Django Admin</a></h3>"
        return HttpResponse(html)
