from mem0 import Memory

from configs import env

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": env.NEBIUS_API_KEY,
            "model": "Qwen/Qwen3-Embedding-8B",
            "openai_base_url": "https://api.studio.nebius.com/v1/",
            "embedding_dims": 4096,
        },
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": env.NEBIUS_API_KEY,
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-fast",
            "openai_base_url": "https://api.studio.nebius.com/v1/",
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "vector-db", "port": 6333, "embedding_model_dims": 4096},
    },
}

memory_client = Memory.from_config(config)
