import os
from collections import defaultdict
import networkx as nx

def read_conllu_file(filepath):
    """
    Generator: yields (sent_id, raw_lines, sentence_tokens, had_invalid_head)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_lines = []
        sentence = []
        had_invalid = False
        sent_id = None
        for line in f:
            line = line.rstrip('\n')
            raw_lines.append(line)

            if line.startswith('# sent_id'):
                sent_id = line.split('=')[-1].strip()

            if not line:
                if sentence:
                    yield sent_id, raw_lines, sentence, had_invalid
                    sentence = []
                    raw_lines = []
                    had_invalid = False
                    sent_id = None
                continue

            if line.startswith('#'):
                continue

            parts = line.split('\t')
            if len(parts) < 7 or '-' in parts[0] or '.' in parts[0]:
                continue  # skip multiword or empty nodes

            try:
                token_id = int(parts[0])
                head = int(parts[6])
                sentence.append({
                    'id': token_id,
                    'form': parts[1],
                    'head': head
                })
            except ValueError:
                had_invalid = True

        if sentence:
            yield sent_id, raw_lines, sentence, had_invalid

def has_cycle_or_bad_head(sentence):
    """
    Returns True if:
    - There is a cycle (including ROOT)
    - A token's HEAD points to a nonexistent ID
    """
    G = nx.DiGraph()
    token_ids = set(token['id'] for token in sentence)
    token_ids.add(0)  # Treat ROOT (0) as valid node

    for token in sentence:
        head = token['head']
        if head not in token_ids:
            return True  # HEAD points to a nonexistent node
        G.add_edge(head, token['id'])

    return nx.is_directed_acyclic_graph(G) == False

def analyze_file(filepath):
    count_valid = 0
    count_invalid_head = 0
    count_with_cycles = 0

    invalid_head_lines = []
    cycle_lines = []

    for sent_id, raw_lines, sentence, had_invalid in read_conllu_file(filepath):
        if had_invalid:
            count_invalid_head += 1
            invalid_head_lines.extend(raw_lines)
            invalid_head_lines.append("")  # blank line between sentences
            continue

        if has_cycle_or_bad_head(sentence):
            count_with_cycles += 1
            cycle_lines.extend(raw_lines)
            cycle_lines.append("")
        else:
            count_valid += 1

    # Save to files
    # split filepath on . and get second to last part
    base_name = filepath.split(".")[-2]
    with open(f"{base_name}_invalid_heads.conllu", "w", encoding="utf-8") as f:
        f.write("\n".join(invalid_head_lines).strip() + "\n")

    with open(f"{base_name}_dependency_cycles.conllu", "w", encoding="utf-8") as f:
        f.write("\n".join(cycle_lines).strip() + "\n")

    # Print summary
    print("\nSummary for file:", filepath)
    print(f"✅ Valid sentences (no cycles, no invalid heads): {count_valid}")
    print(f"⚠️  Sentences with invalid HEADs: {count_invalid_head}")
    print(f"🔁 Sentences with dependency cycles: {count_with_cycles}")
    print(f"📝 Saved invalid sentences to '{base_name}_invalid_heads.conllu' and '{base_name}_dependency_cycles.conllu'.")

if __name__ == "__main__":
    conllu_paths = ["corpus/conllu/train.conllu", "corpus/conllu/dev.conllu", "corpus/conllu/test.conllu"]
    for conllu_path in conllu_paths:
        if os.path.exists(conllu_path):
            analyze_file(conllu_path)
        else:
            print(f"File not found: {conllu_path}")
