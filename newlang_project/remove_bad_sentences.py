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

def remove_bad_sentences(filepath):
    valid_lines = []
    count_total = 0
    count_removed = 0

    for _, raw_lines, sentence, had_invalid in read_conllu_file(filepath):
        count_total += 1
        if had_invalid or has_cycle_or_bad_head(sentence):
            count_removed += 1
            continue
        valid_lines.extend(raw_lines)
        valid_lines.append("")  # blank line between sentences

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(valid_lines).strip() + "\n")

    print(f"✔️ Cleaned {filepath}:")
    print(f"   Original sentences: {count_total}")
    print(f"   Removed bad sentences: {count_removed}")
    print(f"   Remaining valid sentences: {count_total - count_removed}\n")

if __name__ == "__main__":
    conllu_paths = ["corpus/conllu/train.conllu", "corpus/conllu/dev.conllu", "corpus/conllu/test.conllu"]
    for path in conllu_paths:
        if os.path.exists(path):
            remove_bad_sentences(path)
        else:
            print(f"❌ File not found: {path}")
