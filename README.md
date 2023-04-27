# Setup

1. Set up environmental variables for development:

```bash
echo 'SECRET_KEY="<a_secret>"' >> .env
echo 'DEBUG=True' >> .env
```

2. Install dependencies using pipenv:

```bash
pipenv install && pipenv shell
```

Pipenv reads in the environmental variables from `.env` that were set in step 1.
These environmental variables are needed to run the development server.
