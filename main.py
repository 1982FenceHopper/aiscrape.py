import pprint
import os
import sys
import mmap
import re
from schemas import news_schema, encyclopedia_schema
from py_dotenv import read_dotenv
import asyncio
import tiktoken

import scraper
import llm

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

data_dir = os.path.join(os.path.dirname(__file__), 'data')

schema_matcher = {
    "news": news_schema,
    "encyclopedia": encyclopedia_schema
}

def find_website_type(base_url: str):
    for name in os.listdir(data_dir):
        if os.path.isdir(os.path.join(data_dir, name)):
            for file in os.listdir(os.path.join(data_dir, name)):
                if file.endswith(".txt"):
                    with open(os.path.join(data_dir, name, file)) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
                        if s.find(bytes(base_url, 'utf-8')) != -1:
                            return name

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
                        
if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Usage: python main.py <url> <model>\n\nAvailable Models:\nllama3-groq-70b-8192-tool-use-preview, 8192 token context window\nmixtral-8x7b-32768, 32768 token context window\n\nNOTE: mixtral-8x7b-32768, although having a context window of 32768 tokens, is not originally intended for tool use. llama3-groq-70b-8192-tool-use-preview is recommended, albeit at 8192 token context window. However, the program will split the document over multiple calls if your document exceeds the tokens that the LLM can handle at a time, regardless of chosen model.")
        sys.exit(1)
    
    url = sys.argv[1]
    model = sys.argv[2]
    base_url = re.findall(r'(?m)http(?:s?):\/\/.*?([^\.\/]+?\.[^\.]+?)(?:\/|$)', url)
    url_type = find_website_type(base_url[0])
    schema_used = schema_matcher[url_type]
    
    print(f"[MAIN]: Detected URL Type: {url_type}")
    
    print(f"[SCRAPER]: Scraping document from {url}...")
    document = scraper.scrape(url=url)
    print(f"[MAIN]: Processing {num_tokens_from_string(f'{document}', 'cl100k_base')} tokens from document via LLM...")
    llm_processed = asyncio.run(llm.llm_extract(document=document, url=url, schema=schema_used, model=model))
    
    print("[MAIN]: Document processed successfully:\n")
    print(llm_processed[0])
    print()
    print(llm_processed[1])
    print(f"{num_tokens_from_string(llm_processed[1], 'cl100k_base')} tokens")