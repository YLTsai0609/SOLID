'''
以[Python工匠]，里氏替換原則內文舉例
不使用里氏替換原則進行類別設計的缺點為
類別的使用方法為了邏輯實現，需要加入判斷式來判斷目前的物件是什麼
如果未來的需求容易產生多個子類別，且和父類同名方法需要有不同的行為，
那麼維護成本就會提高，可讀性也降低
以下舉例為
普通使用者User及管理員Admin對於停用方法`deactivate`的設計方式所需付出的維護成本

若未來加入了Staff類別，VIP類別等，對於停用方法可能又有不同的要求，屆時維護成本提高
以下透過理事替換原則進行設計，設計邏輯為 子類應當可以把父類全部換掉，程式還是能跑
以下設計使得未來需求就算擴充到Staff, VIP, deactivate_users也不用重寫，可讀性也較好 
'''
from typing import Iterable


class User():
    """
    普通使用者
    """

    def __init__(self, username: str):
        self.username = username

    def allow_deactivate(self) -> bool:
        """
        是否允許停用
        """
        return True

    def deactivate(self):
        """
        停用該使用者
        """
        self.is_active = False


class Admin(User):
    """
    管理員
    """

    def allow_deactivate(self) -> bool:
        """
        是否允許停用
        """
        return False

    def deactivate(self):
        """
        停用該使用者，但Admin不能被停用
        """
        raise NotImplementedError('Cannot deactivate Admin')


def deactivate_users(users: Iterable[User]):
    """
    批量停用使用者
    """
    for user in users:
        # 該使用者無法被停用
        if not user.allow_deactivate():
            print(
                f'skip deactivating user {user.username}\n because it is {user.__class__.__name__}')
            continue
        else:
            user.deactivate()


def main():
    users_admin_mixed = [User('u1'), User('u2'), Admin('u3')]
    deactivate_users(users_admin_mixed)


if __name__ == '__main__':
    main()
