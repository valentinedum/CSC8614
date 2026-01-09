# Rapport TP2

## About the Report

### Question 1

_DUMANGE Valentine_

**Installation de l'environnement** :
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Versions** :
- Python : 3.12.11
- OS : Linux (WSL2)
- torch==2.9.1, tiktoken==0.12.0, tqdm==4.67.1, pandas==2.3.3, matplotlib==3.10.8, tensorflow==2.20.0, jupyterlab==4.5.1

---

## Preparing the model

We download the GPT-2 model.
We obtain 2 different things : `settings` and `params`

---

### Question 2
Settings is a dictionnary that contains 5 different keys including:
- tokens in the vocab `n_vocab`: 50257
- maximum context tokens `n_ctx`: 1024
- dimensions for embeddings `n_embd`: 768
- attention heads `n_head`: 12
- transformer layers `n_layer`: 12

### Question 3
Params is an other dictionnary containing 5 keys too :
- weights for each transformer `layerblocks`: type=list
- bias `b`: type=ndarray, shape=(768,)
- gain`g`: type=ndarray, shape=(768,)
- position embeddings `wpe`: type=ndarray, shape=(1024, 768)
- token embeddings `wte`: type=ndarray, shape=(50257, 768)

### Question 4
The cfg parameter needs :
- vocab_size (from settings: n_vocab)
- emb_dim (from settings: n_embd)
- context_length (from settings: n_ctx)
- drop_rate (already provided: 0.1)
- n_layers (from settings: n_layer)
- n_heads (from settings: n_head)
- qkv_bias (already provided: True)

Now we load our GPT-2 model with these configs.

---

## Preparing the data

### Question 5.1
The line `df = df.sample(frac=1, random_state=123)` shuffles the dataset randomly before splitting into train/test sets. `frac=1` means that we take 100% of the data. `random_state=123` ensures reproducibility - the same shuffle every time we run the code
> This prevents bias from the original data ordering.

### Question 5.2
Analysis of class distribution in the training set:

```
Class distribution in training set:
Label
ham     3860
spam     597
Name: count, dtype: int64
```
This dataset is very unbalanced. There are about 6.5 times more **ham** messages than **spam** messages. The model may be biased toward predicting "ham" leading to poor perfomances.

### Question 6
Now, we can create our dataloaders

### Question 7
With a batch_size of 16 and 4457 samples, we will have 279 batches per epoch.
If we reduce the dataset to 2000 sample, we'll have approximately 125 batches per epoch.

---

## Fine-tuning

We will fine-tune gpt-2 in order to predict binary classes.

### Question 8
We add code lines in order to change the output head of the model :
In this code, we are freezing the internal layers with `param.requires_grad = False` in order to preserve the pre-trained model and only train the new parameters that are specific to the classification task.

```
Original output head: Linear(in_features=768, out_features=50257, bias=False)
New output head: Linear(in_features=768, out_features=2, bias=True)
```

### Question 9
Now we create the training loop. Everything is lauched on my gpu.

### Question 10
Looking at the results of the training phase, loss decreases from 1.9-2.3 to 0.6-0.7 in epoch 1. Then in epoch 2 and 3, it stabilizes around 0.6-0.7
Overall accuracy decreased (87% → 81%) from epoch 1 to 3 but spam detection increased massively (0% → 90%!). The model is learning ! It now detects spam instead of always predicting "ham".

