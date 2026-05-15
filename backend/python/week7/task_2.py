import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from week7.embeddings import generate_embeddings_for_texts
from week7.semantic_search import cosine_similarity_manually

# use of PCA : it converts 384D of embedding to 2D which makes it easy for us to plot


def main():
    product_name = [
        "Lego Castle",
        "Wooden Blocks",
        "Action Figure",
    ]
    # embedding models understand meaning from context, not just names
    product_texts = [
        "Lego Castle brick set for building a castle with towers and walls for kids",
        "Wooden Blocks stackable wooden pieces for making shapes, houses, and small structures",
        "Action Figure superhero character toy for roleplay, battles, and imaginative adventures",
    ]
    embeddings = generate_embeddings_for_texts(
        product_texts, model_name="all-MiniLM-L6-v2")
    sim_lego_wooden = cosine_similarity_manually(
        embeddings[0], embeddings[1])
    sim_lego_action = cosine_similarity_manually(
        embeddings[0], embeddings[2])
    sim_wooden_action = cosine_similarity_manually(
        embeddings[1], embeddings[2])
    print("\nPairwise Cosine Similarity")
    print("----------------------------------------------------------------------------------------------------------------------------")
    print(f"Lego Castle vs Wooden Blocks   : {sim_lego_wooden:.4f}")
    print(f"Lego Castle vs Action Figure   : {sim_lego_action:.4f}")
    print(f"Wooden Blocks vs Action Figure : {sim_wooden_action:.4f}")

    pca = PCA(n_components=2)
    embeddings_2d = pca.fit_transform(embeddings)
    plt.figure(figsize=(8, 6))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], s=120)
    for index, name in enumerate(product_name):
        plt.annotate(
            name,
            (embeddings_2d[index, 0], embeddings_2d[index, 1]),
            xytext=(8, 8),
            textcoords="offset points",
        )
    plt.title("PCA Projection of 3 Product Embeddings")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
