import unittest
import scatterplot
from scatterplot import scatter
import matplotlib.pyplot as plt

class TestScatterPlot(unittest.TestCase):

    def setUp(self):
        self.x = [1,2,3,4]
        self.y = [2,4,1,3] 

    def test_default_plot(self):
        plt.figure()
        scatter(self.x, self.y)
        # Assert plot looks correct
        
    def test_custom_colors(self): 
        colors = ['red', 'green', 'blue', 'black']
        scatter(self.x, self.y, c=colors)
        # Assert colors applied properly
        
    def test_sized_markers(self):
        sizes = [10, 20, 5, 30]
        scatter(self.x, self.y, s=sizes)
        # Assert sizes mapped properly

    def test_colormap(self):
        scatter(self.x, self.y, s=self.y, cmap='viridis')
        # Assert colormap used correctly

    # Other tests for alpha, other kwargs, bad inputs, etc.
        
if __name__ == '__main__':
    unittest.main()