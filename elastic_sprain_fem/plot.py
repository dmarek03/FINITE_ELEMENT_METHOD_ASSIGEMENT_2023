import matplotlib.pyplot as plt
from numpy import ndarray, dtype


def show(x: ndarray[float, dtype[float]], y: ndarray[float, dtype[float]], n: int) -> None:
    plt.style.use('ggplot')
    ax = plt.subplot()
    ax.set(title='elastic sprain FEM', xlabel='n = ' + str(n))
    # Przesuwamy y o 3 w górę, gdyż tak wynika z warunku Dirichleta  " u(2) = 3 "
    ax.plot(x, y+3, color='purple')
    plt.show()
