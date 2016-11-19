import os
from matplotlib.patches import Patch
from matplotlib import pyplot as plt

with open(os.getcwd() + '/scores.txt', 'r') as f:
    lines = f.readlines()

title = lines[0]
lines = lines[1:]
parsed = map(lambda s: s.split('Model Accuracy: '), lines)
iterations = map(lambda pieces: int(pieces[0]), parsed)
training = map(lambda pieces: float(pieces[1][:5]), parsed)
test = map(lambda pieces: float(pieces[2][:5]), parsed)

plt.title(title)
plt.xlabel('Iteration')
plt.ylabel('Accuracy (%)')

training_patch = Patch(color='red', label='Training')
test_patch = Patch(color='blue', label='Test')
plt.legend(handles=[training_patch, test_patch], loc=3)

plt.plot(iterations, training, 'r-', iterations, test, 'b-')

plt.show()
