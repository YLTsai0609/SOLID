'''
接口隔離原則(Interface Segregation Principle)
使用者/客戶若只使用到A功能，那麼類別就不要給A功能以外的方法


不這麼設計的壞處 : 以避免未來繼承時、擴充時接口可能出現無法預期的bug，或是子類無法完全取代父類的行為
使用街口隔離原則設計的好處 : 未來在擴充時，子類容易完全取代父類行為，小的接口不容易出現無法預期的bug
'''


def is_new_visitor(response) -> bool:
    """
    從cookie判斷是否是新的訪客
    """
    return response.cookies.get('is_new_visitor') == 'y'
