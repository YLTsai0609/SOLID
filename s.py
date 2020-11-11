'''
特徵與目標的相關性分析，以house_price為例
將各個特徵與目標的相關係數畫出，排序後，並以bar plot表示
希望以後可以重複利用這些函數
'''

import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple
import numpy as np


def colormap2rgb(num_colors: int,
                 colormap: str = 'rainbow') -> Tuple[np.ndarray, np.ndarray]:
    """
    從colormap中拿到rgba以及rgb

    Args:
        num_colors (int): 需要的顏色數量
        colormap (str): 使用的colormap關鍵字, default to rainbow

    Returns:
        Tuple[np.ndarray, np.ndarray]: rgba以及rgb

    Examples:
        1. 
            rgba_list, rgb_list = colormap2rgb(num_colors=3, colormap='Paired')
            for line_idx in range(len(rgba_list)):
                plt.plot([i for i in range(10)],
                        [i * line_idx for i in range(10)],
                        c=rgba_list[line_idx], label=f'line {line_idx}')
                plt.legend()
            plt.show()
            print(rgba_list)
    """
    func = getattr(plt.cm, colormap)
    rgba_color = func(np.linspace(0, 1, num_colors))
    rgb_color = (rgba_color[:, 0:3] * 255).astype(int)
    return rgba_color, rgb_color


# +
def plot_feature_corr_sorting(df: pd.DataFrame, target: str,
                              verbose: bool = False,
                              fig_title: str = 'Correlations with Target') -> None:
    """
    輸入dataframe，畫出對各個數值特徵對目標的相關係數

    Args:
        df (pd.DataFrame): 整個需要分析的dataframe
        target (str): 目標變數
        verbose(bool) : 是否需要顯示各個變數對目標變數的相關係數 Default to False
        fig_title(str) : 畫圖標題

    Returns:
        None

    """
    import operator

    individual_features_df = []
    num_cols = [var for var in df.columns if df[var].dtypes != 'O']
    df_num = df[num_cols]
    for i in range(0, len(df_num.columns) - 1):
        tmp_df = df_num[[df_num.columns[i], target]]
        tmp_df = tmp_df[tmp_df[df_num.columns[i]] != 0]
        individual_features_df.append(tmp_df)

    all_correlations = {feature.columns[0]: feature.corr(
    )[target][0] for feature in individual_features_df}
    all_correlations = sorted(all_correlations.items(),
                              key=operator.itemgetter(1))
    if verbose:
        for (key, value) in all_correlations:
            print("{:>15}: {:>15}".format(key, value))
    df_corr = pd.DataFrame(all_correlations, columns=[
                           'features', 'corr_with_targets'])

    rgba_list, _ = colormap2rgb(num_colors=df_corr.shape[0])
    with plt.style.context(['science', 'grid', 'no-latex']):
        fig, ax = plt.subplots(figsize=(3, 4), dpi=200)
        ax.barh(df_corr['features'],
                df_corr['corr_with_targets'],
                color=rgba_list)
        plt.xlabel('features')
        plt.title(fig_title)
        plt.tight_layout()
        plt.show()


def main():
    df = pd.read_csv('data/house_price.csv')
    plot_feature_corr_sorting(df=df, target='SalePrice')


if __name__ == "__main__":
    main()
