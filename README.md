# aiscrape.py

### Simple website scraper, using AI to help parse it.

This is a simple project, very unfinished and needs a lot of work, but it works I guess.

Libraries and Tools Used:

- LangChain, for interacting with the LLM via Function/Tool calling
- BeautifulSoup4, for parsing the raw HTML document
- Playwright, for getting the HTML from a url
- GroqCloud, for providing the LLM

---

## Requirements

### Packages

- Python => 3.10.12
- `langchain` => 0.2.13
- `langchain-community` => 0.2.12
- `langchain-core` => 0.2.30
- `langchain-groq` => 0.1.9
- `langchain-text-splitters` => 0.2.2
- `playwright` => 1.46.0
- `beautifulsoup4` => 4.12.3
- `tiktoken` => 0.7.0
- `py-dotenv` => 0.1 (Because at the time of writing this README, `python-dotenv` fails to install via pip, and I&#39;m too lazy to try manually installing it)

### Getting Started

**Before Starting, make sure to make a `.env` file in the root working directory, and put in your Groq API key, with the env variable named as `GROQ_API_KEY`, GroqCloud provides free API keys, signup [here](https://groq.com/)**

---

## Usage

`python main.py <url> <model>`

### URL

URL of the website.

**Supported Websites**

News and Encyclopedia, view the `data/` folder for lists of websites supported.

### Model

Model to be used

**Supported Models (Provided by GroqCloud)**

`llama3-groq-70b-8192-tool-use-preview` (Recommended)
`llama3-groq-8b-8192-tool-use-preview` (Works)
`mixtral-8x7b-32768` (NOTE: Broken as of now, trying to figure out what the actual token limit of this model is, considering context window is 32,768 tokens, but i can only request 5,000 a minute??)

---

## How it works

Firstly, `main.py` uses a RegEx pattern to cleanup the URL and check which category it goes into (i.e. encyclopedia or news), once it figures that out, it continues on to the main show.

`main.py` calls `scrape.py` to scrape the url user provided, it uses LangChain&#39;s implementation of Playwright&#39;s browser call and BeautifulSoup4&#39;s document parser, namely `AsyncChromiumLoader` and `BeautifulSoupTransformer`.

From there, `scrape.py` navigates to the website, grabs all the entire HTML document, and cleans it up to reduce the tokens needed to pass into the LLM. It then returns the cleaned up document back to `main.py`

`main.py`, from there, calls upon `llm.py`, passing it the document, the Pydantic schema associated with the category of the URL, the URL itself (not used as of now), and the model the user desires to use. `llm.py` then creates 2 LLM objects, one for parsing the HTML document, and one for choosing the best one (we will get to that later). Both use the model the user chose for simplicity&#39;s sake.

From there, `llm.py` binds the first LLM with the schema associated with the website type, and the LangChain `RecursiveCharacterTextSplitter` object is used to split the document into chunks of `8192` tokens, via the `from_tiktoken_encoder` method (LangChain&#39;s method implementation, basically calling a function from the package `tiktoken`). Reason for the split is to ensure the document doesn&#39;t overload the LLM&#39;s context window. As such, if the document IS split, then multiple sequential calls are made.

Basically, we have multiple chunks, each having their own description of the encyclopedia entry/news article. Thats where the second model comes in. The second model decides which description is the best one, and sends us an index number, which is used to access the list of chunks, and return the one the LLM chose. From there, this description is returned back to `main.py`, and `main.py` simply prints it with the title of the entry/article. Also, if there is only one chunk, the second LLM simply

---

## To-Do

- [x] Make the app itself (duh)
- [x] Add the HTML document scraping function
- [x] Add the LLM interaction part
- [x] Use pydantic to handle schemas related to handling HTML documents
- [ ] Lower the need for dependencies (Definitely first on the list)
- [ ] Add support for multiple URLs (Planned)
- [ ] Add support for more LLM providers (OpenAI, Mistral, Google, Anthropic) (NOTE: unless I can find a way to do this for free, this is gonna be one hell of an expensive one and maybe not possible soon, or at all if I truly value my bank account [currently broke though, just a high school student])
- [ ] Make a paid version of the app with better scraping, on-demand LLMs (no need to bring your own) and ability to export to file formats such as CSV (This is a potential solution for the previous To-Do, and is doable)

I&#39;ll try my best to support this, but with school starting soon and me going into grade 11 (thats gonna suck considering I took the hardest stuff to date T_T), I may not have time, but I will try nonetheless

---

## This project is under the GNU GPLv3 License, view `LICENSE` for more details
