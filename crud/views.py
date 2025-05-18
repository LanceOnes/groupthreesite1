from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password, check_password
from .utils import login_required_custom
from django.contrib.auth import logout
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Get username instead of email
        password = request.POST.get('password')

        try:
            user = Users.objects.get(username=username)  # Query by username
            if check_password(password, user.password):  # Validate password
                request.session['user_id'] = user.user_id  # Set user_id in session
                messages.success(request, 'Login successful!')
                return redirect('/user/list')  # Redirect to user list
            else:
                messages.error(request, 'Invalid password')  # Incorrect password
        except Users.DoesNotExist:
            messages.error(request, 'User does not exist')  # Username not found
        except Exception as e:
            messages.error(request, f'Error occurred during login: {e}')  # Handle unexpected errors

    return render(request, 'layout/login.html')

@login_required_custom
def gender_list(request):
    try:    
        genders = Genders.objects.all() #Select * FROM tbl_genders
        
        data = {
            'genders':genders
        }
        
        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')

@login_required_custom
def add_gender(request): 
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')
            
            Genders.objects.create(gender=gender).save() #INSERT INTO tbl_genders(gender) VALUES(gender)
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f"Error occurred during add gender: {e}")  
    
@login_required_custom   
def edit_gender(request, genderId):
  try:
    if request.method == 'POST':
     genderObj = Genders.objects.get(pk=genderId) 
     
     gender = request.POST.get('gender')
     
     genderObj.gender = gender
     genderObj.save()
     
     messages.success(request, 'gender updated successfully!')
     
     data = {
       'gender': genderObj
     }
     
     return render(request, 'gender/EditGender.html', data)
    else:      
     genderObj = Genders.objects.get(pk=genderId)     
    
     data = {
       'gender': genderObj
     }
    
     return render (request, 'gender/EditGender.html', data)
  except Exception as e:
    return HttpResponse(f'Error occured during edit gender: {e}')

@login_required_custom
def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
         genderObj = Genders.objects.get(pk=genderId)     
         genderObj.delete()
         
         messages.success(request, 'Gender deleted successfully!')
         return redirect('/gender/list')
        else:
         genderObj = Genders.objects.get(pk=genderId)     
    
         data = {
            'gender': genderObj
        }
    
        return render (request, 'gender/DeleteGender.html', data)
 
    except Exception as e:
        return HttpResponse(f'Error occured during edit gender: {e}')

@login_required_custom
def user_list(request):
    search_query = request.GET.get('search', '')

    user_queryset = Users.objects.select_related('gender').filter(
        Q(full_name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(username__icontains=search_query) |
        Q(gender__gender__icontains=search_query) |  
        Q(birth_date__icontains=search_query) |      
        Q(address__icontains=search_query) |         
        Q(contact_number__icontains=search_query)    
    ).order_by('user_id')

    # Handle AJAX requests for live search
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        users_data = [
            {
                'user_id': user.user_id,
                'full_name': user.full_name,
                'email': user.email,
                'username': user.username,
                'gender': user.gender.gender,
                'birth_date': user.birth_date.strftime('%Y-%m-%d') if user.birth_date else '',
                'address': user.address,
                'contact_number': user.contact_number,
            }
            for user in user_queryset
        ]
        return JsonResponse({'users': users_data})

    paginator = Paginator(user_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }

    return render(request, 'user/UsersList.html', context)

@login_required_custom
def add_user(request):
    try:
        if request.method == 'POST':
            # Get form data
            fullName = request.POST.get('full_Name')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')

            # Check if all required fields are filled
            if not all([fullName, gender, birth_date, address, contactNumber, username, password, confirmPassword]):
                messages.error(request, 'All required fields must be filled!')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': request.POST
                })

            # Check if passwords match
            if password != confirmPassword:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': request.POST,
                    'password_error': True
                })

            # Check if username already exists
            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists! Please choose a different username.')
                return render(request, 'user/AddUser.html', {
                    'genders': Genders.objects.all(),
                    'form_data': request.POST,
                    'username_error': True
                })

            # Create the user
            Users.objects.create(
                full_name=fullName,
                gender=Genders.objects.get(pk=gender),
                birth_date=birth_date,
                address=address,
                contact_number=contactNumber,
                email=email,
                username=username,
                password=make_password(password)
            ).save()

            messages.success(request, 'User added successfully!')
            return redirect('/user/list/')
        else:
            # Render the form with gender options
            genderObj = Genders.objects.all()

        data = {
            'genders': genderObj
        }
        return render(request, 'user/AddUser.html', data)
    except Exception as e:
        messages.error(request, f'Error occurred during add user: {e}')
        return redirect('/user/add')


