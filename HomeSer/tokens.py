from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Include user-specific data and timestamp in the hash
        # Include is_active so token invalidates after activation
        return (
            str(user.pk) + str(timestamp) +
            str(user.is_active) + str(user.email)
        )


account_activation_token = AccountActivationTokenGenerator()


def generate_activation_link(user):
    """Generate an activation link for a user"""
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return reverse('activate', kwargs={'uidb64': uid, 'token': token})