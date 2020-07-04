import statistics
import numpy as np
import matplotlib.pyplot as plt

from soccer_stats.config import Config
from soccer_stats.stats import minute_sort_key


def _dynamic_x_label_size(labels):
    return (-2.0 / 29.0) * len(labels) + (472 / 29)


def goals_per_minute(counter, filename, title=None, labels=True, avg=True):
    labels, values = zip(*sorted(counter.items(), key=minute_sort_key))
    indexes = np.arange(len(labels))
    x_label_size = _dynamic_x_label_size(labels)
    rotation = 'vertical' if x_label_size < 12 else 'horizontal'
    plt.figure(figsize=(25, 15))
    plt.bar(indexes, values)
    plt.xticks(indexes, labels, rotation=rotation)
    plt.tick_params(axis='x', labelsize=x_label_size)
    plt.tick_params(axis='y', labelsize=16)
    plt.xlabel('Minute', labelpad=25, fontsize=22)
    plt.ylabel('Goals', labelpad=25, fontsize=22)
    if labels and x_label_size > 12:
        label_pad = max(values) * 0.02
        for index, value in zip(indexes, values):
            plt.text(
                x=index, y=value + label_pad, s=str(value),
                c='tab:blue', ha='center', fontsize=x_label_size)
    if avg:
        plt.axhline(statistics.mean(values), color='r', linestyle='dashed')
    if title is not None:
        plt.suptitle(title, fontsize=30)
    plt.savefig('{}{}.png'.format(Config.PLOT_PATH, filename))
    plt.close()


def goals_per_year(counter, filename, title=None, labels=True, avg=True):
    labels, values = zip(*sorted(counter.items()))
    indexes = np.arange(len(labels))
    x_label_size = _dynamic_x_label_size(labels)
    rotation = 'vertical' if x_label_size < 12 else 'horizontal'
    plt.figure(figsize=(25, 15))
    plt.bar(indexes, values)
    plt.xticks(indexes, labels, rotation=rotation)
    plt.tick_params(axis='x', labelsize=x_label_size)
    plt.tick_params(axis='y', labelsize=16)
    plt.xlabel('Year', labelpad=25, fontsize=22)
    plt.ylabel('Goals', labelpad=25, fontsize=22)
    if avg:
        plt.axhline(statistics.mean(values), color='r', linestyle='dashed')
    if title is not None:
        plt.suptitle(title, fontsize=30)
    plt.savefig('{}{}.png'.format(Config.PLOT_PATH, filename))
    plt.close()
