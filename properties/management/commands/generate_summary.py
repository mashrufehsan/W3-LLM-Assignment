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

    def handle(self, *args, **options):
        try:
            response = ollama.chat(model='phi3', messages=[
                {
                    'role': 'user',
                    'content': 'give me description of hotel named radisson blue in 10 words',
                },
            ])
            print(response['message']['content'])

        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR(
                "\nProcess interrupted. Exiting..."))
