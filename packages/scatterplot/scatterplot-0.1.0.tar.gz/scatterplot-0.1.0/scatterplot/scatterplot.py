import matplotlib.pyplot as plt

def scatter(x, y, s=20, c=None, alpha=1.0, cmap=None, **kwargs):
    """
    Custom scatter plot with default reasonable styling.

    Args:
        x (array-like): x data
        y (array-like): y data
        s (array-like or int): marker size
        c (array-like or str): marker color
        alpha (float): transparency
        cmap: matplotlib colormap for coloring markers
        **kwargs: other matplotlib scatter plot kwargs

    Returns:
        matplotib.axes.Axes: The plot
    """

    # Default styling
    if 'edgecolors' not in kwargs:
        kwargs['edgecolors'] = 'none'

    if c is None:
        c = '#333333'
        
    # Create plot
    ax = plt.gca() 
    sc = ax.scatter(x, y, s=s, c=c, alpha=alpha, cmap=cmap, **kwargs)

    return sc

def example_usage():
    # Simple case
    x = [1, 2, 3, 4]
    y = [2, 1, 4, 3]

    fig, ax = plt.subplots()
    scatter(x, y)

    # Custom colors
    c = ['r', 'g', 'b', 'k']
    scatter(x, y, c=c)

    # Sized by y-value
    s = [20, 10, 25, 15] 
    scatter(x, y, s=s)

    # Colormap from y-value
    scatter(x, y, s=y, cmap='viridis')

    plt.show()

if __name__ == '__main__':
    example_usage()