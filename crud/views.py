from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password

# Create your views here.

def gender_list(request):
    try:    
        genders = Genders.objects.all() #Select * FROM tbl_genders
        
        data = {
            'genders':genders
        }
        
        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')

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
    
def user_list(request):
      try:
         userObj = Users.objects.select_related('gender')

         data = {
            'users': userObj
         }

         return render(request, 'user/UsersList.html', data)
      except Exception as e:
         return HttpResponse(f'Error occurred during user list retrieval: {e}')
    
def add_user(request):
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
        return redirect('/user/add')
    
    else:
      genderObj = Genders.objects.all()

    data = {
       'genders': genderObj
    }
    return render(request, 'user/AddUser.html', data)
   except Exception as e:
    return HttpResponse(f'Error occured during add user: {e}')
   


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
            
            if not all([full_name, gender, birth_date, address, contact_number, username]):
                messages.error(request, 'All fields are required!')
                return redirect(f'/user/edit/{userId}/')
            
            if password and confirm_password:
                if password != confirm_password:
                    messages.error(request, 'Passwords do not match!')
                    return redirect(f'/user/edit/{userId}/')
                userObj.password = make_password(password)
            
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
            'gender': Genders.objects.all()
        }
        
        return render(request, 'user/EditUser.html', data)
    
    except Exception as e:
        messages.error(request, f'Error occurred during edit: {e}')
        return redirect('/user/list/')
    

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
            
            if not all([full_name, gender, birth_date, address, contact_number, username]):
                messages.error(request, 'All fields are required!')
                return redirect(f'/user/edit/{userId}/')
            
            if password and confirm_password:
                if password != confirm_password:
                    messages.error(request, 'Passwords do not match!')
                    return redirect(f'/user/edit/{userId}/')
                userObj.password = make_password(password)
            
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