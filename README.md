# dsf-interlup-api

Welcome to the dsf-interlup-api repository! This repository contains the source code for the DSF Interlup API project.

## Description

DSF Interlup API is a RESTful API built using Flask, designed to provide backend functionality for managing tasks and task categories. It includes features for user authentication, task creation, updating, deletion, and more.

## Local Installation

To run this project locally, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/danielxavierjob/dsf-interlup-api.git
   ```

2. Install the project dependencies:

   ```bash
   cd dsf-interlup-api
   pip install -r requirements.txt
   ```

3. Set up the environment:

   - Create a `.env` file in the root directory.
   - Define the required environment variables in the `.env` file. Example:
     ```
     SECRET_KEY=your_secret_key
     DATABASE_URL=sqlite:///db.db
     DEBUG=True
     ```

4. Initialize the database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the Flask application:

   ```bash
   flask run
   ```

6. Access the API endpoints at `http://localhost:5000`.

## Docker Installation

To run this project with Docker, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/danielxavierjob/dsf-interlup-api.git
   ```

2. Navigate to the project folder:

   ```bash
   cd dsf-interlup-api
   ```

3. Set up the environment:

   - Create a `.env` file in the root directory.
   - Define the required environment variables in the `.env` file. Example:
     ```
     SECRET_KEY=your_secret_key
     DATABASE_URL=postgresql://postgres:1234@your_ip:5432/postgres
     DEBUG=True
     ```

4. Run the application with Docker:

   ```bash
   docker compose build
   docker compose up
   ```

5. Access the API endpoints at `http://localhost:5000`.

## Usage

Once the application is running, you can interact with the API using tools like `curl`, Postman, or any HTTP client library. Here are some example API endpoints:

- `GET /tasks`: Retrieve all tasks.
- `POST /tasks`: Create a new task.
- `PUT /tasks/<task_id>`: Update an existing task.
- `DELETE /tasks/<task_id>`: Delete a task.

For detailed API documentation and usage examples, refer to the docstrings and comments in the source code, or access the Swagger documentation at the /api route.

## Contributing

Contributions are welcome! If you have ideas for improvements, bug fixes, or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).