import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, HTML

groups = 7
heuristic_agent_values = []
id_improved_values = []
labels = ('Random', 'MM_Null', 'MM_Open', 'MM_Improved', 'AB_Null', 'AB_Open', 'AB_Improved')

index = np.arange(groups)
bar_width = 0.35

def plot_graphs_tables(id_improved_values, versus_values, heuristic_values, versus_values_h, label):
    data = {'ID_Imrpoved Agent Wins (Out of 20)': id_improved_values, 'Heuristic Agent Wins (Out of 20)': heursitic_values}
    df = pd.DataFrame(data)
    display(df)
    id_improved_values = id_improved_values
    versus_values = versus_values
    plt.bar(index, id_improved_values, bar_width,
                     color='b',
                     label='ID_Improved Agent')

    plt.bar(index + bar_width, versus_values, bar_width,
                     color='r')

    plt.xlabel('Agents')
    plt.ylabel('Wins')
    plt.title('ID_Improved Agent Vs Other Agents')
    plt.xticks(index + bar_width / 2, labels)
    plt.rcParams["figure.figsize"] = [20, 5]
    plt.legend()
    plt.show()

    heursitic_values = heursitic_values
    versus_values = versus_values_h

    plt.bar(index, heursitic_values, bar_width,
                     color='b',
                     label='ID_Improved Agent')

    plt.bar(index + bar_width, versus_values, bar_width,
                     color='r')

    plt.xlabel('Agents')
    plt.ylabel('Wins')
    plt.title(label)
    plt.xticks(index + bar_width / 2, labels)
    plt.legend()
    plt.rcParams["figure.figsize"] = [20, 5]
    plt.show()