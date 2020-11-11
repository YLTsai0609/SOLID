'''
特徵與目標的相關性分析，以house_price為例
將各個特徵與目標的相關係數畫出，排序後，並以bar plot表示
希望以後可以重複利用這些函數

-----------------------------------
SRP 單一職責原則，將plot_feature_corr_sorting這隻函數拆小
並以時常更動地方進行拆分
1. 要計算相關係數的特徵欄位可能會經常過濾 - filter_col
2. 畫圖可能會經常修改畫圖參數，例如xy座標，標題等 - plot_barh
plot_feature_corr_sorting 修改為calculate_correlation

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


def filter_col(df: pd.DataFrame, dtype: str = 'number') -> pd.DataFrame:
    """
    從整個dataframe中過濾出特定欄位
    本函數會選出欄位資料型態不是object的欄位

    Args : 
        df (pd.DataFrame): 整個需要分析的dataframe
    Returns : 
        df (pd.DataFrame): 經過過濾的dataframe
    """
    if dtype == 'number':
        cols = [var for var in df.columns if df[var].dtypes != 'O']
    else:
        raise NotImplementedError(f'尚未實作該過濾機制，你目前輸入的dype為 {dtype}')
    return df[cols]


def plot_barh(df: pd.DataFrame,
              y='corr_with_targets',
              x='features',
              fig_title='Correlations with Target') -> None:
    """
    畫出Barh

    Args:
        df (pd.DataFrame): 要畫的圖
        y (str): y軸座標字串
        x (str): x軸座標字串
        fig_title(str) : 畫圖標題

    Returns:
        None

    """
    rgba_list, _ = colormap2rgb(num_colors=df.shape[0])
    with plt.style.context(['science', 'grid', 'no-latex']):
        fig, ax = plt.subplots(figsize=(3, 4), dpi=200)
        ax.barh(df[x], df[y], color=rgba_list)
        plt.xlabel(y)
        plt.title(fig_title)
        plt.tight_layout()
        plt.show()


def caculate_correlation(df: pd.DataFrame, target: str,
                         verbose: bool = False) -> pd.DataFrame:
    """
    給定一個dataframe，計算所有欄位對於目標變數的相關係數

    Args:
        df (pd.DataFrame): 需要計算相關係數的dataframe
        target (str): 目標變數
        verbose(bool) : 是否需要顯示各個變數對目標變數的相關係數 Default to False

    Returns:
        df (pd.DataFrame): 計算完成的dataframe，內含兩個欄位 : 'features', 'corr_with_targets'

    """
    import operator

    individual_features_df = []
    n_features = len(df.columns) - 1
    for i in range(0, n_features):
        tmp_df = df[[df.columns[i], target]]
        tmp_df = tmp_df[tmp_df[df.columns[i]] != 0]
        individual_features_df.append(tmp_df)

    all_correlations = {feature.columns[0]: feature.corr(
    )[target][0] for feature in individual_features_df}
    all_correlations = sorted(all_correlations.items(),
                              key=operator.itemgetter(1))
    if verbose:
        for (key, value) in all_correlations:
            print("{:>15}: {:>15}".format(key, value))

    return pd.DataFrame(all_correlations, columns=['features', 'corr_with_targets'])


def main():
    df = pd.read_csv('data/house_price.csv')
    df_num = filter_col(df)
    df_corr = caculate_correlation(df_num, target='SalePrice')
    plot_barh(df_corr)


if __name__ == "__main__":
    main()
