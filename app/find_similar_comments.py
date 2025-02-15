from sentence_transformers import SentenceTransformer, util

input_file = "/data/comments.txt"
output_file = "/data/comments-similar.txt"

model = SentenceTransformer("all-MiniLM-L6-v2")

try:
    with open(input_file, "r") as f:
        comments = [line.strip() for line in f.readlines()]

    embeddings = model.encode(comments, convert_to_tensor=True)
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)

    max_sim, best_pair = 0, None
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            sim_score = similarity_matrix[i][j].item()
            if sim_score > max_sim:
                max_sim, best_pair = sim_score, (comments[i], comments[j])

    with open(output_file, "w") as f:
        f.write("\n".join(best_pair))

    print("Identified most similar comments.")

except Exception as e:
    print(f"Error finding similar comments: {e}")
