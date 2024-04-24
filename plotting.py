import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

# Sample data (arrays)
file_numbers = ['file1', 'file2', 'file3', 'file4', 'file5', 'file6', 'file7', 'file8', 'file9', 'file10', 'file11', 'file12', 'file13', 'file14', 'file15', 'file16', 'file17', 
'file18', 'file19', 'file20', 'file21', 'file22', 'file23', 'file24', 'file25', 'file26', 'file27', 'file28', 'file29', 'file30']  # File numbers
time_algo1 = [58.33, 50.0, 90.91, 50.0, 50.0, 50.0, 62.5, 28.89, 44.44, 57.78, 50.0, 14.29, 10.0, 66.67, 16.67, 53.33, 80.0, 66.67, 50.0, 44.44, 75.0, 57.14, 64.71, 71.43, 66.67, 33.33, 54.0, 62.0, 66.67, 23.0]  # Time taken for Algorithm 1
time_algo2 = [76.19, 54.76, 92.86, 60.71, 20.69, 86.21, 64.1, 54.76, 83.33, 70.45, 51.02, 79.59, 84.13, 73.02, 92.06, 63.22, 69.77, 89.66, 73.33, 26.67, 87.0, 88.0, 56.0, 92.0, 56.9, 67.24, 70.69, 80.23, 76.34, 84.27]   # Time taken for Algorithm 2

# Plotting the data
plt.plot(file_numbers, time_algo1, label='SIFT_FLANN', marker='o')  # Plot Algorithm 1
plt.plot(file_numbers, time_algo2, label='Euclidean distance', marker='s')  # Plot Algorithm 2

# Adding labels and title
plt.xlabel('File Number')          # Label for x-axis
plt.ylabel('Accuracy (%)') # Label for y-axis
plt.title('Comparison of Accuracy between Algorithms')  # Plot title
plt.xticks(rotation=90) 
# Adding legend
plt.legend()

# Display the plot
plt.show()