@login_required_custom
def edit_user(request, userId):
    try:
        userObj = Users.objects.get(pk=userId)

        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Check if all fields are filled
            if not all([full_name, gender, birth_date, address, contact_number, username]):
                messages.error(request, 'All fields are required!')
                return redirect(f'/user/edit/{userId}')

            # Check if passwords match
            if password and confirm_password:
                if password != confirm_password:
                    messages.error(request, 'Passwords do not match!')
                    return render(request, 'user/EditUser.html', {
                        'user': userObj,
                        'genders': Genders.objects.all(),
                        'password_error': True
                    })
                userObj.password = make_password(password)

            # Check if username is updated and already exists
            if username != userObj.username and Users.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists! Please choose a different username.')
                return render(request, 'user/EditUser.html', {
                    'user': userObj,
                    'genders': Genders.objects.all(),
                    'username_error': True
                })

            # Update the user
            userObj.full_name = full_name
            userObj.gender = Genders.objects.get(pk=gender)
            userObj.birth_date = birth_date
            userObj.address = address
            userObj.contact_number = contact_number
            userObj.email = email
            userObj.username = username
            userObj.save()

            messages.success(request, 'User updated successfully!')
            return redirect('/user/list/')

        data = {
            'user': userObj,
            'genders': Genders.objects.all()
        }

        return render(request, 'user/EditUser.html', data)

    except Exception as e:
        messages.error(request, f'Error occurred during edit: {e}')
        return redirect('/user/list/')

@login_required_custom  
def delete_user(request, userId):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)
            userObj.delete()

            messages.success(request, 'User deleted successfully!')
            return redirect('/user/list/')
        else:
            userObj = Users.objects.get(pk=userId)

            data = {
                'user': userObj
            }

            return render(request, 'user/DeleteUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during delete user: {e}')

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

@login_required_custom
def change_password(request, userId):
    userObj = get_object_or_404(Users, pk=userId)

    if request.method == 'POST':
        form = change_password(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            userObj.password = make_password(new_password)
            userObj.save()

            messages.success(request, 'Password changed successfully!')
            return redirect('/user/list') 
    else:
        form =  change_password()

    context = {
        'user': userObj,
        'form': form,
    }
    return render(request, 'user/changepassword.html', context)

def signup_view(request):
   try:

    if request.method == 'POST':   
        fullName = request.POST.get('full_Name')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        contactNumber = request.POST.get('contact_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirm_password')

        
        Users.objects.create(
            full_name=fullName,
            gender=Genders.objects.get(pk=gender),
            birth_date=birth_date,
            address=address,  
            contact_number=contactNumber,
            email=email,
            username=username,
            password=make_password(password)

        ).save()

        messages.success(request, 'User added successfully!')
        return redirect('login')
    
    else:
      genderObj = Genders.objects.all()

    data = {
       'genders': genderObj
    }
    return render(request, 'layout/Signup.html', data)
   except Exception as e:
    return HttpResponse(f'Error occured during add user: {e}')

@login_required_custom
def password(request, userId=None):
    if not userId:
        messages.error(request, 'User ID is required to change the password.')
        return redirect('/user/list/')

    user = get_object_or_404(Users, pk=userId)

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return redirect(f'/user/password/{userId}/')

            user.password = make_password(password)
            user.save()
            messages.success(request, 'Password updated successfully!')
            return redirect('/user/list/')
        else:
            messages.error(request, 'Password fields cannot be empty!')

    return render(request, 'user/password.html', {'user': user})





