import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data_4.txt", sep=" ")
data = df.to_numpy()

plt.plot(data[:, 0], data[:, 1])
plt.show()

#python.exe .\plot.py 