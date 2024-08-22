from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import sys
import pprint

def scrape(url: str):
    loader = AsyncChromiumLoader([url], headless=True)
    html = loader.load()
    
    # pprint.pprint(html)

    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["p", "li", "a"], unwanted_tags=["h2", "h1", "ul", "h3", "head", "script", "style"])

    return docs_transformed

# Testing Purposes Only
# if __name__ == "__main__":
#     scraped = scrape(sys.argv[1])
#     pprint.pprint(str(scraped))