import matplotlib.pyplot as plt

def plot_list(lst, title, save_fig=False):
    plt.clf()
    for path in self.__paths:
        plt.plot(path)
    plt.ylabel("Price (Bells)")
    plt.xticks([n * 2 for n in range(7)], DAYS)
    plt.title(f"Turnip Price Paths over {len(self.__paths):,} Weeks")
    if save_fig:
        fileName = f"paths_{len(self.__paths)}.png"        
        output_dir = os.path.join(os.getcwd(), "output")
        if not os.path.exists(output_dir): os.mkdir(output_dir)
        path = os.path.join(output_dir, fileName)
        plt.savefig(path, bbox_inches="tight")
        print(f"Plot saved to {path}")
    else:
        plt.show()
