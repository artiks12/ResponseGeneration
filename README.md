# ResponseGeneration
This is the repository to generate responses for models. It is a part of the master thesis "Evaluation and Adaptation of Large Language Models for Question-Answering on Legislation" made in University of Latvia.

### How to Use
This script was used with Python 3.10 so it is recomended to use this version of python. You also need to install ollama, google and openai packages.

First you need to get instructions to pass to the models. The repository that prepares these instructions is available here: https://github.com/artiks12/DatasetPreperation. You need to place them in "instructions" folder.

The file getModelResponses.py contains examples on how to run response generation for each endpoint. Make sure you specify your keys for Gemini and OpenRouter endpoints and/or download and run ollama on your computer or Docker (https://hub.docker.com/r/ollama/ollama).

Once everything is configured, run the script and answers will be generated and stored in ModelResponses folder. Files are saved after each response and youu can continue generating responses in case you haven't finished everything.

### Supported endpoints
- Google Gemini endpoint
- OpenRouter endpoints
- Ollama
