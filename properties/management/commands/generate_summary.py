from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from django.conf import settings
from getpass import getpass
import psycopg2
from properties.models import PropertyInfo, Location
from dotenv import load_dotenv
import os
import ollama

load_dotenv()


class Command(BaseCommand):
    help = "Interact with the Ollama model phi3"

    def ask_llm(self, prompt):
        response = ollama.chat(model='gemma2:2b', messages=[
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
                self.stdout.write(self.style.SUCCESS('\nAdmin login success!'))
                db_config = settings.DATABASES['default']

                property_info = PropertyInfo.objects.first()
                if property_info:
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

                    self.stdout.write(result_str)
                else:
                    self.stdout.write("No properties found.")

                generated_description = self.ask_llm(
                    'give description in 2 sentences for ' + result_str)

                generated_title = self.ask_llm(
                    f'''rewrite the title for {property_info.title}. 
                    give just 1 title witout any special characters''')

                generated_summary = self.ask_llm(
                    f'''generate a brief summary for this hotel in plain text without any special characters.
                    If available, include amenities, location, latitude, longitude. Otherwise don't.
                    Dont't use any line break. details: + {result_str}''')

                print('Original title:', property_info.title)
                print('Generated title:', generated_title)
                print('Geerated description:', generated_description)
                print('Genarated summary:', generated_summary)

            else:
                self.stdout.write(self.style.ERROR(
                    'Invalid credentials or user is not a superadmin'))

        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR(
                "\nProcess interrupted. Exiting..."))
