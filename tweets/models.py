import random
from django.db import models

class Tweet(models.Model):
    # Map to SQL data
    # id = models.AutoField(primary_key=True)
    content = models.TextField()
    image = models.FileField(upload_to='images/', blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }
