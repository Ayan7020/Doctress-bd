from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone , ServerlessSpec
from core.embedding import EmbeddingModel
from core.config import settings
import numpy as np

index_name = "doctress"
embedding_dim = np.array(EmbeddingModel.embed_query("test")).shape[0]

pc = Pinecone(
    api_key=settings.PINECONE_API_KEY
)

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=embedding_dim,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    
VectorStore = PineconeVectorStore(
    index_name=index_name, 
    embedding=EmbeddingModel,
    pinecone_api_key=settings.PINECONE_API_KEY
)

VectorStoreRetrival = VectorStore.as_retriever()