# 資源

* 參考[Python 工匠](https://github.com/piglei/one-python-craftsman)

# 為什麼需要SOLID

* 比起23種設計模式，設計原則適用性更加廣泛，也較容易入門學習，SOLID是眾多設計原則之中最有名的一個設計原則
* 設計原則與設計模式都是經過時間考驗後的程式設計師所寫下，遵從設計原則可以讓程式碼容易維護及擴展，反之則會難以維護，不容易擴展
* 設計原則並非不可以違反，而是普遍來說容易維護和擴展，若有特殊需求可以重新考量是否要遵從原則

# 各章節內容

S : 單一責任原則 Single Responsibility Principle

    - 搭配例子 - [相關係數分析] 分析數值變數和目標變數的相關係數，並畫出barh

O : 封閉修改，開放擴充原則 Open-Closed Principle

    - 搭配例子 - [深度學習的實驗分析] 輸入實驗名稱並畫出3-fold loss, accuracy vs epoch

L : 里氏替換原則 Liskov Substitution Principle

    - 搭配例子 - [以User及Admin的停用操作，列出相關貼文兩個功能舉例] 

I : 接口隔離原則 Interface Segregation Principles

    - 搭配例子 TBC

 

D : 依賴倒置原則 Dependency Inversion Principle

    - 搭配例子 TBC

# 安裝

 `conda create --name solid python=3.6`

 `conda activate solid`

 `pip install -r requirements.txt`
