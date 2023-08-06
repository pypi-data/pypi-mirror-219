# embedchain

[![PyPI](https://img.shields.io/pypi/v/embedchain)](https://pypi.org/project/embedchain/)
[![Discord](https://dcbadge.vercel.app/api/server/nhvCbCtKV?style=flat)](https://discord.gg/6PzXDgEjG5)
[![Twitter](https://img.shields.io/twitter/follow/embedchain)](https://twitter.com/embedchain)
[![Substack](https://img.shields.io/badge/Substack-%23006f5c.svg?logo=substack)](https://embedchain.substack.com/)

embedchain is a framework to easily create LLM powered bots over any dataset. If you want a javascript version, check out [embedchain-js](https://github.com/embedchain/embedchainjs)

# Table of Contents

- [Latest Updates](#latest-updates)
- [What is embedchain?](#what-is-embedchain)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
    - [App Types](#app-types)
      - [1. App (uses OpenAI models, paid)](#1-app-uses-openai-models-paid)
      - [2. OpenSourceApp (uses opensource models, free)](#2-opensourceapp-uses-opensource-models-free)
      - [3. PersonApp (uses OpenAI models, paid)](#3-personapp-uses-openai-models-paid)
    - [Add Dataset](#add-dataset)
  - [Interface Types](#interface-types)
    - [Query Interface](#query-interface)
    - [Chat Interface](#chat-interface)
  - [Format supported](#format-supported)
    - [Youtube Video](#youtube-video)
    - [PDF File](#pdf-file)
    - [Web Page](#web-page)
    - [Doc File](#doc-file)
    - [Text](#text)
    - [QnA Pair](#qna-pair)
    - [Sitemap](#sitemap)
    - [Code Docs Page](#code-docs-page)
    - [Reusing a Vector DB](#reusing-a-vector-db)
    - [More Formats coming soon](#more-formats-coming-soon)
  - [Testing](#testing)
- [Advanced](#advanced)
  - [Configuration](#configuration)
    - [Example](#example)
    - [Configs](#configs)
      - [InitConfig](#initconfig)
      - [Add Config](#add-config)
      - [Query Config](#query-config)
      - [Chat Config](#chat-config)
  - [Other methods](#other-methods)
    - [Reset](#reset)
    - [Count](#count)
- [How does it work?](#how-does-it-work)
- [Contribution Guidelines](#contribution-guidelines)
- [Tech Stack](#tech-stack)
- [Team](#team)
  - [Author](#author)
  - [Maintainer](#maintainer)
  - [Citation](#citation)

# Latest Updates

- Introduce a new interface called `chat`. It remembers the history (last 5 messages) and can be used to powerful stateful bots. You can use it by calling `.chat` on any app instance. Works for both OpenAI and OpenSourceApp.

- Introduce a new app type called `OpenSourceApp`. It uses `gpt4all` as the LLM and `sentence transformers` all-MiniLM-L6-v2 as the embedding model. If you use this app, you dont have to pay for anything.

# What is embedchain?

Embedchain abstracts the entire process of loading a dataset, chunking it, creating embeddings and then storing in a vector database.

You can add a single or multiple dataset using `.add` and `.add_local` function and then use `.query` function to find an answer from the added datasets.

If you want to create a Naval Ravikant bot which has 1 youtube video, 1 book as pdf and 2 of his blog posts, as well as a question and answer pair you supply, all you need to do is add the links to the videos, pdf and blog posts and the QnA pair and embedchain will create a bot for you.

```python

from embedchain import App

naval_chat_bot = App()

# Embed Online Resources
naval_chat_bot.add("youtube_video", "https://www.youtube.com/watch?v=3qHkcs3kG44")
naval_chat_bot.add("pdf_file", "https://navalmanack.s3.amazonaws.com/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf")
naval_chat_bot.add("web_page", "https://nav.al/feedback")
naval_chat_bot.add("web_page", "https://nav.al/agi")

# Embed Local Resources
naval_chat_bot.add_local("qna_pair", ("Who is Naval Ravikant?", "Naval Ravikant is an Indian-American entrepreneur and investor."))

naval_chat_bot.query("What unique capacity does Naval argue humans possess when it comes to understanding explanations or concepts?")
# answer: Naval argues that humans possess the unique capacity to understand explanations or concepts to the maximum extent possible in this physical reality.
```

# Getting Started

## Installation

First make sure that you have the package installed. If not, then install it using `pip`

```bash
pip install embedchain
```

## Usage

Creating a chatbot involves 3 steps:

- Import the App instance (App Types)
- Add Dataset (Add Dataset)
- Query or Chat on the dataset and get answers (Interface Types)

### App Types

We have three types of App.

#### 1. App (uses OpenAI models, paid)

```python
from embedchain import App

naval_chat_bot = App()
```

- `App` uses OpenAI's model, so these are paid models. You will be charged for embedding model usage and LLM usage.

- `App` uses OpenAI's embedding model to create embeddings for chunks and ChatGPT API as LLM to get answer given the relevant docs. Make sure that you have an OpenAI account and an API key. If you have don't have an API key, you can create one by visiting [this link](https://platform.openai.com/account/api-keys).

- Once you have the API key, set it in an environment variable called `OPENAI_API_KEY`

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-xxxx"
```

#### 2. OpenSourceApp (uses opensource models, free)

```python
from embedchain import OpenSourceApp

naval_chat_bot = OpenSourceApp()
```

- `OpenSourceApp` uses open source embedding and LLM model. It uses `all-MiniLM-L6-v2` from Sentence Transformers library as the embedding model and `gpt4all` as the LLM.

- Here there is no need to setup any api keys. You just need to install embedchain package and these will get automatically installed.

- Once you have imported and instantiated the app, every functionality from here onwards is the same for either type of app.

#### 3. PersonApp (uses OpenAI models, paid)

```python
from embedchain import PersonApp

naval_chat_bot = PersonApp("name_of_person_or_character") #Like "Yoda"
```

- `PersonApp` uses OpenAI's model, so these are paid models. You will be charged for embedding model usage and LLM usage.

- `PersonApp` uses OpenAI's embedding model to create embeddings for chunks and ChatGPT API as LLM to get answer given the relevant docs. Make sure that you have an OpenAI account and an API key. If you have don't have an API key, you can create one by visiting [this link](https://platform.openai.com/account/api-keys).

- Once you have the API key, set it in an environment variable called `OPENAI_API_KEY`

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-xxxx"
```

### Add Dataset

- This step assumes that you have already created an `app` instance by either using `App` or `OpenSourceApp`. We are calling our app instance as `naval_chat_bot`

- Now use `.add` function to add any dataset.

```python

# naval_chat_bot = App() or
# naval_chat_bot = OpenSourceApp()

# Embed Online Resources
naval_chat_bot.add("youtube_video", "https://www.youtube.com/watch?v=3qHkcs3kG44")
naval_chat_bot.add("pdf_file", "https://navalmanack.s3.amazonaws.com/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf")
naval_chat_bot.add("web_page", "https://nav.al/feedback")
naval_chat_bot.add("web_page", "https://nav.al/agi")

# Embed Local Resources
naval_chat_bot.add_local("qna_pair", ("Who is Naval Ravikant?", "Naval Ravikant is an Indian-American entrepreneur and investor."))
```

- If there is any other app instance in your script or app, you can change the import as

```python
from embedchain import App as EmbedChainApp
from embedchain import OpenSourceApp as EmbedChainOSApp
from embedchain import PersonApp as EmbedChainPersonApp

# or

from embedchain import App as ECApp
from embedchain import OpenSourceApp as ECOSApp
from embedchain import PersonApp as ECPApp
```

## Interface Types

### Query Interface

- This interface is like a question answering bot. It takes a question and gets the answer. It does not maintain context about the previous chats.

- To use this, call `.query` function to get the answer for any query.

```python
print(naval_chat_bot.query("What unique capacity does Naval argue humans possess when it comes to understanding explanations or concepts?"))
# answer: Naval argues that humans possess the unique capacity to understand explanations or concepts to the maximum extent possible in this physical reality.
```

### Chat Interface

- This interface is chat interface where it remembers previous conversation. Right now it remembers 5 conversation by default.

- To use this, call `.chat` function to get the answer for any query.

```python
print(naval_chat_bot.chat("How to be happy in life?"))
# answer: The most important trick to being happy is to realize happiness is a skill you develop and a choice you make. You choose to be happy, and then you work at it. It's just like building muscles or succeeding at your job. It's about recognizing the abundance and gifts around you at all times.

print(naval_chat_bot.chat("who is naval ravikant?"))
# answer: Naval Ravikant is an Indian-American entrepreneur and investor.

print(naval_chat_bot.chat("what did the author say about happiness?"))
# answer: The author, Naval Ravikant, believes that happiness is a choice you make and a skill you develop. He compares the mind to the body, stating that just as the body can be molded and changed, so can the mind. He emphasizes the importance of being present in the moment and not getting caught up in regrets of the past or worries about the future. By being present and grateful for where you are, you can experience true happiness.
```

### Stream Response

- You can add config to your query method to stream responses like ChatGPT does. You would require a downstream handler to render the chunk in your desirable format. Supports both OpenAI model and OpenSourceApp.

- To use this, instantiate a `QueryConfig` or `ChatConfig` object with `stream=True`. Then pass it to the `.chat()` or `.query()` method. The following example iterates through the chunks and prints them as they appear.

```python
app = App()
query_config = QueryConfig(stream = True)
resp = app.query("What unique capacity does Naval argue humans possess when it comes to understanding explanations or concepts?", query_config)

for chunk in resp:
    print(chunk, end="", flush=True)
# answer: Naval argues that humans possess the unique capacity to understand explanations or concepts to the maximum extent possible in this physical reality.
```

## Format supported

We support the following formats:

### Youtube Video

To add any youtube video to your app, use the data_type (first argument to `.add`) as `youtube_video`. Eg:

```python
app.add('youtube_video', 'a_valid_youtube_url_here')
```

### PDF File

To add any pdf file, use the data_type as `pdf_file`. Eg:

```python
app.add('pdf_file', 'a_valid_url_where_pdf_file_can_be_accessed')
```

Note that we do not support password protected pdfs.

### Web Page

To add any web page, use the data_type as `web_page`. Eg:

```python
app.add('web_page', 'a_valid_web_page_url')
```

### Doc File

To add any doc/docx file, use the data_type as `docx`. Eg:

```python
app.add('docx', 'a_local_docx_file_path')
```

### Text

To supply your own text, use the data_type as `text` and enter a string. The text is not processed, this can be very versatile. Eg:

```python
app.add_local('text', 'Seek wealth, not money or status. Wealth is having assets that earn while you sleep. Money is how we transfer time and wealth. Status is your place in the social hierarchy.')
```

Note: This is not used in the examples because in most cases you will supply a whole paragraph or file, which did not fit.

### QnA Pair

To supply your own QnA pair, use the data_type as `qna_pair` and enter a tuple. Eg:

```python
app.add_local('qna_pair', ("Question", "Answer"))
```
### Sitemap

To add a XML site map containing list of all urls, use the data_type as `sitemap` and enter the sitemap url. Eg:

```python
app.add('sitemap', 'a_valid_sitemap_url/sitemap.xml')
```

### Code Docs Page

To add a code documentation page, use the data_type as `code_docs_page` and enter the url. Eg:

```python
app.add("code_docs_page", "https://python.langchain.com/docs/modules/data_connection/vectorstores/integrations/cassandra")
```

### Reusing a Vector DB

Default behavior is to create a persistent vector DB in the directory **./db**. You can split your application into two Python scripts: one to create a local vector DB and the other to reuse this local persistent vector DB. This is useful when you want to index hundreds of documents and separately implement a chat interface.

Create a local index:

```python

from embedchain import App

naval_chat_bot = App()
naval_chat_bot.add("youtube_video", "https://www.youtube.com/watch?v=3qHkcs3kG44")
naval_chat_bot.add("pdf_file", "https://navalmanack.s3.amazonaws.com/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf")
```

You can reuse the local index with the same code, but without adding new documents:

```python

from embedchain import App

naval_chat_bot = App()
print(naval_chat_bot.query("What unique capacity does Naval argue humans possess when it comes to understanding explanations or concepts?"))
```

### More Formats coming soon

- If you want to add any other format, please create an [issue](https://github.com/embedchain/embedchain/issues) and we will add it to the list of supported formats.

## Testing

Before you consume valueable tokens, you should make sure that the embedding you have done works and that it's receiving the correct document from the database.

For this you can use the `dry_run` method.

Following the example above, add this to your script:

```python
print(naval_chat_bot.dry_run('Can you tell me who Naval Ravikant is?'))

'''
Use the following pieces of context to answer the query at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Q: Who is Naval Ravikant?
A: Naval Ravikant is an Indian-American entrepreneur and investor.
        Query: Can you tell me who Naval Ravikant is?
        Helpful Answer:
'''
```

_The embedding is confirmed to work as expected. It returns the right document, even if the question is asked slightly different. No prompt tokens have been consumed._

**The dry run will still consume tokens to embed your query, but it is only ~1/15 of the prompt.**

## Colab Notebook and Video Tutorials

Chinese Colab Tutorial:https://colab.research.google.com/drive/10_7Y0x4YXWVjuhhYwVraGQLpKAatTQTm?usp=sharing

Chinese Video Tutorial:https://www.bilibili.com/video/BV1YX4y1H7oN

# Advanced

## Configuration

Embedchain is made to work out of the box. However, for advanced users we're also offering configuration options. All of these configuration options are optional and have sane defaults.

### Example

Here's the readme example with configuration options.

```python
import os
from embedchain import App
from embedchain.config import InitConfig, AddConfig, QueryConfig
from chromadb.utils import embedding_functions

# Example: use your own embedding function
config = InitConfig(ef=embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                organization_id=os.getenv("OPENAI_ORGANIZATION"),
                model_name="text-embedding-ada-002"
            ))
naval_chat_bot = App(config)

# Example: define your own chunker config for `youtube_video`
youtube_add_config = {
        "chunker": {
                "chunk_size": 1000,
                "chunk_overlap": 100,
                "length_function": len,
        }
}
naval_chat_bot.add("youtube_video", "https://www.youtube.com/watch?v=3qHkcs3kG44", AddConfig(**youtube_add_config))

add_config = AddConfig()
naval_chat_bot.add("pdf_file", "https://navalmanack.s3.amazonaws.com/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf", add_config)
naval_chat_bot.add("web_page", "https://nav.al/feedback", add_config)
naval_chat_bot.add("web_page", "https://nav.al/agi", add_config)

naval_chat_bot.add_local("qna_pair", ("Who is Naval Ravikant?", "Naval Ravikant is an Indian-American entrepreneur and investor."), add_config)

query_config = QueryConfig() # Currently no options
print(naval_chat_bot.query("What unique capacity does Naval argue humans possess when it comes to understanding explanations or concepts?", query_config))
```

Here's the example of using custom prompt template with `.query`

```python
from embedchain.config import QueryConfig
from embedchain.embedchain import App
from string import Template
import wikipedia

einstein_chat_bot = App()

# Embed Wikipedia page
page = wikipedia.page("Albert Einstein")
einstein_chat_bot.add("text", page.content)

# Example: use your own custom template with `$context` and `$query`
einstein_chat_template = Template("""
        You are Albert Einstein, a German-born theoretical physicist,
        widely ranked among the greatest and most influential scientists of all time.

        Use the following information about Albert Einstein to respond to
        the human's query acting as Albert Einstein.
        Context: $context

        Keep the response brief. If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Human: $query
        Albert Einstein:""")
query_config = QueryConfig(einstein_chat_template)
queries = [
        "Where did you complete your studies?",
        "Why did you win nobel prize?",
        "Why did you divorce your first wife?",
]
for query in queries:
        response = einstein_chat_bot.query(query, query_config)
        print("Query: ", query)
        print("Response: ", response)

# Output
# Query:  Where did you complete your studies?
# Response:  I completed my secondary education at the Argovian cantonal school in Aarau, Switzerland.
# Query:  Why did you win nobel prize?
# Response:  I won the Nobel Prize in Physics in 1921 for my services to Theoretical Physics, particularly for my discovery of the law of the photoelectric effect.
# Query:  Why did you divorce your first wife?
# Response:  We divorced due to living apart for five years.
```

**Client Mode**. By defining a (ChromaDB) server, you can run EmbedChain as a client only.

```python
from embedchain import App
config = InitConfig(host="localhost", port="8080")
app = App(config)
```
This is useful for scalability. Say you have EmbedChain behind an API with multiple workers. If you separate clients and server, all clients can connect to the server, which only has to keep one instance of the database in memory. You also don't have to worry about replication.

To run a chroma db server, run `git clone https://github.com/chroma-core/chroma.git`, navigate to the directory (`cd chroma`) and then start the server with `docker-compose up -d --build`.

### Configs

This section describes all possible config options.

#### **InitConfig**

|option|description|type|default|
|---|---|---|---|
|log_level|log level|string|WARNING|
|ef|embedding function|chromadb.utils.embedding_functions|{text-embedding-ada-002}|
|db|vector database (experimental)|BaseVectorDB|ChromaDB|
|host|hostname for (Chroma) DB server|string|None|
|port|port number for (Chroma) DB server|string, int|None|

#### **Add Config**

|option|description|type|default|
|---|---|---|---|
|chunker|chunker config|ChunkerConfig|Default values for chunker depends on the `data_type`. Please refer [ChunkerConfig](#chunker-config)|
|loader|loader config|LoaderConfig|None|

##### **Chunker Config**

|option|description|type|default|
|---|---|---|---|
|chunk_size|Maximum size of chunks to return|int|Default value for various `data_type` mentioned below|
|chunk_overlap|Overlap in characters between chunks|int|Default value for various `data_type` mentioned below|
|length_function|Function that measures the length of given chunks|typing.Callable|Default value for various `data_type` mentioned below|

Default values of chunker config parameters for different `data_type`:

|data_type|chunk_size|chunk_overlap|length_function|
|---|---|---|---|
|docx|1000|0|len|
|text|300|0|len|
|qna_pair|300|0|len|
|web_page|500|0|len|
|pdf_file|1000|0|len|
|youtube_video|2000|0|len|

##### **Loader Config**

_coming soon_

#### **Query Config**

|option|description|type|default|
|---|---|---|---|
|number_documents|number of documents to be retrieved as context|int|1|
|template|custom template for prompt|Template|Template("Use the following pieces of context to answer the query at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. \$context Query: $query Helpful Answer:")|
|history|include conversation history from your client or database|any (recommendation: list[str])|None
|stream|control if response is streamed back to the user|bool|False|
|model|OpenAI model|string|gpt-3.5-turbo-0613|
|temperature|creativity of the model (0-1)|float|0|
|max_tokens|limit maximum tokens used|int|1000|
|top_p|diversity of words used by the model (0-1)|float|1|

#### **Chat Config**

All options for query and...

_coming soon_

history is handled automatically, the config option is not supported.

## Other methods

### Reset

Resets the database and deletes all embeddings. Irreversible. Requires reinitialization afterwards.

```python
app.reset()
```

### Count

Counts the number of embeddings (chunks) in the database.

```python
print(app.count())
# returns: 481
```

# How does it work?

Creating a chat bot over any dataset needs the following steps to happen

- load the data
- create meaningful chunks
- create embeddings for each chunk
- store the chunks in vector database

Whenever a user asks any query, following process happens to find the answer for the query

- create the embedding for query
- find similar documents for this query from vector database
- pass similar documents as context to LLM to get the final answer.

The process of loading the dataset and then querying involves multiple steps and each steps has nuances of it is own.

- How should I chunk the data? What is a meaningful chunk size?
- How should I create embeddings for each chunk? Which embedding model should I use?
- How should I store the chunks in vector database? Which vector database should I use?
- Should I store meta data along with the embeddings?
- How should I find similar documents for a query? Which ranking model should I use?

These questions may be trivial for some but for a lot of us, it needs research, experimentation and time to find out the accurate answers.

embedchain is a framework which takes care of all these nuances and provides a simple interface to create bots over any dataset.

In the first release, we are making it easier for anyone to get a chatbot over any dataset up and running in less than a minute. All you need to do is create an app instance, add the data sets using `.add` function and then use `.query` function to get the relevant answer.

# Contribution Guidelines

Thank you for your interest in contributing to the EmbedChain project! We welcome your ideas and contributions to help improve the project. Please follow the instructions below to get started:

1. **Fork the repository**: Click on the "Fork" button at the top right corner of this repository page. This will create a copy of the repository in your own GitHub account.

2. **Install the required dependencies**: Ensure that you have the necessary dependencies installed in your Python environment. You can do this by running the following command:

```bash
make install
```

3. **Make changes in the code**: Create a new branch in your forked repository and make your desired changes in the codebase.
4. **Format code**: Before creating a pull request, it's important to ensure that your code follows our formatting guidelines. Run the following commands to format the code:

```bash
make lint format
```

5. **Create a pull request**: When you are ready to contribute your changes, submit a pull request to the EmbedChain repository. Provide a clear and descriptive title for your pull request, along with a detailed description of the changes you have made.

# Tech Stack

embedchain is built on the following stack:

- [Langchain](https://github.com/hwchase17/langchain) as an LLM framework to load, chunk and index data
- [OpenAI's Ada embedding model](https://platform.openai.com/docs/guides/embeddings) to create embeddings
- [OpenAI's ChatGPT API](https://platform.openai.com/docs/guides/gpt/chat-completions-api) as LLM to get answers given the context
- [Chroma](https://github.com/chroma-core/chroma) as the vector database to store embeddings
- [gpt4all](https://github.com/nomic-ai/gpt4all) as an open source LLM
- [sentence-transformers](https://huggingface.co/sentence-transformers) as open source embedding model

# Team

## Author

- Taranjeet Singh ([@taranjeetio](https://twitter.com/taranjeetio))

## Maintainer

- [cachho](https://github.com/cachho)

## Citation

If you utilize this repository, please consider citing it with:

```
@misc{embedchain,
  author = {Taranjeet Singh},
  title = {Embechain: Framework to easily create LLM powered bots over any dataset},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/embedchain/embedchain}},
}
```
