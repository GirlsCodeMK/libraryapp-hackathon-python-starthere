from rest_framework import viewsets, filters
from rest_framework.permissions import (
    DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, 
    IsAuthenticated, IsAdminUser, BasePermission,
    )
from django_filters.rest_framework import DjangoFilterBackend
from library.serializers import BookSerializer, CopySerializer, LoanSerializer, UserSerializer

import datetime

from django.contrib.auth.models import User

from library.models import Book, Copy, Loan
from library.models import Configuration

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('library.views')


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    # filter_backends = (filters.SearchFilter,)
    filterset_fields = ('author', 'title')
    search_fields = ('author', 'title')


class CopyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows copies to be viewed or edited.
    """
    queryset = Copy.objects.all()
    serializer_class = CopySerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

class MyLoanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows loans to be viewed or edited.
    """
    # queryset = Loan.objects.all()
    def get_queryset(self):
        return_closed_loans = self.request.query_params.get('closed', 'false')
        if return_closed_loans.lower() in ['true', 't', 'yes']:
            return Loan.objects.filter(borrower=self.request.user).filter(date_returned__isnull=False).order_by('return_due')
        else:
            return Loan.objects.filter(borrower=self.request.user).filter(date_returned__isnull=True).order_by('return_due')

    serializer_class = LoanSerializer
    permission_classes = (DjangoModelPermissions,)

class LoanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows loans to be viewed or edited.
    """
    # queryset = Loan.objects.all()
    def get_queryset(self):
        return_closed_loans = self.request.query_params.get('closed', 'false')
        if return_closed_loans.lower() in ['true', 't', 'yes']:
            queryset = Loan.objects.filter(date_returned__isnull=False)
        else:
            queryset = Loan.objects.filter(date_returned__isnull=True)

        if 'borrower' in self.request.query_params:
            try:
                query_borrower_id = int(self.request.query_params['borrower'])
                queryset = queryset.filter(borrower_id=query_borrower_id)
            except ValueError:
                pass

        return queryset.order_by('return_due')

    serializer_class = LoanSerializer
    permission_classes = (DjangoModelPermissions,)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows loans to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)