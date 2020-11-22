'''
`SiteSourceGrouper`依賴於 `requests`, `lxml`
假想情境為 : 寫測試時，local端可以訪問外網，但是server端不行，縱使可以使用mock
但這裡希望將是否為local端還是server端與計算域名統計解耦合

Dependency Inversion Principle : 高階模組與低階模組不應該互相依賴，兩者應該依賴於抽象層
使用Dependency Inversion Principle
設計的好處，若需求頻繁變動在低階模組，很多新增項目，就能夠透過中基層一次收集起來，然後執行

典型的例子就是sklearn的Pipeline物件
或是自己寫的transformer抽象物件，裡面可以裝preprocessing function
'''
import requests
from lxml import etree
from typing import Dict
from collections import Counter
from abc import ABCMeta, abstractmethod


class HNWebPage(metaclass=ABCMeta):
    """
    抽象类：Hacker New 站点页面
    抽象類別無法被實例化，並且繼承本類別的子類別，都必須實作get_text
    """

    @abstractmethod
    def get_text(self) -> str:
        raise NotImplementedError


class RemoteHNWebPage(HNWebPage):
    """远程页面，通过请求 HN 站点返回内容"""

    def __init__(self, url: str):
        self.url = url

    def get_text(self) -> str:
        resp = requests.get(self.url)
        return resp.text


class LocalHNWebPage(HNWebPage):
    """本地页面，根据本地文件返回页面内容"""

    def __init__(self, path: str):
        self.path = path

    def get_text(self) -> str:
        with open(self.path, 'r') as fp:
            return fp.read()


class SiteSourceGrouper:
    """
    對HackNews進行域名的分組統計
    """

    def __init__(self, page: HNWebPage):
        self.page = page

    def get_groups(self) -> Dict[str, int]:
        """獲取 (域名, 个数) 分组
        """
        html = etree.HTML(self.page.get_text())
        elems = html.xpath(
            '//table[@class="itemlist"]//span[@class="sitestr"]')

        groups = Counter()
        for elem in elems:
            groups.update([elem.text])
        return groups


def test_grouper_from_local():
    page = LocalHNWebPage(path="data/static_hn.html")
    grouper = SiteSourceGrouper(page)
    result = grouper.get_groups()
    assert isinstance(result, Counter), "groups should be Counter instance"


def main():
    test_grouper_from_local()
    print('Test passed!')


if __name__ == '__main__':
    main()
