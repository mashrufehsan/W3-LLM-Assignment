from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from django.conf import settings
from getpass import getpass
import psycopg2
from properties.models import PropertyInfo, PropertySummary
from dotenv import load_dotenv
import os
import ollama

load_dotenv()


class Command(BaseCommand):
    help = "Interact with the Ollama model gemma2:2b"

    def ask_llm(self, prompt):
        response = ollama.chat(model=os.getenv('MODEL'), messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        output = response['message']['content']
        return output

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            'Using the database configuration from \'.env\' file.'))
        try:
            username = input("Enter superadmin username: ")
            password = getpass("Enter superadmin password: ")
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                self.stdout.write(self.style.SUCCESS(
                    '\nAdmin login success!\n'))
                db_config = settings.DATABASES['default']

                # Fetch all PropertyInfo objects
                property_infos = PropertyInfo.objects.all()

                for property_info in property_infos:
                    title = property_info.title
                    locations = property_info.locations.all()
                    if locations.exists():
                        location_names = ', '.join([
                            f"{location.name} ({location.get_type_display()}), "
                            f"Latitude: {location.latitude}, Longitude: {location.longitude}"
                            for location in locations
                        ])
                    else:
                        location_names = ""

                    amenities = property_info.amenities.all()
                    if amenities.exists():
                        amenity_names = ', '.join(
                            [amenity.name for amenity in amenities])
                    else:
                        amenity_names = ""

                    result_str = (f"\nHotel name: {title}")
                    if location_names != "":
                        result_str += f" Location: {location_names}"
                    if amenity_names != "":
                        result_str += f" Amenities: {amenity_names}"

                    self.stdout.write(self.style.WARNING(
                        f"Generating Title, Description and Summary for {property_info.title.rstrip()}.\nPlease wait..."))

                    self.stdout.write(self.style.WARNING(
                        'Generating description... '))

                    generated_description = self.ask_llm(
                        'give description in 2 sentences for ' + result_str)

                    self.stdout.write(self.style.SUCCESS('Generated!'))

                    self.stdout.write(
                        self.style.WARNING('Generating title... '))

                    generated_title = self.ask_llm(
                        f'''rewrite the title for {property_info.title}.
                        give just 1 title witout any special characters''')

                    self.stdout.write(self.style.SUCCESS('Generated!'))

                    self.stdout.write(
                        self.style.WARNING('Generating summary... '))

                    generated_summary = self.ask_llm(
                        f'''Generate a 4-line summary for the hotel described below.
                        - Include the hotel name.
                        - Mention the location if available (name, latitude, and longitude).
                        - Include any amenities if mentioned.
                        - Avoid special characters or line breaks.
                        Details: {result_str}''')

                    self.stdout.write(self.style.SUCCESS('Generated!'))

                    self.stdout.write(self.style.WARNING(
                        'Saving to database...'))

                    property_info.title = generated_title
                    property_info.description = generated_description
                    property_info.save()

                    summary, created = PropertySummary.objects.get_or_create(
                        property_info=property_info
                    )

                    if created:
                        # New summary created
                        summary.summary = generated_summary
                        summary.save(update_fields=['summary'])
                    else:
                        # Existing summary found, update it
                        summary.summary = generated_summary
                        summary.save()

                    self.stdout.write(self.style.SUCCESS('Saved!\n'))

            else:
                self.stdout.write(self.style.ERROR(
                    'Invalid credentials or user is not a superadmin'))

        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR(
                "\nProcess interrupted. Exiting..."))
