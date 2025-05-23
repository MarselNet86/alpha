from django.shortcuts import render, redirect
from .forms import LoginForm, ChangePasswordForm, UserEditForm, UserCreateForm
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404

from datetime import timedelta, datetime

from .models import User, Role


def home(request):
    return redirect('login')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'] 
            password = form.cleaned_data['password'] 

            try:
                user = User.objects.get(name=name)

                if user.last_login_date and timezone.now() - user.last_login_date > timedelta(days=30):
                    user.is_blocked = True
                    user.save()
                    messages.error(request, 'Ваша учётная запись заблокирована из-за неактивности более 1 месяца.')

                if user.password == password:
                    user.failed_attempts = 0
                    user.last_login_date = timezone.now()
                    user.save()

                    request.session['user_id'] = user.id
                    messages.success(request, 'Вы успешно авторизовались.')


                    if user.is_password_changed == False:
                        return redirect('change_password')
                
                    else:
                        if user.role.name == 'Пользователь':
                            return redirect('user_panel')
                        
                        if user.role.name == 'Администратор':
                            return redirect('admin_panel')
                
                else:
                    user.failed_attempts += 1
                    if user.failed_attempts >= 3:
                        user.is_blocked = True
                        messages.error(request, 'Вы заблокированы. Обратитесь к администратору.')

                    else:
                        messages.error(request,
                            f'Вы ввели неверный логин или пароль. Осталось попыток: {3 - user.failed_attempts}'
                            )
                    user.save()
                    return render(request, 'main/login.html', {'form': form})

                
            
            except User.DoesNotExist:
                messages.error(request,
                    'Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные.'
                )

    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})


def change_password(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Вы не авторизованы.')
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден.')
        return redirect('login')
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            secondary_password = form.cleaned_data['secondary_password']

            if user.password != old_password:
                messages.error(request, 'Старый пароль введён неверно.')
            elif new_password != secondary_password:
                messages.error(request, 'Новые пароли не совпадают.')
            else:
                user.password = new_password
                user.is_password_changed = True
                user.save()
                messages.success(request, 'Пароль успешно изменён.')

                return redirect('login')
    else:
        form = ChangePasswordForm()

    return render(request, 'main/change_password.html', {'form': form})


def user_panel(request):
    return render(request, 'main/user_panel.html')


def admin_panel(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            if User.objects.filter(name=form.cleaned_data['name']).exists():
                messages.error(request, 'Пользователь с таким логином уже существует.')
            else:
                form.save()
                messages.success(request, 'Пользователь добавлен.')
            return redirect('admin_panel')
    else:
        form = UserCreateForm(initial={'last_login_date': timezone.now()})

    users = User.objects.all()
    return render(request, 'main/admin_panel.html', {'form': form, 'users': users})


def unblock_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_blocked = False
        user.failed_attempts = 0
        user.save()
        messages.success(request, f'Пользователь {user.name} разблокирован.')
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден.')

    return redirect('admin_panel')


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь обновлён.')
            return redirect('admin_panel')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'main/edit_user.html', {'form': form})



def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, f'Пользователь {user.name} удалён.')
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден.')

    return redirect('admin_panel')
