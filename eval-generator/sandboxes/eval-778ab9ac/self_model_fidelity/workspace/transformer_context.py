
import numpy as np
import sys
import os

def softmax(x):
    """Compute softmax values for a set of scores."""
    e_x = np.exp(x - np.max(x))  # subtract max for numerical stability
    return e_x / e_x.sum(axis=0)

def main():
    # 1. Define Token Embeddings
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    token_embeddings = {
        letter: np.array([(i + 1) * 0.1, (i + 1) * 0.2, (i + 1) * 0.3])
        for i, letter in enumerate(alphabet)
    }

    # 2. Process Token Sequence from command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python transformer_context.py <context_window_size> <token_sequence>")
        sys.exit(1)

    try:
        context_window_size = int(sys.argv[1])
    except ValueError:
        print("Error: context_window_size must be an integer.")
        sys.exit(1)

    token_sequence = sys.argv[2]
    
    if not token_sequence.isalpha() or not token_sequence.isupper():
        print("Error: token_sequence must consist of uppercase English letters.")
        sys.exit(1)

    # Prepare the output file
    output_filename = 'attention_log.txt'
    if os.path.exists(output_filename):
        os.remove(output_filename) # Clear the file at the start of a new run

    # 3. Manage Context Window
    context_window_tokens = []
    context_window_embeddings = []

    for token in token_sequence:
        # If the window is full, remove the oldest token
        if len(context_window_tokens) == context_window_size:
            context_window_tokens.pop(0)
            context_window_embeddings.pop(0)

        # Add the new token
        context_window_tokens.append(token)
        context_window_embeddings.append(token_embeddings[token])

        # 4. Calculate Simplified Attention
        # The query is the embedding of the newly added token
        query = context_window_embeddings[-1]
        
        # The keys are all embeddings in the current context
        keys = np.array(context_window_embeddings)

        # Compute raw attention scores
        raw_scores = np.dot(keys, query)

        # Apply softmax to get final attention weights
        attention_weights = softmax(raw_scores)

        # 5. Output Results to File
        with open(output_filename, 'a') as f:
            f.write(f"--- Processing Token: {token} ---\n")
            f.write(f"Current Context Window (tokens): {context_window_tokens}\n")
            f.write(f"Attention of '{token}' to Context Tokens:\n")
            f.write(f"  Tokens: {context_window_tokens}\n")
            # Format weights for output
            formatted_weights = [f"{weight:.4f}" for weight in attention_weights]
            f.write(f"  Weights: {formatted_weights}\n")
            f.write("\n")

if __name__ == "__main__":
    main()
