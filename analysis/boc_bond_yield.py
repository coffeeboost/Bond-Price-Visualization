# -*- coding: utf-8 -*-
"""boc bond yield.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12C97A0wmJnqQonix2nAYQl1R89xdT3gG
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Sample data or you can load your dataset using pandas
# Replace this with your actual dataset
data = df.read_csv('/content/data.csv')

# Normalize the data using MinMaxScaler
scaler = MinMaxScaler(feature_range=(-1, 1))
data['Value'] = scaler.fit_transform(data['Value'].values.reshape(-1, 1))

# Convert data to PyTorch tensor
data_tensor = torch.FloatTensor(data['Value'].values).view(-1, 1)

# Function to prepare data for the model
def prepare_data(data, seq_len):
    sequences = []
    for i in range(len(data) - seq_len):
        seq = data[i:i + seq_len]
        label = data[i + seq_len:i + seq_len + 1]
        sequences.append((seq, label))
    return sequences

# Define sequence length and split data into sequences
sequence_length = 10
sequences = prepare_data(data_tensor, sequence_length)

# Split data into train and test sets
train_size = int(len(sequences) * 0.7)
test_size = len(sequences) - train_size
train_data, test_data = sequences[:train_size], sequences[train_size:]

# Define RNN model
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.rnn(x, h0)
        out = self.fc(out[:, -1, :])
        return out

# Define LSTM model
class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

# Define GRU model
class GRU(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(GRU, self).__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.gru(x, h0)
        out = self.fc(out[:, -1, :])
        return out

# Define model parameters
input_size = 1
hidden_size = 64
output_size = 1

# Initialize models
rnn_model = RNN(input_size, hidden_size, output_size)
lstm_model = LSTM(input_size, hidden_size, output_size)
gru_model = GRU(input_size, hidden_size, output_size)

# Loss function and optimizer
criterion = nn.MSELoss()
rnn_optimizer = torch.optim.Adam(rnn_model.parameters(), lr=0.001)
lstm_optimizer = torch.optim.Adam(lstm_model.parameters(), lr=0.001)
gru_optimizer = torch.optim.Adam(gru_model.parameters(), lr=0.001)

# Training function for all models
def train_model(model, optimizer, criterion, train_data, epochs=10):
    model.train()
    for epoch in range(epochs):
        for seq, labels in train_data:
            optimizer.zero_grad()
            output = model(seq.unsqueeze(0))
            loss = criterion(output, labels)
            loss.backward()
            optimizer.step()
        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

# Train RNN model
train_model(rnn_model, rnn_optimizer, criterion, train_data)
# print('finish RNN')

# Train LSTM model
train_model(lstm_model, lstm_optimizer, criterion, train_data)
# print('finish LSTM')

# Train GRU model
train_model(gru_model, gru_optimizer, criterion, train_data)
# print('finish GRU')

# Define file paths for saving the models
rnn_model_path = 'rnn_model.pth'
lstm_model_path = 'lstm_model.pth'
gru_model_path = 'gru_model.pth'

# # Save RNN model
# torch.save(rnn_model.state_dict(), rnn_model_path)

# # Save LSTM model
# torch.save(lstm_model.state_dict(), lstm_model_path)

# # Save GRU model
# torch.save(gru_model.state_dict(), gru_model_path)


# # Loading the saved models
# loaded_rnn_model = RNN(input_size, hidden_size, output_size)
# loaded_rnn_model.load_state_dict(torch.load(rnn_model_path))

# loaded_lstm_model = LSTM(input_size, hidden_size, output_size)
# loaded_lstm_model.load_state_dict(torch.load(lstm_model_path))

# loaded_gru_model = GRU(input_size, hidden_size, output_size)
# loaded_gru_model.load_state_dict(torch.load(gru_model_path))

# Prediction function for all models
def predict(model, data):
    model.eval()
    with torch.no_grad():
        predicted = []
        for seq, _ in data:
            output = model(seq.unsqueeze(0))
            predicted.append(output.item())
    return predicted

# Make predictions on test data
rnn_predictions = predict(rnn_model, test_data)
lstm_predictions = predict(lstm_model, test_data)
gru_predictions = predict(gru_model, test_data)

# Convert predictions back to original scale using inverse_transform
rnn_predictions = scaler.inverse_transform(np.array(rnn_predictions).reshape(-1, 1))
lstm_predictions = scaler.inverse_transform(np.array(lstm_predictions).reshape(-1, 1))
gru_predictions = scaler.inverse_transform(np.array(gru_predictions).reshape(-1, 1))

# Printing the predictions
# print("RNN Predictions:")
# print(rnn_predictions)

# print("\nLSTM Predictions:")
# print(lstm_predictions)

# print("\nGRU Predictions:")
# print(gru_predictions)