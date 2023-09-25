from cards.models import Level
import os
import django
from pprint import pprint


# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn_easy.settings")

# Initialize Django
django.setup()


def add_levels():
    levels_data = [
        {
            "name": "Discovery Novice",
            "level_number": 1,
            "total_attempts_min": 0,
            "total_correct_min": 0,
            "interval_time": 1,
            "card_background": "Basic background with a soft gradient.",
            "card_glow": "Subtle and calming glow around the card edges.",
            "description": "Welcome to the world of discovery! As a Discovery Novice, you're just beginning your journey into the realm of knowledge. You have the potential to unlock a world of insights. Keep exploring and learning to progress to the next level."
        },
        {
            "name": "Rookie Learner",
            "level_number": 2,
            "total_attempts_min": 10,
            "total_correct_min": 3,
            "interval_time": 2,
            "card_background": "A slightly textured background to add depth.",
            "card_glow": "A gentle, pulsating glow to draw attention.",
            "description": "Congratulations on reaching Rookie Learner status! By successfully attempting at least {total_attempts_min} cards with a minimum of {total_correct_min} correct answers, you've made significant progress in your learning journey. Keep up the great work, and soon you'll become a seasoned explorer of knowledge."
        },
        {
            "name": "Journeyman Explorer",
            "level_number": 3,
            "total_attempts_min": 30,
            "total_correct_min": 8,
            "interval_time": 4,
            "card_background": "A themed background related to the subject of the card.",
            "card_glow": "A dynamic, changing glow with a mild animation.",
            "description": "You've achieved the rank of Journeyman Explorer by attempting at least {total_attempts_min} cards with a minimum of {total_correct_min} correct answers. Your dedication to learning is admirable. Keep it up, and you'll uncover deeper insights as you explore cards with themed backgrounds and dynamic glows."
        },
        {
            "name": "Master Artisan",
            "level_number": 4,
            "total_attempts_min": 70,
            "total_correct_min": 21,
            "interval_time": 7,
            "card_background": "A dynamic background with subtle, animated elements.",
            "card_glow": "A vibrant, pulsating glow that reacts to user interactions.",
            "description": "Welcome to the elite ranks of Master Artisan! To reach this level, you've attempted at least {total_attempts_min} cards with a minimum of {total_correct_min} correct answers. Your understanding and expertise are evident. As you craft your knowledge and skills with dynamic backgrounds and vibrant glows, you'll shape your path towards becoming a true master. Keep honing your abilities."
        },
        {
            "name": "Sage Scholar",
            "level_number": 5,
            "total_attempts_min": 150,
            "total_correct_min": 51,
            "interval_time": 14,
            "card_background": "A rich, textured background with interactive elements.",
            "card_glow": "A mesmerizing, interactive glow that responds to user actions.",
            "description": "You've reached the pinnacle as a Sage Scholar! To attain this esteemed status, you've successfully attempted at least {total_attempts_min} cards with a minimum of {total_correct_min} correct answers. Your wisdom and mastery are inspiring. Embrace your role as a guiding light for others on their learning journeys. Your dedication to knowledge, coupled with rich, textured backgrounds and mesmerizing glows, is truly remarkable."
        },
    ]

    for level_data in levels_data:
        Level.objects.create(
            name=f"{level_data['name']} (Level {level_data['level_number']})",
            level_number=level_data["level_number"],
            total_attempts_min=level_data["total_attempts_min"],
            total_correct_min=level_data["total_correct_min"],
            interval_time=level_data["interval_time"],
            card_background=level_data["card_background"],
            card_glow=level_data["card_glow"],
            description=level_data["description"].format(
                total_attempts_min=level_data["total_attempts_min"],
                total_correct_min=level_data["total_correct_min"]
            )
        )


def run():
    add_levels()