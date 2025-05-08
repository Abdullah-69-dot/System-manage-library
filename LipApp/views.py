from django.shortcuts import render ,redirect ,get_object_or_404
from .models import Book, Category
from .forms import BookForm, CatForm
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Q

def index(request):
    if request.method == 'POST':
        new_book = BookForm(request.POST, request.FILES)
        if new_book.is_valid():
            new_book.save()
            return redirect('index')

        new_cat = CatForm(request.POST)
        if new_cat.is_valid():
            new_cat.save()
            return redirect('index')
            
    # Get all books and apply filters if provided
    books_list = Book.objects.all()
    
    # Filter by status if provided in URL parameters
    status_filter = request.GET.get('status', None)
    if status_filter:
        books_list = books_list.filter(status=status_filter)
    
    # Filter by category if provided in URL parameters
    category_id = request.GET.get('category', None)
    if category_id and category_id.isdigit():
        books_list = books_list.filter(category_id=int(category_id))
    
    # Search by book name if provided in URL parameters
    search_query = request.GET.get('search', None)
    if search_query:
        books_list = books_list.filter(title__icontains=search_query)

    # حساب إجمالي الربح من البيع
    sold_profit = Book.objects.filter(status='sold').aggregate(
        total=Sum('price'))['total'] or 0

    # حساب الربح من الإيجار
    rental_profit = Book.objects.filter(status='rental').annotate(
        total_rent=ExpressionWrapper(
            F('retail_price_day') * F('retail_period'),
            output_field=DecimalField()
        )
    ).aggregate(total=Sum('total_rent'))['total'] or 0
    total_profit = sold_profit + rental_profit
    
    context = {
        'books': books_list,
        'category': Category.objects.all(),
        'form': BookForm(),
        'catform': CatForm(),
        'allbooks': Book.objects.filter(active=True).count(),
        'sold': Book.objects.filter(status='sold').count(),
        'rental': Book.objects.filter(status='rental').count(),
        'avalible': Book.objects.filter(status='avalible').count(),  # تأكد إنها مكتوبة كده في الـ model
        'sold_profit': float(sold_profit),
        'rental_profit': float(rental_profit),
        'total_profit': float(total_profit),
        'current_status': status_filter,
        'current_category': category_id,
        'search_query': search_query
    }

    return render(request, 'pages/index.html', context)

def books(request):
    # Get all books and categories
    books_list = Book.objects.all()
    categories = Category.objects.all()
    
    # Print all available books with their statuses for debugging
    print("All books and their statuses:")
    for book in Book.objects.all():
        print(f"Book: {book.title}, Status: {book.status}")
    
    # Filter by status if provided in URL parameters
    status_filter = request.GET.get('status', None)
    if status_filter:
        print(f"Filtering by status: {status_filter}")
        books_list = books_list.filter(status=status_filter)
    
    # Filter by category if provided in URL parameters
    category_id = request.GET.get('category', None)
    if category_id and category_id.isdigit():
        print(f"Filtering by category ID: {category_id}")
        books_list = books_list.filter(category_id=int(category_id))
    
    # Search by book name if provided in URL parameters
    search_query = request.GET.get('search', None)
    if search_query:
        print(f"Searching for: {search_query}")
        books_list = books_list.filter(title__icontains=search_query)
    
    # Prepare context with all necessary variables
    context = {
        'books': books_list,
        'category': categories,
        'current_status': status_filter,
        'current_category': category_id,
        'search_query': search_query
    }
    
    # Print filtered books for debugging
    print(f"Filtered books:")
    for book in books_list:
        print(f"Book: {book.title}, Status: {book.status}, Category: {book.category.name}")
    
    return render(request, 'pages/books.html', context)

def update(request, id):
    book = get_object_or_404(Book, id=id)  # جلب الكتاب أو إرجاع 404
    form = BookForm(instance=book)  # تعريف الفورم باسم متسق

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('index')  # إعادة التوجيه بعد التحديث باستخدام اسم URL

    return render(request, 'pages/update.html', {'form': form})
def delete(request, id):
    book = get_object_or_404(Book, id=id)  # Using get_object_or_404 for better error handling
    if request.method == 'POST':
        book.delete()
        return redirect('index')  # Using named URL pattern
    return render(request, 'pages/delete.html', {'book': book})  # Pass the book to the template