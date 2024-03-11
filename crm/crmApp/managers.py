from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phoneNumber, role, team, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phoneNumber=phoneNumber,
            role=role,
            team=team
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phoneNumber, role, team, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            phoneNumber=phoneNumber,
            role=role,
            team=team,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
