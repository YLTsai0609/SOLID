'''
以[Python工匠]，里氏替換原則內文舉例
不使用里氏替換原則進行類別設計的缺點為
類別的使用方法為了邏輯實現，需要加入判斷式來判斷目前的物件是什麼
如果未來的需求容易產生多個子類別，且和父類同名方法需要有不同的行為，
那麼維護成本就會提高，可讀性也降低
以下舉例為
普通使用者User及管理員Admin對於停用方法`deactivate`的設計方式所需付出的維護成本
'''
from typing import Iterable


class User():
    """
    普通使用者
    """

    def __init__(self, username: str):
        self.username = username

    def deactivate(self):
        """
        停用該使用者
        """
        self.is_active = False


class Admin(User):
    """
    管理員
    """

    def deactivate(self):
        """
        管理員無法被停用
        Raises:
            RuntimeError: [管理員無法被停用]
        """
        raise RuntimeError('admin can not be deactivated!')


def deactivate_users(users: Iterable[User]):
    """
    批量停用使用者
    """
    for user in users:
        # 無法停用管理員，跳過
        if isinstance(user, Admin):
            print(f'skip deactivating admin user {user.username}')
            continue
        else:
            user.deactivate()


def main():
    users_admin_mixed = [User('u1'), User('u2'), Admin('u3')]
    deactivate_users(users_admin_mixed)


if __name__ == '__main__':
    main()
