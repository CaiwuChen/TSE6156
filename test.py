import matplotlib.pyplot as plt
import numpy as np

# Data
x_labels = ['10', '30', '50', '100']
walking_time = [0.5, 0.6, 1, 0.5]
success_rate = [0, 0.4, 1, 0]

# Plot
plt.figure(figsize=(6, 4))
plt.plot(x_labels, walking_time, marker='o', linestyle='-', label="Normalization Value")
plt.plot(x_labels, success_rate, marker='s', linestyle='--', label="Success Value")

# Labels and Title
plt.xlabel("Length of Historical Observations & Actions")
plt.ylabel("Value")

plt.legend()
plt.grid(True)

# Displaying the plot
plt.show()
