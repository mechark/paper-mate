
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

### Examples
```
1.
> What is the NEMO paper all about?
> NEMO proposes a system for extracting organization names from PubMed affiliation strings and normalizing them to a canonical organization name.
The system achieves more than 98% f-score in extracting organization names, and it uses clustering based on local sequence alignment metrics and local learning based on finding connected components for normalization.

2.
> Do you know something about Indian system to help indians better understand each other? Because they may speak different languages. Can you name such systems? Mention paper names as well.
> Yes, there are several systems and research papers that focus on helping Indians better understand each other by addressing the language barrier:

"Anusaaraka: Overcoming the Language Barrier in India" (2001) - This system aims to build multilingual speech-to-speech machine translation systems connecting all Indian languages.

MuRIL: Multilingual Representations for Indian Languages (2021) - This work focuses on improving multilingual language models to better represent and process Indian languages, which are often underrepresented in current models.

Exploiting Spectral Augmentation for Code-Switched Spoken Language Identification (2020) - While not specifically focused on machine translation, this paper discusses the importance of spoken language identification systems in a multilingual country like India to identify languages present in an audio sample.

These systems and research papers aim to address the challenges posed by language diversity in India's education sector and promote inclusivity among Indians who speak different languages.
```
