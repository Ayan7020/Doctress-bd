from langchain_huggingface import HuggingFaceEmbeddings

EmbeddingModel = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="/modelEmbedding"
)