from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import datetime
from functools import reduce
import operator

from library.forms import RenewLoanForm, ReturnLoanForm, IssueFindUserForm, IssueToUserForm, BookSearchForm
from library.models import Book, Copy, Loan
from library.models import Configuration


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Use by calling 
# logger.warning('some message that is all one string')


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

def book_list(request):
    """View function for book search."""

    # If the form is invalid, use these definitions of what to display
    book_list = Book.objects.all()
    order_term = 'title'
    default_order = '3'

    # Complex logic as this view can be accessed in three different ways: 
    #   1. as the standard "all books" list ('q' not set, 'order' not set)
    #   2. the result of s earch on the "all books" list ('q' set, 'order' set)
    #   3. the result of a search from some other page ('q' set, 'order' not set)
    # In case 1, we create an empty form.
    # In case 3, we inlcude the default sort order in the form parameters
    # In case 2, we use the form parameters as in the request.

    if 'q' in request.GET:
        # Result of some search, case 2 or 3 as above
        form_fields = {'q': request.GET['q']}
        if 'order' in request.GET:
            # Case 2: use the given sort order
            form_fields['order'] = request.GET['order']
        else:
            # Case 3: use the default sort order
            form_fields['order'] = default_order
        form = BookSearchForm(form_fields)
    else:
        # standard "all books" search, case 1 above
        form = BookSearchForm()


    if form.is_valid():

        if 'q' in form.cleaned_data:
            q = form.cleaned_data['q']
            if q:
                query_list = q.split()
                book_list = Book.objects.filter(
                    reduce(operator.and_,
                        (Q(title__icontains=term) for term in query_list)) 
                    |
                    reduce(operator.and_,
                        (Q(author__icontains=term) for term in query_list))
                    )
        
        if 'order' in form.cleaned_data:
            order = form.cleaned_data['order']
            if order == "1":
                order_term = 'author'
            elif order == "2":
                order_term = '-author'
            elif order == "3":
                order_term = 'title'
            elif order == "4":
                order_term = '-title'

    page = request.GET.get('page', 1)
    book_list = book_list.order_by(order_term)

    paginator = Paginator(book_list, 10)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'book_search_form': form,
        'book_list': books,
        # is_a_search_result used to select the message displayed if book_list is empty
        'is_a_search_result': form.is_valid(),
        }

    return render(request, 'library/book_list.html', context=context)


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
    success_url = reverse_lazy('book_list')
    permission_required = 'library.delete_book'

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
    permission_required = 'library.delete_copy'
    # success_url = reverse_lazy('book_list')
    def get_success_url(self):
        # logger.warning('copy delete args: ' + str(self.kwargs))
        book_id = Copy.objects.get(pk=self.kwargs['pk']).book.id
        # logger.warning('copy delete, loading book: ' + str(book_id))
        return reverse_lazy('book_detail', kwargs={'pk': book_id}) # kwargs={'pk': self.kwargs['pk']})

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
