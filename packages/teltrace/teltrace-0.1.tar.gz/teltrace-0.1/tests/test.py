from teltrace.load import file_read
import matplotlib.pyplot as plt

filepath = "/Users/bensappey/Downloads/Source_file_METEC_04NOV_2021_methane_background.csv"

spectrum = file_read(filepath=filepath)
print(spectrum)

# plt.plot()
# plt.show()