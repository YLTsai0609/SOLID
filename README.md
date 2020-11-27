# 為什麼需要SOLID

* 比起23種設計模式，設計原則適用性更加廣泛，也較容易入門學習，SOLID是眾多設計原則之中最有名的一個設計原則
* 設計原則與設計模式都是經過時間考驗後的程式設計師所寫下，遵從設計原則可以讓程式碼容易維護及擴展，反之則會難以維護，不容易擴展
* 設計原則並非不可以違反，而是普遍來說容易維護和擴展，若有特殊需求可以重新考量是否要遵從原則

# 各章節內容

S : 單一責任原則 Single Responsibility Principle

    - 小、小、小，一個函數、一個類別只做一件事，當你因為一個以上的原因修改某個函數和類別時，表示該函數/類別，應該要被拆開了

    - 搭配例子 - [相關係數分析] 分析數值變數和目標變數的相關係數，並畫出barh，從一個大函數拆成三個小函數

O : 封閉修改，開放擴充原則 Open-Closed Principle

    - 對修改關閉，對擴充開放，找出經常改的地方，把他隔離出來，就像python的`sort`可以傳入一隻函數來調整怎麼排序一樣

    - 搭配例子 - [深度學習的實驗分析] 輸入實驗名稱並畫出3-fold loss, accuracy vs epoch

L : 里氏替換原則 Liskov Substitution Principle

    - 子類應當可以完全替代父類的行為，如果不行，意味著該類別的使用方法要進行類別判斷，使維護成本提高，建議重新設計類別

    - 方法的輸入參數及輸出值的型態也需要一致，減少未來莫名的bug產生

    - 搭配例子 - [以User及Admin的停用操作]，列出相關貼文兩個功能舉例，說明如何重新設計類別，讓類別使用方法更順暢

I : 接口隔離原則 Interface Segregation Principles

    - 接口中的單一責任原則，不要給使用者他不會用到的方法，乾淨的接口有助於長久維護，減少殭屍方法

    - 搭配例子 [使用者屬性檢查] 以使用者是否為新訪客的檢查為例，與其傳入整個response，事實上僅需傳入cookie即可，不需要整個response

 

D : 依賴倒置原則 Dependency Inversion Principle

    - 當高階模組與低階模組之間變動頻繁時，容易互相影響，一個壞掉另一個也不能動，此時可以學習sklearn的`Pipeline`哲學，Transformer依賴於Pipeline，training行為也依賴於Pipeline，方便新增修改刪除

    - 搭配例子 [網頁分析] 以測試網頁中對各域名統計為例，若Server無法連外網，則需要一個LocalPage的類別，兩者皆依賴於HNWebPage類別

# 安裝

 `conda create --name solid python=3.6`

 `conda activate solid`

 `pip install -r requirements.txt`

# 參考資料

* [Python 工匠](https://github.com/piglei/one-python-craftsman)
