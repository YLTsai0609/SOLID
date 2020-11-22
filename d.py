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


class SiteSourceGrouper:
    """
    對HackerNews的域名進行分組統計
    """

    def __init__(self, url: str):
        self.url = url

    def get_groups(self) -> Dict[str, int]:
        """
        獲取域名、個數資料
        """
        resp = requests.get(self.url)
        html = etree.HTML(resp.text)
        elems = html.xpath(
            '//table[@class="itemlist"]//span[@class="sitestr"]')

        groups = Counter()
        for elem in elems:
            groups.update([elem.text])
        return groups


def test_grouper_returning_valid_types():
    """测试 get_groups 是否返回了正确类型
    """
    grouper = SiteSourceGrouper('https://news.ycombinator.com/')
    result = grouper.get_groups()
    assert isinstance(result, Counter), "groups should be Counter instance"


def main():
    groups = SiteSourceGrouper("https://news.ycombinator.com/").get_groups()
    for key, value in groups.most_common(3):
        print(f'Site: {key} | Count: {value}')
    test_grouper_returning_valid_types()
    print('Test passed!')


if __name__ == '__main__':
    main()
