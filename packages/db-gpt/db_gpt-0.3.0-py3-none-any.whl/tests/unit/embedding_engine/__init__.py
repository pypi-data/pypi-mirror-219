from pilot import EmbeddingEngine, KnowledgeType

embedding_model_path = (
    "/Users/chenketing/Desktop/project/DB-GPT-NEW/DB-GPT/models/text2vec-large-chinese"
)
vector_store_config = {
    "vector_store_type": "Chroma",
    "vector_store_name": "dddww",
    "chroma_persist_path": "/Users/chenketing/Desktop/project/DB-GPT-NEW/DB-GPT/pilot/data",
}
# if you have no test document embedding data, you can use db-gpt embedding engine api to embedding some test document
raw_text = """
    This is a document about the DB-GPT,
    is an experimental open-source project that uses localized GPT large models to interact with your data and environment. 
    With this solution, you can be assured that there is no risk of data leakage, and your data is 100% private and secure.
    Our vision is to make it easier and more convenient to build applications around databases and llm.
"""
embedding_engine = EmbeddingEngine(
    knowledge_type=KnowledgeType.TEXT.value,
    knowledge_source=raw_text,
    model_name=embedding_model_path,
    vector_store_config=vector_store_config,
)
embedding_engine.knowledge_embedding()
