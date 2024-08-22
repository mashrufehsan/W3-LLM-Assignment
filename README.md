
# Property Information rewriter and summary generator Django Application #

This project is a Django-based Command Line Interface (CLI) application that rewrites property titles and descriptions using an Ollama model and stores the updated information in a PostgreSQL database. Additionally, it generates summaries of the property information and saves them in a separate table.


## Features ##
- **Django CLI Integration**: All operations are performed through a command-line interface, leveraging Django's management commands.
- **Ollama Model Integration**: Utilizes a model from Ollama for rewriting content and generating summaries.
- **PostgreSQL Database**: Stores rewritten property titles, descriptions, and generated summaries using Django ORM.
- **Summary Generation**: Automatically generates and stores property summaries in a separate table.
- **Django Admin Interface:** Manage property summary with proper authentication.

## Index ##
- 👉 [Installation](#Installation "Go to: Installation")
- 👉 [Admin Interface](#Admin-Interface "Go to: Admin Interface")
- 👉 [Using the CLI application](#Using-the-CLI-application "Go to: Using the CLI application")
- 👉 [Models](#Models "Go to: Models")

## Installation ##

### Prerequisites ###
1. Python
2. Django
3. PostgreSQL
4. Ollama model setup ( PLease refer to [Ollama documentation](https://github.com/ollama/ollama/tree/main))
5. Git

### Steps ###

1. **Clone and navigate to the the Repository.**
    ```bash
    git clone https://github.com/mashrufehsan/W3-LLM-Assignment.git
    cd W3-LLM-Assignment
    ```
2. **Create and Activate Virtual Environment.**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```
3. **Install Dependencies.**
    ```bash
    pip install -r requirements.txt
    ```
4. **Configure environment variables.**

    Copy the .env.sample file to .env and fill in the required configuration.
    - On macOS/Linux:
        ```bash
        cp .env.sample .env
        ```
    - On windows:
        ```bash
        copy .env.sample .env
        ```
    
    Update the `.env` file with your PostgreSQL database credentials and specify the Ollama model of your choice.

5. **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. **Start the CLI application**
    ```bash
    python manage.py generate_summary
    ```
Upon running the application, you will be prompted to enter the superuser admin `username` and `password`.

Once authenticated, the application will rewrite property titles and descriptions, generate summaries from the available data, and store the summaries in a separate table.

## Admin Interface ##
Once the server is running, the Djnago admin interface can be accessed at:
> http://localhost:8000/admin


## Models
This CLI application generates a property_summary table, delivering an insightful summary of property data.

### PropertySummary
Represents a summary of a property with a relationship to the PropertyInfo model.

- **title**: `CharField` - Title of the property.
- **description**: `TextField` - Detailed description of the property (nullable).
- **locations**: `ManyToManyField` - Relationship to the `Location` model, representing a many-to-many relationship.
- **amenities**: `ManyToManyField` - Relationship to the `Amenity` model, representing a many-to-many relationship.
- **created_date**: `DateTimeField` - Timestamp of when the property was created.
- **updated_date**: `DateTimeField` - Timestamp of when the property was last updated.

**Meta Options:**
- `db_table`: 'property_info'.
- `verbose_name_plural`: 'Property Info'.

### Image
Represents an image associated with a property.

- **property_info**: `ForeignKey` - Relationship to the `PropertyInfo` model.
- **img_path**: `ImageField` - Path to the image file, with a custom filename generator.
- **created_date**: `DateTimeField` - Timestamp of when the image was uploaded.
- **updated_date**: `DateTimeField` - Timestamp of when the image was last updated.

**Meta Options:**
- `db_table`: 'image'.
- `verbose_name_plural`: 'Images'.

**Additional Functionality:**
- **delete**: Custom delete method to remove the image file from the filesystem when the image object is deleted.
- **pre_delete Signal**: Signal to remove the image file from the filesystem when the image object is deleted.

### Location
Represents a geographical location with different types (country, state, city).

- **name**: `CharField` - Name of the location.
- **type**: `CharField` - Type of the location (choices: Country, State, City).
- **latitude**: `DecimalField` - Latitude coordinate of the location (nullable).
- **longitude**: `DecimalField` - Longitude coordinate of the location (nullable).
- **created_date**: `DateTimeField` - Timestamp of when the location was created.
- **updated_date**: `DateTimeField` - Timestamp of when the location was last updated.

**Meta Options:**
- `unique_together`: Ensures a unique combination of name and type.
- `db_table`: 'location'.
- `verbose_name_plural`: 'Locations'.

### Amenity
Represents an amenity that can be associated with a property.

- **name**: `CharField` - Name of the amenity (unique).
- **created_date**: `DateTimeField` - Timestamp of when the amenity was created.
- **updated_date**: `DateTimeField` - Timestamp of when the amenity was last updated.

**Meta Options:**
- `db_table`: 'amenity'.
- `verbose_name_plural`: 'Amenities'.

## Notes

- Ensure PostgreSQL is running and accessible with the credentials provided in the .env file.
