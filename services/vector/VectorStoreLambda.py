from services.vector.VectorStore import VectorStore
from langchain_core.runnables import RunnableLambda


VectorStoreRetrivalLambda = RunnableLambda(
    lambda input: VectorStore.max_marginal_relevance_search(
        input["query"],
        k=6,
        filter={
            "companyName": input["companyName"],
            "department": input["department"]  
        }
    )
)