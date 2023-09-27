from django.db import models

class Deck(models.Model):
    user = models.ForeignKey('usersApp.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, verbose_name="Deck Name")
    is_public = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        # Ensure that deck names are case-insensitive unique
        self.name = self.name.lower()
        super(Deck, self).save(*args, **kwargs)