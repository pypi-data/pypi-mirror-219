import os
from win32com.client import Dispatch


def doc_to_docx(file_path, word):
    """
    将指定的doc文件转化为docx格式
    file_path: 文件路径
    word: 代表word应用程序
    """
    # 打开原始文档
    doc = word.Documents.Open(file_path)

    # 将文档另存为docx格式
    new_file_path = os.path.splitext(file_path)[0] + ".docx"
    doc.SaveAs(new_file_path, 16)

    # 关闭文档
    doc.Close()

    # 删除原始文件
    # os.remove(file_path)

    # 打印操作过程
    print(f"{file_path}已经被成功转换为{new_file_path}")


def main():
    # 定义文件夹路径和Word应用程序对象
    folder_path = r"D:\dbzqPro\pythonProject3\Text"
    word = Dispatch("Word.Application")

    # 遍历文件夹中所有的.doc文件，并将其转换为.docx格式
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".doc"):
                file_path = os.path.join(root, file)
                doc_to_docx(file_path, word)

    # 关闭Word应用程序
    word.Quit()

    print("全部doc文件已经全部转换为docx!")


if __name__ == "__main__":
    main()