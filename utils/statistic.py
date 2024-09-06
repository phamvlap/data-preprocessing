import matplotlib.pyplot as plt
from tokenizers import Tokenizer
from pandas import Series

from .mix import make_dir


def plot_hist_graph(
    data: list[int],
    title: str,
    x_label: str,
    y_label: str,
    fig_path: str = None,
    bins: int = 20,
) -> None:
    plt.hist(data, bins=bins)
    plt.grid(True)
    plt.title(title)
    plt.x_label(x_label)
    plt.y_label(y_label)

    if fig_path is not None:
        dir_path = fig_path.rsplit("/", 1)[0]
        make_dir(dir_path)
        plt.savefig(fig_path)

    plt.show()
    plt.close()


def get_tokens_length(tokenizer: Tokenizer, data: Series | list[str]) -> list[int]:
    return [len(tokenizer.encode(x).ids) for x in data]
