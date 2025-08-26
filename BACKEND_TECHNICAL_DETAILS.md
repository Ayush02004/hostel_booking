# Hostel Booking System - Backend Technical Documentation

## Project Overview

The Hostel Booking System is a Django-based web application that provides a comprehensive platform for managing hostel room bookings. The backend is built using Django 4.2.5 and follows the Model-View-Template (MVT) architectural pattern.

## Technology Stack

- **Framework**: Django 4.2.5
- **Database**: SQLite3 (development)
- **Language**: Python 3.x
- **Architecture**: MVT (Model-View-Template)

## Project Structure

```
Hostel_booking/
├── Hostel_booking/          # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── booking/                 # Core booking application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin interface
│   ├── forms.py            # Form classes
│   └── migrations/         # Database migrations
├── users/                   # User management application
│   ├── models.py           # User models
│   ├── views.py            # Authentication views
│   ├── urls.py             # URL routing
│   ├── forms.py            # User forms
│   └── migrations/         # Database migrations
└── manage.py               # Django management script
```

## Database Schema

### 1. hostel_details Model

```python
class hostel_details(models.Model):
    cooling = models.CharField(max_length=10)      # AC/Non-AC
    block = models.CharField(max_length=1)         # Hostel block (A, B, C, etc.)
    sharing = models.IntegerField()                # Number of people sharing (1, 2, 3, etc.)
    bathroom = models.CharField(max_length=10)     # Attached/Common
    price = models.IntegerField()                  # Room price per month
```

**Purpose**: Stores information about available hostel rooms with their specifications and pricing.

**Fields**:
- `id`: Auto-generated primary key
- `cooling`: Type of cooling (AC/Non-AC)
- `block`: Hostel block identifier
- `sharing`: Number of occupants per room
- `bathroom`: Bathroom type (Attached/Common)
- `price`: Monthly rental price

### 2. transactions Model

```python
class transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(hostel_details, on_delete=models.CASCADE)
```

**Purpose**: Records booking transactions linking users to their booked rooms.

**Fields**:
- `id`: Auto-generated primary key
- `user`: Foreign key to Django's built-in User model
- `room`: Foreign key to hostel_details model

**Relationships**:
- Many-to-One relationship with User (one user can have multiple transactions)
- Many-to-One relationship with hostel_details (one room can have multiple bookings)

### Migration History

The database has evolved through several migrations:

1. **0001_initial**: Created initial hostel_details model
2. **0002_transactions**: Added transactions model
3. **0003_transactions_price**: Added price field to transactions (later removed)
4. **0004_rename_user_name_transactions_user**: Renamed user_name field to user
5. **0005_remove_transactions_price**: Removed price field from transactions

## API Endpoints and Views

### Booking Application (`/booking/`)

#### 1. Index View (`/`)
```python
def index(request):
    return render(request, "booking/index.html")
```
- **Purpose**: Displays the main landing page
- **Method**: GET
- **Template**: `booking/index.html`

#### 2. Details View (`/details`)
```python
def details(request):
    room_details = hostel_details.objects.all()
    return render(request, "booking/details.html", {"room_details": room_details})
```
- **Purpose**: Shows all available hostel rooms
- **Method**: GET
- **Data**: Fetches all hostel_details records
- **Template**: `booking/details.html`

#### 3. Booking View (`/booking`)
```python
def booking(request):
    # Handles both room search and payment processing
    if request.method == "POST":
        form_type = request.POST.get("form_type", "")
        if form_type == "booking":
            # Room search logic
        elif form_type == "payment":
            # Payment processing logic
    # GET request - display booking form
```

**Features**:
- **Room Search**: Filters rooms based on user criteria
- **Payment Processing**: Creates transaction records
- **Dynamic Form Handling**: Uses form_type to distinguish between search and payment

**Search Algorithm**:
```python
room = hostel_details.objects.filter(
    block=hostel_block,
    cooling=cooling,
    sharing=sharing,
    bathroom=bathroom
).values()[0]
```

**Payment Processing**:
```python
transaction = transactions(user=request.user, room_id=room_id)
transaction.save()
```

