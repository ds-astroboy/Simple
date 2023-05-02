# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense


 # Load weather data
data = pd.read_csv('weather_data.csv')
 # Split data into training and testing sets
train_size = int(len(data) * 0.7)
train_data = data.iloc[:train_size, :]
test_data = data.iloc[train_size:, :]
 # Create input and output sequences for LSTM model


def create_sequences(data, seq_length):
    x = []
    y = []
    for i in range(len(data)-seq_length-1):
        input_seq = data.iloc[i:i+seq_length, 0].values
        output_seq = data.iloc[i+seq_length, 0]
        x.append(input_seq)
        y.append(output_seq)
    return np.array(x), np.array(y)


seq_length = 5
x_train, y_train = create_sequences(train_data, seq_length)
x_test, y_test = create_sequences(test_data, seq_length)
 # Reshape data for LSTM input
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
 # Build LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(seq_length, 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))
 # Compile model
model.compile(optimizer='adam', loss='mean_squared_error')
 # Train model
model.fit(x_train, y_train, epochs=50, batch_size=32)
 # Evaluate model
train_loss = model.evaluate(x_train, y_train, verbose=0)
test_loss = model.evaluate(x_test, y_test, verbose=0)
print(f'Training Loss: {train_loss:.4f} \nTesting Loss: {test_loss:.4f}')
 # Make predictions
train_predictions = model.predict(x_train)
test_predictions = model.predict(x_test)
 # Plot results
plt.figure(figsize=(10, 6))
plt.plot(train_data.index[seq_length+1:], y_train, label='Actual')
plt.plot(train_data.index[seq_length+1:], train_predictions, label='Predicted')
plt.plot(test_data.index[seq_length+1:], y_test, label='Actual')
plt.plot(test_data.index[seq_length+1:], test_predictions, label='Predicted')
plt.legend()
plt.show()