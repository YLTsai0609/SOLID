'''
以[Python工匠]，里氏替換原則內文舉例
第2種常見的難維護情況，父類子類同方法返回值不同
造成使用類別時難以管理
'''

from typing import Iterable, Generator


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

    def add_post(self, name):
        self.post_list.append(name)

    def list_related_posts(self) -> Iterable[int]:
        """
        得到所有和該使用者有關的PostId
        """
        return self.post_list


class Admin(User):
    """
    管理員
    """

    def list_related_posts(self) -> Generator[int, None, None]:
        """
        管理員和所有文章都有關係，以Generator傳回，節省記憶體空間
        Yields:
            Generator[int]: post id
        """
        for post in self.post_list:
            yield post.id


def main():
    # 初始化使用者及該使用者相關的文章
    u1, u2, admin = User('u1'), User('u2'), Admin('u3')
    p1, p2 = Post(1, 'jupyter'), Post(2, 'notebook')
    for user, post in zip([u1, u2], [p1, p2]):
        user.add_post(post)
        admin.add_post(post)

    # 列出所有使用者與其相關的文章
    for user in [u1, u2, admin]:
        print(f'{user.username} : {user.list_related_posts()}')


if __name__ == '__main__':
    main()
