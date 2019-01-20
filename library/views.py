from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from library.models import Configuration
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from functools import reduce

import datetime
import operator


from django.db.models import Q
from library.models import Book, Copy, Loan
from library.forms import RenewLoanForm, ReturnLoanForm, IssueFindUserForm, IssueToUserForm

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
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'library.add_book'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'library.change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'library.delete_book'

class BookSearchListView(BookListView):

     def get_queryset(self):
        result = super(BookSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(author__icontains=q) for q in query_list))
            )

        return result


class CopyCreate(PermissionRequiredMixin, CreateView):
    model = Copy
    fields = '__all__'
    permission_required = 'library.add_copy'

class CopyUpdate(PermissionRequiredMixin, UpdateView):
    model = Copy
    fields = '__all__'
    permission_required = 'library.change_copy'

class CopyDelete(PermissionRequiredMixin, DeleteView):
    model = Copy
    success_url = reverse_lazy('books')
    permission_required = 'library.delete_copy'

#class ConfigurationUpdate(PermissionRequiredMixin, UpdateView):
#    model = Configuration
#    fields = '__all__'
#    permission_required = 'library.change_configuration'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Loan
    template_name ='library/loan_list_user.html'

    def get_queryset(self):
        return Loan.objects.filter(borrower=self.request.user).filter(date_returned__isnull=True).order_by('return_due')

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = Loan
    permission_required = 'library.can_view_all_loans'
    template_name ='library/loan_list_all.html'
    paginate_by = 10

    def get_queryset(self):
        return Loan.objects.filter(date_returned__isnull=True).order_by('return_due')

class LoanedBooksAllOpenClosedListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = Loan
    permission_required = 'library.can_view_all_loans'
    template_name ='library/loan_list_all_open_closed.html'
    paginate_by = 10

    def get_queryset(self):
        return Loan.objects.filter(date_returned__isnull=True).order_by('return_due')

    def get_context_data(self, *args, **kwargs):
        context = super(LoanedBooksAllOpenClosedListView, self).get_context_data(*args, **kwargs)
        context['closed_loan_list'] = Loan.objects.filter(date_returned__isnull=False).order_by('-date_returned')
        return context

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
            return HttpResponseRedirect(reverse('all_loans') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewLoanForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'loan': loan,
    }

    return render(request, 'library/loan_renew_librarian.html', context)

@permission_required('library.can_mark_returned')
def return_loan_librarian(request, pk):
    """View function for returning a specific Loan by librarian."""
    loan = get_object_or_404(Loan, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ReturnLoanForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            loan.date_returned = form.cleaned_data['return_date']
            loan.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all_loans') )

    # If this is a GET (or any other method) create the default form.
    else:
        form = ReturnLoanForm(initial={'return_date': datetime.date.today()})

    context = {
        'form': form,
        'loan': loan,
    }

    return render(request, 'library/loan_return_librarian.html', context)

class LoanCreate(PermissionRequiredMixin, CreateView):
    model = Loan
    fields = '__all__'
    permission_required = 'library.add_loan'

    def get_initial(self):
        initial = super(LoanCreate, self).get_initial()
        initial['loan_start'] = datetime.date.today()
        initial['return_due'] = datetime.date.today() + datetime.timedelta(weeks=3)
        return initial


class LoanUpdate(PermissionRequiredMixin, UpdateView):
    model = Loan
    fields = '__all__'
    permission_required = 'library.change_loan'

class LoanDelete(PermissionRequiredMixin, DeleteView):
    model = Loan
    success_url = reverse_lazy('all_loans')
    permission_required = 'library.delete_loan'

@permission_required('library.can_mark_loaned')
def issue_find_user(request):
    """View function for issuing a book copy by librarian."""

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = IssueFindUserForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('issue_to_user', args=[form.cleaned_data['selected_user'].pk]) )

    # If this is a GET (or any other method) create the default form.
    else:
        form = IssueFindUserForm()

    context = {
        'form': form,
    }

    return render(request, 'library/issue_find_user.html', context)

@permission_required('library.can_mark_loaned')
def issue_to_user(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user_loans = Loan.objects.filter(borrower=user)
    open_loans = user_loans.filter(date_returned__isnull=True).order_by('return_due')
    returned_loans = user_loans.filter(date_returned__isnull=False).order_by('date_returned')

    configuration = get_object_or_404(Configuration)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = IssueToUserForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            loan = Loan(loaned_copy = Copy.objects.get(pk=form.cleaned_data['selected_copy']),
                borrower = user,
                loan_start = datetime.date.today(),
                return_due = form.cleaned_data['return_due'],
                )
            loan.save()

            # redirect to a new URL:
            # return HttpResponseRedirect(reverse('all-loans'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = IssueToUserForm(initial={'return_due': datetime.date.today() + datetime.timedelta(weeks=3)})

    context = {
        'form': form,
        'user': user,
        'open_loans': open_loans,
        'returned_loans': returned_loans,
        'configuration': configuration,
    }

    return render(request, 'library/issue_to_user.html', context)
