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


## 說明
porgram 會搜尋論文中的 `[doi.org/ ...]`文字，然後使用 Chrome 搜尋所有的 citation。
接著會得到兩個檔案 `BibTex.txt`, `論文名稱`+`_replaced.txt`
![Finish](images/finish.png?raw=true "Finish")

1. `論文名稱`+`_replaced.txt`
論文內文的`[doi]`更改為`\cite{...}`，並儲存為`論文名稱`+`_replaced.txt`，並且將搜尋到的 BibTex 存放在 BibTex.txt。

1. `BibTex.txt`
citation 都放在檔案中。若不需使用中文註解，可以將 funciton `save_txt`第一行的 `add_zh_title(bibtex_text)`添加`translate=False`的參數。