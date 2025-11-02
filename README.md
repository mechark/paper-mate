
# Paper-Mate - your personal assistant for exploring arXiv papers

### Run Paper Mate

1. clone the repository with ``git clone https://github.com/mechark/paper-mate.git``
2. Run ``cd paper-mate``
3. Paste ``vector_store`` directory inside ``/paper-mate``
4. Make sure your Docker Engine is running and type ``docker compose up --build`` into your terminal. You can set the language model you want to use via ``MODEL_NAME`` env variable. By default the project uses ``llama3.2:3b model``.
5. After everything is up and running, you can go to http://localhost:8000 and checkout the setup!
