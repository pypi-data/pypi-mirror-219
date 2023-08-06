import numpy as np
import threading

def train(model, data_input, data_output, **options):
    batch_size, epoch_number, learning_rate = options.get("batch_size"), options.get("epoch_number"), options.get("rate")
    for epoch in range(epoch_number):
        t_loss = 0
        for batch_start in range(0, len(data_input), batch_size):
            batch_end =  min(batch_start + batch_size,len(data_input))
            t_loss += model.computeBatch(data_input[batch_start:batch_end], data_output[batch_start:batch_end], batch_end-batch_start, learning_rate)
        print("Epoch = " + str(epoch) + " Loss = " + str(t_loss/len(data_input)), end='\r')
    model.save()
    print("\nTraining finished, model saved.")

class neuralNetwork:
    def __init__(self, **options):
        if options.get("load"):
            self.load(options.get("load"))
        else:
            if options.get("name") == None: self.name = "unknown"
            else: self.name = options.get("name")
            self.layers = options.get("layers")
            self.initializeWeightsAndBiases()

    def run(self, input):
        layers_output_space = np.empty(len(self.layers), dtype=object)
        layers_output_space[0] = input
        return self._run(layers_output_space)[-1]

    def _run(self, layer_history):
        for layer in range(1,len(self.layers)):
            layer_history[layer] = np.add(np.dot(self.weights[layer], layer_history[layer-1]), self.biases[layer])
            match self.layers[layer][1]:
                case "sigmoid": layer_history[layer] = 1 / (1 + np.exp(-layer_history[layer]))
                case "relu": layer_history[layer] = np.maximum(0, layer_history[layer])
                case "leakyRelu": layer_history[layer] = np.maximum(0.1 * layer_history[layer], layer_history[layer])
        return layer_history

    def _pass(self,  batch_input, batch_output):
        layer_number = len(self.layers)
        layers_output_space = np.empty(layer_number, dtype=object)
        layers_output_space[0] = batch_input
        layers_output_space = self._run(layers_output_space)
        error = np.subtract(layers_output_space[-1], batch_output)
        for layer in range(layer_number - 1, 0, -1):
            match self.layers[layer][1]:
                case "sigmoid": delta = np.multiply(error, layers_output_space[layer] * (1 - layers_output_space[layer]))
                case "relu": delta = np.multiply(error, np.where(layers_output_space[layer] > 0, 1, 0))
                case "leakyRelu": delta = np.multiply(error, np.where(layers_output_space[layer] > 0, 1, 0.1))
            with threading.Lock():
                self.weights_mod[layer] += np.outer(delta, layers_output_space[layer - 1])
                self.biases_mod[layer] += delta
            if layer>1: error = np.dot(self.weights[layer].T, delta)
        with threading.Lock():
            self.loss += abs(np.mean(layers_output_space[-1] - batch_output))

    def computeBatch(self, batch_input, batch_output, batch_size, learning_rate):
        self.weights_mod, self.biases_mod, self.loss = np.zeros_like(self.weights), np.zeros_like(self.biases), 0
        threads = []
        for i in range(batch_size):
            thread = threading.Thread(target=self._pass, args=(batch_input[i], batch_output[i]))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        factor = 1/batch_size*learning_rate
        self.weights -= np.multiply(self.weights_mod, factor)
        self.biases -= np.multiply(self.biases_mod, factor)
        return self.loss

    def initializeWeightsAndBiases(self):
        self.weights, self.biases = np.zeros(len(self.layers), dtype=object), np.zeros(len(self.layers), dtype=object)
        for i in range(1, len(self.layers)):
            match self.layers[i][1]:
                case "sigmoid": self.weights[i] = np.random.uniform(low=-0.1, high=0.1, size=(self.layers[i][0], self.layers[i-1][0]))
                case "relu": self.weights[i] = np.random.normal(loc=0, scale=np.sqrt(2 / self.layers[i-1][0]), size=(self.layers[i][0], self.layers[i-1][0]))
                case "leakyRelu": self.weights[i] = np.random.normal(loc=0, scale=np.sqrt(2 / self.layers[i-1][0]), size=(self.layers[i][0], self.layers[i-1][0]))*np.where(self.weights[i] > 0, 1, 0.1)
            self.biases[i] = np.zeros(self.layers[i][0], dtype=np.float32)

    def save(self):
        np.savez(self.name + ".npz", matrix1=self.weights, matrix2=self.biases, matrix3=self.layers)

    def load(self, filename):
        data = np.load(filename + ".npz", allow_pickle=True)
        self.weights, self.biases, self.layers, self.name = data['matrix1'], data['matrix2'], data['matrix3'], filename
