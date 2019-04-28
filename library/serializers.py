from django.contrib.auth.models import User, Group
from rest_framework import serializers

from library.models import Book, Copy, Loan

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')

class LoanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Loan
        fields = ('url', 'loaned_copy', 'borrower', 
            'loan_start', 'return_due', 'date_returned')

class CopySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Copy
        fields = ('url', 'book', 'copy_number', 'condition', 'acquisition_date',
            'available', 'on_loan')

class BookSerializer(serializers.HyperlinkedModelSerializer):
    # copies = CopySerializer(many=True, required=False)
    # copy_conditions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = ('url', 'title', 'author', 'isbn', 'copy_available', 'publication_date', 'copies')
