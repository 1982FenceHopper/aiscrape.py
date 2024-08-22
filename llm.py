from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pprint

from schemas import best_choice_schema

async def llm_extract(document, url: str, schema: dict, model: str):
    raw_processed = []
    main_content = []
    final_result = []
    
    llm = ChatGroq(temperature=0, model=model, max_tokens=8192)
    tool_bound_llm = llm.with_structured_output(schema)
    
    choice_llm = ChatGroq(temperature=1, model=model, max_tokens=8192)
    tool_bound_cllm = choice_llm.with_structured_output(best_choice_schema)
    
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=8192, chunk_overlap=0)
    splits = splitter.split_documents(document)
    # pprint.pprint(splits)
    
    for i, split in enumerate(splits):
        print(f"[LLM]: Processing input chunk {i+1} of {len(splits)}...")
        # pprint.pprint(f"{split.page_content}")
        raw_processed.append(await tool_bound_llm.ainvoke(f"{split.page_content}"))
    
    if len(raw_processed) > 2:
        for i, chunk in enumerate(raw_processed):
            main_content.append(f"{chunk.content}")
            
        best_content = await tool_bound_cllm.ainvoke(f"{str(main_content)}")
        final_result.append(raw_processed[int(best_content.choice)].entry)
        final_result.append(main_content[int(best_content.choice)])
    else:
        final_result.append(raw_processed[0].entry)
        final_result.append(raw_processed[0].content)
    
    return final_result