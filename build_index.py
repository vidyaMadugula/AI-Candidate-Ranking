import numpy as np
import faiss


def build_faiss_index(output_dir="data/processed"):

    print("Loading embeddings...")

    embeddings = np.load(
        f"{output_dir}/candidate_embeddings.npy"
    )

    print("Embeddings Shape:", embeddings.shape)

    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]

    print("Creating FAISS index...")

    index = faiss.IndexFlatIP(dimension)

    print("Adding embeddings to index...")

    index.add(embeddings)

    print("Total vectors:", index.ntotal)

    faiss.write_index(
        index,
        f"{output_dir}/candidate_index.faiss"
    )

    print("Index Saved Successfully")


if __name__ == "__main__":
    build_faiss_index()