# Thesis Citation Helper - 論文引用助手
### 歡迎使用 Thesis Citation Helper
此 porgram 提供您將論文 citation 的 BibTex 找出，並輸出為「BibTex.txt」檔案。

使用 Latex 撰寫論文時，citation 一項是個非常麻煩的問題，為了提高寫作速度，我們使用爬蟲將 BibTex 查找工作交給了電腦。

## 使用方法

### 基本環境
1. 撰寫論文時，所有的 ciatiton 使用中括號將 doi 放入`[doi.org/ ...]`，論文的格式可以為 `.tex`, `.md`, `.txt`。
2. 確保在電腦已經安裝 `Chrome`

### 安裝 Library
main.py call 了許多 library，像是`selenium`, `tkinter`, ...等，使用前務必使先安裝，

### 執行方法
執行 python 檔即可
```bash
python3 main.py
```
porgram 會開啟一個對話筐
![Choose File](images/chooseFile.png?raw=true "Choose File")
在此選擇您的論文，接著 porgram 會搜尋論文中的 `[doi.org/ ...]`文字，然後使用 Chrome 搜尋所有的 citation。
接著會得到兩個檔案 "Bi", ""
![Finish](images/finish.png?raw=true "Finish")
歡迎使用論文 citation 搜尋器，這個程式幫助您你將論文 citation 的 BibTex 找出，並輸出為「BibTex.txt」檔案。
    
請將論文的格式以 md file 撰寫，並且 citation 使用 "[doi.org/...]" 的方式寫下。
經過此程式，會獲得一個新的 md file，並將內文的`[doi]`更改為`\cite{...}`，搜尋到的 BibTex 存放在 BibTex.txt。
並且更改為`\cite{...}`的檔案放在 program 的檔案中。