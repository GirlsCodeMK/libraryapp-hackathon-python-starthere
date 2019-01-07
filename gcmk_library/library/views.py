from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import datetime

from library.models import Book, Copy, Loan
from library.forms import RenewLoanForm

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_copies = Copy.objects.filter(condition__in='MGWD').count()
    
    # Available books (status = 'a')
    num_copies_available = len([c for c in Copy.objects.all() if c.available])
    
    context = {
        'num_books': num_books,
        'num_copies': num_copies,
        'num_copies_available': num_copies_available,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'library.add_book'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Loan
    template_name ='library/loan_list_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Loan.objects.filter(borrower=self.request.user).filter(date_returned__isnull=True).order_by('return_due')

class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = Loan
    permission_required = 'library.can_mark_returned'
    template_name ='library/loan_list_all.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Loan.objects.filter(date_returned__isnull=True).order_by('return_due')  


@permission_required('library.can_mark_returned')
def renew_loan_librarian(request, pk):
    """View function for renewing a specific Loan by librarian."""
    loan = get_object_or_404(Loan, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewLoanForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            loan.return_due = form.cleaned_data['renewal_date']
            loan.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-loans') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewLoanForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'loan': loan,
    }

    return render(request, 'library/loan_renew_librarian.html', context)
