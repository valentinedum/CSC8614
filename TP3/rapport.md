# Rapport TP3

## About the Report

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

## Puting it all together

### Question 1 
In the original model, each layer is a `Linear`. But with LoRA, they are replaced by `LinearWithLoRa` that contain the frozen original layer and a new layer LoRA (trainable).
The injection's worked correctly.

### Question 2
```
Parameter Count:
trainable params: 1,327,104 || all params: 164,364,288 || trainable%: 0.81%
```
With LoRA, training is just for a small part of the model (0.81%). 

## Spam Classification

### Question 3
After replacing the output head for classification, the number and fraction of trainable parameters increased slightly:
```
trainable params: 1,328,642 || all params: 125,768,450 || trainable%: 1.06
```
The increase in trainable parameters comes from the new classification head, which is unfrozen and added to the trainable set. The decrease in total parameters is because the new head is smaller than the original vocabulary projection layer (which had many more output units).

### Question 4
With `lr=5e-4` and `epochs=1`, 
During training, the loss decreases over the course of the epoch. So the model is correctly learning to classify the data. The final accuracy after one epoch is quite high (`94,21%`). 
This is reasonable given the binary nature of the spam classification task and the inbalanced dataset.  

### Question 5
The overall test accuracy after 1 epoch is `97.32%` which is very close to the train accuracy. It tells that the model is efficiently generalizing and that it does not overfit. This shows that the LoRA-adapted GPT model can quickly adapt to the classification problem with only a small fraction of trainable parameters.
