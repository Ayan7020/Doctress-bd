from langchain_core.runnables import RunnableParallel, RunnableMap, RunnableLambda, RunnablePassthrough
from services.vector.VectorStoreLambda import VectorStoreRetrivalLambda
from services.langchainFlow.memory import MemoryRetrievalLambda
from services.langchainFlow.prompt  import prompt
from services.langchainFlow.llm import GroqLLm
from langchain_core.output_parsers import StrOutputParser

def format_docs(retrived_docs):
    print("Format Docs",retrived_docs)
    context_text = "\n\n".join(doc.page_content for doc in retrived_docs)
    return context_text

parallelchain = RunnableParallel({
    "context": VectorStoreRetrivalLambda | RunnableLambda(format_docs),
    "input": RunnablePassthrough(),
    "chat_history": MemoryRetrievalLambda
})

parser = StrOutputParser()

MainChain = parallelchain | prompt | GroqLLm | parser     