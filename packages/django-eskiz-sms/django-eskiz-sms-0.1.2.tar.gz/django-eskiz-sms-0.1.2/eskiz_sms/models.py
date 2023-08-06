from django.db import models
from django.utils import timezone
import requests



class EskizSMS(models.Model):
    
    email = models.EmailField('Eskiz Email')
    password = models.CharField('Eskiz Pass from Cabinet', max_length=255)
    from_name = models.CharField('Nickname (Default 4546)', max_length=255, blank=True, null=True)
    callback_url = models.URLField("Callback URL (Optional)", null=True, blank=True)

    eskiz_token = models.TextField("Token (Auto generated)", null=True, blank=True)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
    

    def update_token(self):
        
        payload = {
            'email': self.email,
            'password': self.password
        }
        
        response = requests.post("https://notify.eskiz.uz/api/auth/login", headers={}, data=payload)
        
        if response.status_code == 200:
            resp_data = response.json()
            
            self.last_updated = timezone.now()
            self.eskiz_token = resp_data.get('data', {}).get('token', '')
            self.save()
            
            return resp_data.get('data', {}).get('token', '')
        return None





class SMSLog(models.Model):
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    from_name = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    status_date = models.DateTimeField(default=timezone.now)
    error_message = models.TextField(blank=True, null=True)
    from_app = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.phone_number} - {self.message}"

def save_sms_log(phone_number, message, from_name, status, error_message=None, from_app=None):
    SMSLog.objects.create(
        phone_number=phone_number,
        message=message,
        from_name=from_name,
        status=status,
        error_message=error_message,
        from_app=from_app
    )
