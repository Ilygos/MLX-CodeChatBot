# MLX Code ChatBot

This is a simple lightweight chat bot using MLX, Code Gemma and TK-Inter

Model: codegemma-7b-it-8bit (https://huggingface.co/mlx-community/codegemma-1.1-7b-it-8bit)

### Starter

- if you do not have python on macos with homebrew

```bash
brew install python-tk
```
- Install the environment

```bash
python3 -m venv path/to/venv
source path/to/venv/bin/activate
python3 -m pip install mlx
python3 -m pip install mlx-lm
python3 -m pip install transformers
```

- The chatbot requires a HuggingFace connection to download the model 
https://pypi.org/project/huggingface-hub/

```bash
python3 -m pip install huggingface_hub
huggingface-cli login
# or using an environment variable
huggingface-cli login --token $HUGGINGFACE_TOKEN
```

- Now move to the root of your project

```bash
python3 chat.py
```

- ENJOY !

### Limitations

- The model used for now is really lightweight and not tweek for our side so there might be issues with the answers
- There are not context cache so each answer will be separately treated
- For now the code part is not formated making it a bit complicated to read
- Japanese is not yet supported so prompt must be in English