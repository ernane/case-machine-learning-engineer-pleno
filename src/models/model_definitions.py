class DummyModel:
    def predict(self, X):
        return [len(x) for x in X]
