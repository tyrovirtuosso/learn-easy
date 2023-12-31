from django.db import models
from usersApp.models import CustomUser
from django.utils import timezone


# Tags Table
class Tag(models.Model):
    tag_name = models.CharField(max_length=255, unique=True, verbose_name="Tag Name")
    group_name = models.CharField(max_length=255, verbose_name="Tag Group", blank=True, null=True, unique=True)

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
    decks = models.ManyToManyField('decks.Deck', related_name='cards_deck')
    smart_decks = models.ManyToManyField('decks.SmartDeck', related_name='cards_smartdeck')
    system_defined_tags = models.ManyToManyField(Tag, related_name="system_defined_cards", verbose_name="System Defined Tags")
    user_defined_tags = models.ManyToManyField(Tag, related_name="user_defined_cards", verbose_name="User Defined Tags")
    card_content_system_generated = models.TextField(verbose_name="System Generated Content")
    card_content_user_generated = models.TextField(verbose_name="User Generated Content")
    notes = models.TextField(verbose_name="User Notes")
    associated_resources = models.TextField(verbose_name="Associated Resources")
    pronunciation = models.FileField(upload_to='pronunciations/', null=True, blank=True, verbose_name="Pronunciation")

    class Meta:
        unique_together = ('user', 'card_name')
        
    def current_level(self):
        # Get the most recent review of this card
        latest_review = self.review_set.order_by('-last_review').first()

        # If there is a review, return its level, otherwise return None
        return latest_review.level if latest_review else None
    
    def save(self, *args, **kwargs):
        self.card_name = self.card_name.lower()
        super(Card, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.card_name


# Review Table
# Smart deck should be an option the user needs to click to perform or get updated(not automatic). There is a different section for smart and user defined
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
    outcome = models.BooleanField(default=False, choices=OUTCOME_CHOICES, verbose_name="Outcome (Correct or Incorrect Answer)")
    status = models.BooleanField(default=False, verbose_name="Review Status (Completed or Not Completed)")
    completion_time = models.FloatField(null=True, verbose_name="Completion Time (minutes)")
    last_review = models.DateTimeField(null=True, default=None, verbose_name="Date and Time of Last Review")
    next_review = models.DateTimeField(null=True, default=None, verbose_name="Date and Time of Next Review")
    priority_level = models.BooleanField(default=False, verbose_name="Priority Level (1 for Priority, 0 for No Priority)")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, verbose_name="Associated Learning Level")
    ease_factor = models.FloatField(default=2.5, verbose_name="Ease Factor (Used for Recall Calculation)")
    interval = models.IntegerField(default=1, verbose_name="Review Interval (in Days)")
    repetitions = models.IntegerField(default=0, verbose_name="Number of Successful Recall Attempts")
    question = models.TextField(blank=True, null=True, verbose_name="Review Question")
    answer = models.TextField(blank=True, null=True, verbose_name="Review Answer")
    
    # Review should be there only if question for review card is present    
    def update_review(self, card, outcome, ease_of_recall, priority_level, completion_time):
        print("updating review")
        self.last_review = timezone.now()
        self.outcome = outcome
        self.ease_of_recall = ease_of_recall
        self.priority_level = priority_level
        self.completion_time = completion_time
        self.status = True
        
        if outcome:  # If the card was answered correctly
            self.repetitions += 1
            
            if ease_of_recall:
                self.ease_factor += 0.2
            else:
                self.ease_factor -= 0.1
                self.ease_factor = max(self.ease_factor, 1.3)                        
                
        else:  # If the card was answered incorrectly
            self.repetitions -= 2
            self.repetitions = max(self.repetitions, 1)
        
        # Finding out proper Level and Intercal for card
        if self.repetitions == 1:
            self.interval = 1
            self.level = Level.objects.get(level_number=2)
        elif self.repetitions == 2:
            self.interval = 2
            self.level = Level.objects.get(level_number=3)
        else:
            self.interval *= self.ease_factor
            if self.priority_level:
                self.interval *= 0.9
            
            if self.repetitions >= 5 and self.ease_factor > 2.5:
                self.level = Level.objects.get(level_number=4)
            elif self.repetitions >= 10 and self.ease_factor > 3:
                self.level = Level.objects.get(level_number=5)

        new_review = Review(card=card)
        new_review.next_review = self.last_review + timezone.timedelta(days=self.interval)
        total_reviews = Review.objects.filter(card=card).count()
        self.save()
        new_review.save()

    def __str__(self):
        return f"Review of {self.card}"

class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message