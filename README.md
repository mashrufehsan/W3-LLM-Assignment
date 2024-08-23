
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
- 👉 [Models](#Models "Go to: Models")
- 👉 [Admin Interface](#Admin-Interface "Go to: Admin Interface")
- 👉 [Notes](#Notes "Go to: Using the CLI application")


## Installation ##

### Prerequisites ###
1. Python
2. Django
3. PostgreSQL
4. Git
5. Ollama model setup (PLease refer to [Ollama documentation](https://github.com/ollama/ollama/tree/main))


### Steps ###

1. **[Download](https://ollama.com/download) and install Ollama.**

2. **Choose a [model](https://ollama.com/library).**

3. **Download the model:**
    ```bash
    ollama pull <model_name>
    ```

4. **Clone and navigate to the the Repository.**
    ```bash
    git clone https://github.com/mashrufehsan/W3-LLM-Assignment.git
    cd W3-LLM-Assignment
    ```
5. **Create and Activate Virtual Environment.**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```
6. **Install Dependencies.**
    ```bash
    pip install -r requirements.txt
    ```
7. **Configure environment variables.**

    Copy the .env.sample file to .env and fill in the required configuration.
    - On macOS/Linux:
        ```bash
        cp .env.sample .env
        ```
    - On windows:
        ```bash
        copy .env.sample .env
        ```
    Run the following command to view all the available Ollama models available on your machine.
    ```bash
    ollama list
    ```
    Update the `.env` file with your PostgreSQL database credentials and specify the Ollama model of your choice.

8. **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
9. **Start the CLI application**
    ```bash
    python manage.py generate_summary
    ```

### ! Important ###
Upon running the application, you will be prompted to enter the superuser admin `username` and `password`.

You can use the previous Django project's superadmin `username` and `password`.

Otherwise, create a new superadmin before starting the CLI application:
```bash
python manage.py createsuperuser
```

Once authenticated, the application will rewrite property titles and descriptions, generate summaries from the available data, and store the summaries in a separate table.

## Models ##
This CLI application generates a `property_summary` table, delivering an insightful summary of property data.

### PropertySummary ###
Represents a summary of a property with a relationship to the `PropertyInfo` model.

- **property_info**: `ForeignKey` - A relationship to the `PropertyInfo` model, representing the property to which this summary is linked.
- **summary**: `TextField` - A Detailed text field containing the summary of the property.

**Meta Options:**
- `db_table`: 'property_summary'
- `verbose_name_plural`: 'Property Summaries'


## Admin Interface ##
This project also offers an admin panel to view data of the newly generated `property_summary` table.

To access the admin panel, start the server on a different port:
```bash
python manage.py runserver 8001
```
Once the server is running, the admin panel for `property_summary` can be accessed at:
> http://localhost:8001/admin


## Notes ##
- Ensure PostgreSQL and Ollama are running and accessible with the credentials provided in the .env file.