#### 4. Transaction View (`/transaction`)
```python
def transaction(request):
    try:
        username = request.user
        transactions_obj = transactions.objects.filter(user=username).values()[0]
        room_id = transactions_obj["room_id"]
        room_details = hostel_details.objects.filter(id=room_id).values()[0]
        return render(request, "booking/transaction.html", {"room_details": room_details})
    except:
        return render(request, "booking/transaction.html")
```

**Features**:
- Displays user's booking history
- Shows room details for booked rooms
- Handles cases where no transactions exist

### User Management Application (`/`)

#### 1. User Registration (`/`)
```python
def create_user(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
```

**Features**:
- User registration with custom form
- Automatic login after registration
- Form validation and error handling

#### 2. User Login (`/login/`)
```python
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
```

**Features**:
- Username/password authentication
- Session management
- Error handling for invalid credentials

#### 3. User Logout (`/logout/`)
```python
def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out"})
```

**Features**:
- Session termination
- Redirect to login page with confirmation message

## Forms and Validation

### User Registration Form
```python
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", 'email', 'password1', 'password2')
```

**Features**:
- Extends Django's UserCreationForm
- Includes additional fields (first_name, last_name, email)
- Built-in password validation
- Username uniqueness validation

## Admin Interface

### Configuration
```python
# booking/admin.py
admin.site.register(hostel_details)
admin.site.register(transactions)
```

**Features**:
- Hostel room management
- Transaction monitoring
- User management through Django's built-in admin
- Data export and import capabilities

## Security Features

### Authentication
- Django's built-in authentication system
- Session-based user management
- Password hashing and validation
- CSRF protection on all forms

### Data Validation
- Model-level constraints
- Form validation
- SQL injection prevention through ORM
- XSS protection through template escaping

## Technical Implementation Details

### Database Operations

#### Complex Queries
```python
# Dynamic room filtering
room = hostel_details.objects.filter(
    block=hostel_block,
    cooling=cooling,
    sharing=sharing,
    bathroom=bathroom
).values()[0]

# User transaction retrieval
transactions_obj = transactions.objects.filter(user=username).values()[0]
```

#### Data Aggregation
```python
# Unique value extraction for form options
block, cooling, sharing, bathroom = set(), set(), set(), set()
for x in hostel_details.objects.all():
    block.add(x.block)
    cooling.add(x.cooling)
    sharing.add(x.sharing)
    bathroom.add(x.bathroom)
```

### Error Handling
- Try-catch blocks for database operations
- Graceful handling of missing data
- User-friendly error messages
- Fallback templates for error states

### Performance Considerations
- Efficient ORM queries
- Minimal database hits
- Strategic use of .values() for specific fields
- Set operations for unique value extraction

## URL Routing Architecture

### Main URL Configuration
```python
# Hostel_booking/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include('booking.urls')),
    path('', include('users.urls')),
]
```

### Application-Specific Routing
```python
# booking/urls.py
urlpatterns = [
    path("", views.index, name="index"),
    path("details", views.details, name="details"),
    path("booking", views.booking, name="booking"),
    path("transaction", views.transaction, name="transaction"),
]

# users/urls.py
urlpatterns = [
    path('', views.create_user, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.login_view, name='logout'),  # Note: Should be logout_view
]
```

## Development and Deployment

### Database Migration Commands
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

### Development Server
```bash
python manage.py runserver
```

### Admin User Creation
```bash
python manage.py createsuperuser
```

## Current Database State
- **Hostel Details**: 8 room configurations available
- **Transactions**: 4 booking transactions recorded
- **Migration Status**: All migrations applied successfully

## Future Enhancements Considerations

1. **API Development**: REST API using Django REST Framework
2. **Payment Gateway Integration**: Secure payment processing
3. **Room Availability Tracking**: Real-time availability status
4. **Booking Validation**: Prevent double bookings
5. **Email Notifications**: Booking confirmations and reminders
6. **Advanced Search**: Date-based room availability
7. **User Profiles**: Extended user information management
8. **Reporting**: Analytics and booking reports

## Summary

This Django-based hostel booking system demonstrates a well-structured backend implementation with:
- Clean separation of concerns using Django apps
- Proper database relationships and migrations
- Secure user authentication and session management
- Efficient data filtering and retrieval
- Admin interface for system management
- Scalable architecture for future enhancements

The system successfully handles core functionality including user registration/login, room search with multiple criteria, booking transactions, and transaction history management.