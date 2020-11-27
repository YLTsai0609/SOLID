import os
import pickle
from typing import Tuple
import matplotlib.pyplot as plt
from matplotlib.axes._subplots import Axes
import re
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def _get_exp_and_histories(exp_keys: list) -> dict:
    """
    根據輸入的實驗名稱，透過`get_histories`函數拿取相應的fold.pkl
    Args:
        exp_keys (list): 輸入的實驗名稱list

    Returns:
        dict : 輸出的實驗名稱 & fold_1.pkl, fold_2.pkl, fold_3.pkl pair
    """
    exp_collection = {}
    for k in exp_keys:
        exp_collection[k] = _get_histories(k)
    return exp_collection


def _get_histories(exp_name: str) -> dict:
    """
    根據輸入的實驗名稱拿取對應的history
    Args:
        exp_name (str): 輸入的實驗名稱

    Returns:
        dict : 輸出的實驗名稱 & fold_1.pkl, fold_2.pkl, fold_3.pkl pair
    """
    exp_histroy_pair = {}
    for n in range(1, 4):
        fold_path = os.path.join('experiments', exp_name, f'fold_{n}.pkl')
        with open(fold_path, 'rb') as save_history:
            exp_histroy_pair[f'fold_{n}'] = pickle.load(save_history)
    return exp_histroy_pair


def plot_history(history: dict,
                 lbl: str,
                 ax1: Axes,
                 ax2: Axes,
                 color: str) -> Tuple[Axes, Axes]:
    """
    根據給定的history畫圖，左為loss vs epoch，右為accuracy vs epoch
    Args:
        history (dict): keras中的history dict
        lbl (str): 該history對應的legend
        ax1 (Axes) 物件，畫線圖 (loss vs epoch)
        ax2 (Axes) 物件，畫線圖 (accuracy vs epoch)
        color (str) : 該history對應的顏色


    Returns:
        Tuple[Axes, Axes] : 畫好線的Axes物件 

    """
    acc_keyword = ['acc', 'accuracy']
    val_acc_keyword = ['val_acc', 'val_accuracy']
    ax1.plot(history['loss'],
             label=f'{lbl}_train', c=color)
    ax1.plot(history['val_loss'], label=f'{lbl}_val',
             c=color, linestyle='--')
    ax1.set_ylabel('Loss')
    ax1.set_xlabel('Epoch')
    ######### [START] for differenct keras version acc keywords #############
    try:
        # 'acc' for keras 2.1.6
        ax2.plot(history[acc_keyword[0]],
                 label=f'{lbl}_train', c=color)
        ax2.plot(history[val_acc_keyword[0]], label=f'{lbl}_val',
                 c=color, linestyle='--')
    except KeyError:
        # 'accuracy' for keras > 2.1.6
        ax2.plot(history[acc_keyword[1]],
                 label=f'{lbl}_train', c=color)
        ax2.plot(history[val_acc_keyword[1]], label=f'{lbl}_val',
                 c=color, linestyle='--')
    ######### [END] for differenct keras version acc keywords #############
    ax2.set_ylabel('accuracy')
    ax2.set_xlabel('Epoch')
    return ax1, ax2


def _extract_label_keyword_func(exp_name: str, extract_pattern: re.Pattern) -> str:
    """
    Args:
        exp_name (str): 輸入的實驗名稱
        extract_pattern(re.Pattern) : 擷取標籤的正則表達式
    Returns:
        str: 輸出的histroy plot label
    """
    return extract_pattern.search(exp_name).group()


def main(pattern_to_extract_label: re.Pattern):
    display_exp = sorted(os.listdir('experiments'))
    exp_s = "\n".join(display_exp)
    print(f'all experiments are : {exp_s}')

    exp_keys = []
    keep_asking = True
    while keep_asking:
        exp_name = input("enter experiments names, if end, key [end]")
        if exp_name == 'end':
            keep_asking = False
        else:
            exp_keys.append(exp_name)

    print(exp_keys)

    exp_collections = _get_exp_and_histories(exp_keys=exp_keys)
    colors = 'bgrcmykw'[:len(exp_collections.keys())]

    with plt.style.context(['science', 'grid', 'no-latex']):
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(3, 4), dpi=150)
        for color_i, (exp_name, all_fold_d) in enumerate(exp_collections.items()):
            color = colors[color_i]
            for fold_i, history in all_fold_d.items():
                if fold_i == 'fold_1':
                    row = 0
                elif fold_i == 'fold_2':
                    row = 1
                elif fold_i == 'fold_3':
                    row = 2
                else:
                    raise ValueError('should be 3 fold in this experiments')
                short_exp_name = _extract_label_keyword_func(exp_name,
                                                             pattern_to_extract_label)
                axes[row][0], axes[row][1] = plot_history(history=history,
                                                          ax1=axes[row][0], ax2=axes[row][1],
                                                          lbl=short_exp_name,
                                                          color=color)

        handles, labels = axes[0][0].get_legend_handles_labels()
        fig.legend(handles, labels,
                   loc='upper center',
                   ncol=len(exp_collections.keys()),
                   shadow=True
                   )
        fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=0.5)
        fig.subplots_adjust(top=0.85)
        plt.show()


if __name__ == "__main__":
    pattern_to_extract_label = re.compile(r'dataset_1_(aug_[0-9]+)')
    main(pattern_to_extract_label)
