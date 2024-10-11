class DummyModel:
    @staticmethod
    def predict(X):
        return [len(x) for x in X]
