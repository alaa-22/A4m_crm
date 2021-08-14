from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from allauth.account.utils import perform_login


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return
        try:
            # t=user.socialaccount_set.filter(provider='google').values_list()
            # print(sociallogin.cleaneddata.get('name'))
            user = User.objects.get(id=user.id)  # if user exists, connect the account to the existing account and login
            sociallogin.state['process'] = 'connect'
            perform_login(request, user, 'none')
        except user.DoesNotExist:
            pass

    def get_login_redirect_url(self, request):
        path = '/dashboard'
        return path
