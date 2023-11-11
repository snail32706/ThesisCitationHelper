from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from googletrans import Translator
import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog

"""
歡迎使用論文 citation 搜尋器，這個程式幫助您你將論文 citation 的 BibTex 找出，並輸出為「BitTex.txt」檔案。
    
請將論文的格式以 md file 撰寫，並且 citation 使用 "[doi.org/...]" 的方式寫下。
經過此程式，會獲得一個新的 md file，並將內文的`[doi]`更改為`\cite{...}`，搜尋到的 BibTex 存放在 BitTex.txt。
並且更改為`\cite{...}`的檔案放在 program 的檔案中。

"""
def select_file():
    # 创建一个 Tkinter 根窗口，但不显示
    root = tk.Tk()
    root.withdraw()

    # 显示文件选择对话框
    file_path = filedialog.askopenfilename(
        title='选择文件',
        filetypes=[('Markdown files', '*.md'), ('Text files', '*.txt')]
    )

    # 返回选择的文件路径
    return file_path

def search_url(keyword):
    google_scholar = "https://scholar.google.com/scholar"
    encoded_keyword = quote_plus(keyword)
    return f"{google_scholar}?hl=en&as_sdt=0%2C5&q={encoded_keyword}&btnG="

def save_txt(bibtex_text):
    BibTex_add_zh_title = add_zh_title(bibtex_text)
    with open("BitTex.txt", "a", encoding="utf-8") as file: # 'a': 追加模式
        file.write(BibTex_add_zh_title)

def translate_text(text, dest_language='zh-TW'):
    translation = Translator().translate(text, dest=dest_language)
    return translation.text

def extract_bibtex_title(bibtex_text):
    """
    找出 BibTex title，目的是翻譯而已，不喜歡這個功能的話可以自行刪除。

    """
    title_match = re.search(r"title=\{(.+?)\}", bibtex_text)
    if title_match:
        title = title_match.group(1)
        return title
    else:
        return "在 BibTex 條目中找不到 title."

def extract_bibtex_identifier(bibtex_text, doi):
    """
    找出 BibTex citation 互換的文字。

    """
    match = re.search(r"@article\{([^,]+),", bibtex_text) # `([^,]+)`：捕獲一個或多個非逗號字元。 這部分匹配條目標識符。
    if match:
        return match.group(1)
    else:
        return f"{doi} 沒有找到"

def add_zh_title(bibtex_text):
    title_en = extract_bibtex_title(bibtex_text)
    title_zh = translate_text(title_en)

    BibTex_add_zh_title = f"% {title_zh}\n{bibtex_text}\n"
    return BibTex_add_zh_title 

def search_google_scholar(doi, driver):
    
    url = search_url(doi)
    driver.get(url)
    time.sleep(1.5)

    try:
        # 点击第一个搜索结果的“Cite”按钮
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "gs_or_cit"))
        ).click()
        time.sleep(.5)

        # 在弹出的引用选项中，找到并点击“BibTeX”链接
        bibtex_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "BibTeX"))
        )
        bibtex_link.click() # 打開 BibTex
        time.sleep(.5)

        # 获取BibTeX信息所在的元素
        bibtex_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))

        # 从元素中提取文本
        bibtex_text = bibtex_element.text

        save_txt(bibtex_text)
        time.sleep(.5)
        output_str = extract_bibtex_identifier(bibtex_text, doi)
        return output_str # 表示成功

    except Exception as e:
        print(f"執行{doi}發生錯誤: {e}")
        time.sleep(.5)
        return f"{doi} 沒有找到 BibTex" # 表示失敗

def foor_loop_case(doi_text_list, driver):
    """
    `doi_text_list` is a doi list.
    ex: ["doi.org/10.1016/j.apsusc.2005.07.100", "doi.org/10.3390/ma15041378", "doi.org/10.1016/j.mssp.2013.09.026"]

    """
    resplace_list = []
    for doi in doi_text_list:
        output_str = search_google_scholar(doi, driver)
        resplace_list.append(output_str)

    return resplace_list

def check_file(fpath):
    if os.path.exists(fpath) and (fpath.endswith('.md') or fpath.endswith('.txt')):
        # 获取文件名和后缀
        filename = os.path.basename(fpath)
        backup_filename = os.path.splitext(filename)[0] + "_backup.txt"

        # 获取当前工作目录并构建完整的备份路径
        current_dir = os.getcwd()
        backup_path = os.path.join(current_dir, backup_filename)

        # 備份文件
        shutil.copy(fpath, backup_path)
        print("檔案備份成功")
        return True
    else:
        print("檔案不存在或格式不正确")
        return False


def open_md_file(fpath):
    if check_file(fpath):
        with open(fpath, 'r', encoding='utf-8') as file:
            content = file.read()
        return os.path.basename(fpath), content
    else:
        return None, None


def thesis_doi_list(fpath):
    """
    將 thesis 內文中所有的 citation [doi.org/...] 找出

    """
    fname, file_content = open_md_file(fpath)

    if file_content:    # 如果檔案有成功打開
        doi_pattern = r"\[doi\.org/([^\]]+)\]"
        doi_list = re.findall(doi_pattern, file_content)
        doi_list = [f"doi.org/{doi}" for doi in doi_list]  # 格式化为完整的 DOI
        return doi_list

def thesis_doi_replaced(fpath, replace_list):
    """
    將內文中的 [doi.org/...] 更換成 \cite{name}
    """
    fname, file_content = open_md_file(fpath)

    if file_content and replace_list:  # 如果文件打开成功且替换列表非空
        # 寻找所有的 DOI
        doi_pattern = r"\[doi\.org/([^\]]+)\]"
        doi_matches = re.findall(doi_pattern, file_content)

        # 检查找到的 DOI 数量与替换列表长度是否一致
        if len(doi_matches) != len(replace_list):
            print("錯誤：doi 數量與替換清單長度不匹配")
            return

        # 替换所有的 DOI
        for doi, replacement in zip(doi_matches, replace_list):
            file_content = file_content.replace(f"[doi.org/{doi}]", f"\\cite{{{replacement}}}")

        # 保存替换后的内容到新文件
        filename = os.path.basename(fpath)
        replaced_filename = os.path.splitext(filename)[0] + "_replaced.txt"
        with open(replaced_filename, 'w', encoding='utf-8') as file:
            file.write(file_content)

        print(f"doi 替換成功")

if __name__ == "__main__":
    fpath = select_file()
    

    if fpath:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        time.sleep(3)

        # search_google_scholar("doi.org/10.1016/j.apsusc.2005.07.100", driver) # test
        doi_list = thesis_doi_list(fpath)
        with open("BitTex.txt", "w", encoding="utf-8") as file: # 'w': 複寫模式
            file.write(f"{doi_list}\n\n")

        replace_list = foor_loop_case(doi_list, driver)
        thesis_doi_replaced(fpath, replace_list)
        driver.quit()

    else:
        print("未選擇文件")





