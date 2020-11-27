'''
以[Python工匠]，里氏替換原則內文舉例
第2種常見的難維護情況，父類子類同方法返回值不同
造成使用類別時難以管理
若按照里氏替換原則進行設計，子類應當可以任意抽換父類，並且程式還能跑
就能得出子類返回值應當設計成一樣的，甚至輸入參數也是，若未來需要擴充的情況下
就能夠確保類別使用方法不必修修改改，型別判斷，降低未來維護成本

本例子中兩類別中list_related_posts將修改為都使用generator(也可改成都是list，只是選擇的不同)
'''

from typing import Generator


class Post:
    """
    貼文
    """

    def __init__(self, post_id: int, name: str):
        self.id = post_id
        self.name = name

    def __repr__(self):
        return f'Post id {self.id} : {self.name}'


class User():
    """
    普通使用者
    """

    def __init__(self, username: str):
        self.username = username
        self.post_list = []

    def add_post(self, post):
        self.post_list.append(post)

    def list_related_posts(self) -> Generator[int, None, None]:
        """
        得到所有和該使用者有關的post
        """
        for post in self.post_list:
            yield post


class Admin(User):
    """
    管理員
    """


def main():
    # 初始化使用者及該使用者相關的文章
    u1, u2, admin = User('u1'), User('u2'), Admin('u3')
    p1, p2 = Post(1, 'jupyter'), Post(2, 'notebook')
    for user, post in zip([u1, u2], [p1, p2]):
        user.add_post(post)
        admin.add_post(post)

    # 列出所有使用者與其相關的文章
    for user in [u1, u2, admin]:
        print(f'{user.username}')
        for post in user.list_related_posts():
            print(f'{post}')


if __name__ == '__main__':
    main()
