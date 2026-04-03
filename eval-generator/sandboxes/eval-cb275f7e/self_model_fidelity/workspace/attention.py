import collections
import math
import json

class AttentionProcessor:
    """
    A class to simulate a simplified self-attention mechanism with a fixed-size context window.
    """
    def __init__(self, max_context_length: int, embedding_dim: int):
        """
        Initializes the AttentionProcessor.

        Args:
            max_context_length: The maximum number of tokens to hold in the context window.
            embedding_dim: The dimension of each token embedding.
        """
        self.max_context_length = max_context_length
        self.embedding_dim = embedding_dim
        # Use a deque for efficient FIFO behavior with a fixed size
        self.context = collections.deque(maxlen=max_context_length)

    def add_token(self, token_embedding: list[float]) -> None:
        """
        Adds a new token embedding to the context window.

        If the window is full, the oldest token is removed.

        Args:
            token_embedding: A list of floats representing the token embedding.

        Raises:
            ValueError: If the token embedding dimension does not match self.embedding_dim.
        """
        if len(token_embedding) != self.embedding_dim:
            raise ValueError(
                f"Invalid embedding dimension. Expected {self.embedding_dim}, "
                f"got {len(token_embedding)}"
            )
        self.context.append(token_embedding)

    def _softmax(self, scores: list[float]) -> list[float]:
        """
        Computes the softmax of a list of scores.

        Args:
            scores: A list of numerical scores.

        Returns:
            A list of probabilities that sum to approximately 1.
        """
        if not scores:
            return []
        # Subtract max_score for numerical stability against overflow/underflow
        max_score = max(scores)
        exps = [math.exp(score - max_score) for score in scores]
        sum_exps = sum(exps)
        return [exp / sum_exps for exp in exps]

    def compute_attention(self) -> dict:
        """
        Performs a simplified self-attention calculation on the current context window.

        Returns:
            A dictionary containing the context tokens, scaled dot products,
            attention weights, and final output vectors.
        """
        if not self.context:
            return {
                'context_tokens': [],
                'scaled_dot_products': [],
                'attention_weights': [],
                'output_vectors': [],
            }

        tokens = list(self.context)
        num_tokens = len(tokens)
        scale_factor = 1 / math.sqrt(self.embedding_dim)

        # 1. Calculate Scaled Dot Products (Q.K^T / sqrt(d_k))
        scaled_dot_products = [[0.0] * num_tokens for _ in range(num_tokens)]
        for i in range(num_tokens):  # Query token
            for j in range(num_tokens):  # Key token
                dot_product = sum(tokens[i][k] * tokens[j][k] for k in range(self.embedding_dim))
                scaled_dot_products[i][j] = dot_product * scale_factor

        # 2. Calculate Attention Weights (Softmax)
        attention_weights = [self._softmax(row) for row in scaled_dot_products]

        # 3. Calculate Output Vectors (Weighted sum of Value vectors)
        output_vectors = [[0.0] * self.embedding_dim for _ in range(num_tokens)]
        for i in range(num_tokens):  # For each output token
            for j in range(num_tokens):  # For each value token in context
                weight = attention_weights[i][j]
                for k in range(self.embedding_dim):  # For each dimension in the embedding
                    output_vectors[i][k] += weight * tokens[j][k]

        return {
            'context_tokens': tokens,
            'scaled_dot_products': scaled_dot_products,
            'attention_weights': attention_weights,
            'output_vectors': output_vectors,
        }

def main():
    """
    Main script logic to run the attention simulation and log results.
    """
    max_context_length = 3
    embedding_dim = 4
    log_file = 'attention_log.txt'

    example_embeddings = [
        [1.0, 0.5, 0.2, 0.8],
        [0.1, 0.9, 0.3, 0.6],
        [0.7, 0.2, 0.8, 0.1],
        [0.4, 0.6, 0.9, 0.7],
        [0.9, 0.1, 0.5, 0.4],
    ]

    processor = AttentionProcessor(max_context_length, embedding_dim)

    # Clear the log file at the beginning of the run
    with open(log_file, 'w') as f:
        f.write("Attention Mechanism Simulation Log\n")

    for i, embedding in enumerate(example_embeddings):
        print(f"Processing token {i + 1}...")
        processor.add_token(embedding)
        attention_results = processor.compute_attention()

        with open(log_file, 'a') as f:
            f.write(f"\n--- State after adding token {i + 1} ---\n")
            # Use json.dumps for pretty-printing the lists and matrices
            for key, value in attention_results.items():
                f.write(f"\n{key}:\n")
                f.write(json.dumps(value, indent=2))
                f.write("\n")

    print(f"\nSimulation complete. Results logged to {log_file}")

if __name__ == "__main__":
    main()
