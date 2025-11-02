
# Paper-Mate - your personal assistant for exploring arXiv papers

### Run Paper Mate

1. Clone the repository:

```bash
git clone https://github.com/mechark/paper-mate.git
```

2. Open the working directory:

```bash
cd paper-mate
```

3. Place the  ``vector_store`` directory inside the  ``/paper-mate``
4. Make sure Docker Engine is running, then build and start the containers:

```bash
docker compose up --build
```

You can set the language model you want to use via ``MODEL_NAME`` env variable (see other available variables in ``.env.example``). By default the project uses  ``llama3.2:3b`` model.

🎉 Once <b>everything is up and running</b>, open http://localhost:8000 to checkout the setup!
