import pickle

from sklearn.linear_model import LogisticRegression

# Exemplo de treinamento de um modelo simples
model = LogisticRegression()
X = [[0, 0], [1, 1]]
y = [0, 1]
model.fit(X, y)

# Salvando o modelo em um arquivo .pkl
with open('/tmp/model.pkl', 'wb') as f:
    pickle.dump(model, f)
