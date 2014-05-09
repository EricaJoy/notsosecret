from django.db import models


# Create your models here.

class Secret(models.Model):
    secrets_id = models.AutoField(primary_key=True)
    secret_url = models.URLField(max_length=512)
    secret_text = models.TextField()
    postive_count =  models.IntegerField(default=1)
    share_count = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.secret_text


def get_secrets(x=10):
    secrets = Secret.objects.all()[:x]
    return secrets

def secret_exists(secret_url):
    try:
        secret = Secret.objects.get(secret_url=secret_url)
        secret.share_count += 1
        secret.save()
        print secret_url, "exists"
        return True
    except:
        return False

def put_secret(secret_url, secret_text):
    s = Secret(secret_url=secret_url, secret_text=secret_text)
    s.save()

# Maybe not needed
def increment_share_count(secret_url):
    secret = Secret.objects.get(secret_url=secret_url)
    secret.share_count += 1
    secret.save()

def increment_positive_count(secrets_id):
    secret = Secret.objects.get(secrets_id=secrets_id)
    secret.postive_count += 1
    secret.save()
