# Summary of My LLM Learning Journey

## 1. Embeddings
---
#### Image Embeddings
- **Definition:** Image embeddings refer to the representation of images in a lower-dimensional space.
- **Purpose:** They are used to capture meaningful information and features of images.

#### Sentence Embeddings
- **Definition:** Sentence embeddings represent sentences in a vector space, capturing semantic information.
- **Purpose:** Useful for various natural language processing tasks like similarity comparison and text classification.

#### Vectors Similarity and Distance Metrics

- Euclidean Distance
- Dot Product
- Cosine Similarity

#### Vectors Searching Metrics

- K-Nearest Neighbors (KNN)
- Hierarchical Navigable Small Worlds (HNSW)
  - Faster than KNN algorithm
  - Default algorithm used in Weaviate Vector DB

---

## 2. Vector-DB (Weaviate)

#### Introduction
- How to create Embedding Client
- How to create schema
- How to insert embedding into the created schema
- How to get vector embedding similar or nearest in distance to the query vector