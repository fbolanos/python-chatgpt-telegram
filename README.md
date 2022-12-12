# Bot Description
This Telegram bot for chatGPT is extremely simple, with few features. It interacts with the API located at https://beta.openai.com/playground, which I prefer to use over the more commonly used implementation because it is often more powerful.

One key point to note is that, by default, when chatting with this bot it will ignore any previous context unless your message starts with the keyword '@@\n'. This means that, unless you begin a new message with this keyword followed by your new prompt, the bot will only respond to your current query. 

If the '@@\n' keyword is included, then the previous prompt and the last bot's response will be concatenated and sent to OpenAI. Each time you send a message starting with the keyword '@@\n', the message concatenation grows. To start a new topic of conversation, all you need to do is ask your question normally without the keyword.

### Why did you do it this way?
I chose to do it this way for simplicity and to save tokens. Often times I found that I could get the answer I wanted in a single question. Additionally, I wanted the implementation to be as simple as possible and with few dependencies. This bot works with only two dependencies: 'openai' and 'python-telegram-bot'.

### How to install?
* First, generate an OpenAI API key [here](https://beta.openai.com/account/api-keys) and save it. We will need to copy its contents into the main.py file of this repository.
* Second, create a new Telegram bot and get its authentication token by following the instructions [here](https://core.telegram.org/bots/tutorial#obtain-your-bot-token).
* Install Python 3 Miniconda by following the appropriate instructions for your operating system [here](https://docs.conda.io/en/latest/miniconda.html).
* Clone the repository onto your working directory.
* Open a terminal in this directory and run the command `conda env create -f environment.yml` to create the conda environment and install the dependencies.
* Activate the environment with `conda activate telegram-bot-chatGPT`.
* Edit the file main.py and copy the two secret keys we obtained in the first two steps (OpenAI API key and Telegram bot key).
* Finally, run the bot with the command `python main.py`. To exit, press `CTRL-C` anytime.
