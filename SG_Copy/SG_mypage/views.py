from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

@login_required
def dashboard(request):
    user = request.user
    if user.user_type == 'client':  # 의뢰인
        return render(request, 'mypage/client_dashboard.html', {'user': user})
    elif user.user_type == 'pro':  # 고수
        return render(request, 'mypage/pro_dashboard.html', {'user': user})
    else:
        return redirect('account:login')  # 혹시 모를 예외 처리

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('mypage:profile')
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'mypage/profile.html', {'form': form})