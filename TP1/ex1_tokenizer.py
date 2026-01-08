from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
phrase = "Artificial intelligence is metamorphosing the world!"
phrase2 =  "GPT models use BPE tokenization to process unusual words like antidisestablishmentarianism." 

# TODO: tokeniser la phrase
tokens = tokenizer.tokenize(phrase)
tokens2 = tokenizer.tokenize(phrase2)

print(tokens)
print(tokens2)

# TODO: obtenir les IDs
token_ids = tokenizer.encode(phrase)
print("Token IDs:", token_ids)

print("Détails par token:")
for tid in token_ids:
    # TODO: décoder un seul token id
    txt = tokenizer.decode([tid])
    print(tid, repr(txt))

### ------------------------------------------------

# TODO: extraire uniquement les tokens correspondant au mot long (optionnel mais recommandé)
long_word = "antidisestablishmentarianism"
long_word_tokens = tokenizer.tokenize(long_word)
print(f"\nTokens pour '{long_word}':", long_word_tokens)

# TODO: compter le nombre de sous-tokens pour le tokens 2
print(f"Nombre de sous-tokens: {len(long_word_tokens)}")
