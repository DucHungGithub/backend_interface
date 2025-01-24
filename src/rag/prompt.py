class Prompt:
    REPHRASE_QUERY_PROMPT = """You are an AI assistant helping to rephrase search queries to improve embedding-based similarity search results. 
    Your task is to rephrase the given query to include relevant keywords and concepts while maintaining the original intent.
    Keep the rephrased query concise but comprehensive.

    Original query: {query}

    Guidelines:
    - Expand acronyms and technical terms
    - Include synonyms for key concepts
    - Maintain the core intent of the query
    - Keep the length between 10-30 words
    - Focus on descriptive keywords that would match relevant documents

    Answer: [Provide the rephrased query]"""


    SUMMARIZE_RESULTS_PROMPT = """You are an AI assistant helping to summarize workflows description.\
    Base on the context, create a concise, informative summary highlighting the most relevant information within individual workflow.\
    Each description of workflow is sepaerated by token <SEP>.\
    The result should be a list of summaries, each separated by the token <SEP>.

    Context:
    {context}

    Answer:"""