from django.db import models
from usersApp.models import CustomUser

# Tags Table
class Tag(models.Model):
    tag_name = models.CharField(max_length=255, unique=True, verbose_name="Tag Name")

    def save(self, *args, **kwargs):
        # Ensure that tag_name is always stored in uppercase
        self.tag_name = self.tag_name.upper()
        super(Tag, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.tag_name

# Level Table
class Level(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of the Level")
    description = models.TextField(verbose_name="Description of the Level")
    level_number = models.IntegerField(verbose_name="Hierachial Number of the Level")
    total_attempts_min = models.IntegerField(verbose_name="Minimum Total Attempts")
    total_correct_min = models.IntegerField(verbose_name="Minimum Total Correct")
    interval_time = models.IntegerField(verbose_name="Interval Time (in days)")
    card_background = models.CharField(max_length=255, verbose_name="Card Background")
    card_glow = models.CharField(max_length=255, verbose_name="Card Glow")

    def __str__(self):
        return self.name

# Card Table
class Card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Owner of the Card")
    card_name = models.CharField(max_length=255, verbose_name="Card Name")
    decks = models.ManyToManyField('decks.Deck', related_name='cards')
    system_defined_tags = models.ManyToManyField(Tag, related_name="system_defined_cards", verbose_name="System Defined Tags")
    user_defined_tags = models.ManyToManyField(Tag, related_name="user_defined_cards", verbose_name="User Defined Tags")
    card_content_system_generated = models.TextField(verbose_name="System Generated Content")
    card_content_user_generated = models.TextField(verbose_name="User Generated Content")
    notes = models.TextField(verbose_name="User Notes (Markdown Format)")
    associated_resources = models.TextField(verbose_name="Associated Resources")
    pronunciation = models.FileField(upload_to='pronunciations/', null=True, blank=True, verbose_name="Pronunciation")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name="Level ID")

    def __str__(self):
        return self.card_name


# Review Table
class Review(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name="Card")
    EASE_CHOICES = [
        (False, 'Not Easy'),
        (True, 'Easy'),
    ]
    ease_of_recall = models.BooleanField(default=False, choices=EASE_CHOICES, verbose_name="Ease of Recall")
    OUTCOME_CHOICES = [
        (False, 'Wrong'),
        (True, 'Correct'),
    ]
    outcome = models.BooleanField(default=False, choices=OUTCOME_CHOICES, verbose_name="Outcome (Correct or Wrong)")
    total_attempts = models.IntegerField(verbose_name="Total Attempts")
    total_correct = models.IntegerField(verbose_name="Total Correct")
    accuracy = models.FloatField(verbose_name="Accuracy (Percentage)")
    completion_time = models.IntegerField(verbose_name="Completion Time (minutes)")
    last_review = models.DateField(verbose_name="Last Review")
    next_review = models.DateField(verbose_name="Next Review")
    PRIORITY_CHOICES = [
        (0, 'No Priority'),
        (1, 'Priority'),
    ]
    priority_level = models.IntegerField(default=0, choices=PRIORITY_CHOICES, verbose_name="Priority Level")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name="Level ID")

    def __str__(self):
        return f"Review of {self.card}"


class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message