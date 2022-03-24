import jieba
import re
from micro_blog.mblog_spider import cursor
from bs4 import BeautifulSoup


def clean_chineses_text(text):
    if not verify_str(text):
        return ''
    # 去掉html标签
    text = BeautifulSoup(text, 'html.parser').get_text()
    text = jieba.lcut_for_search(text)
    # 加载停用词(中文)
    stopwords = {}.fromkeys([line.rstrip() for line in open('./cn_stopwords.txt')])
    # 去掉重复的词
    eng_stopwords = set(stopwords)
    # 去除文本中的停用词
    words = [w for w in text if w not in eng_stopwords]
    return ' '.join(words)


def is_chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def verify_str(string):
    if string is None or string == '' or string == ' ':
        return False
    return True


def get_from_db():
    sql_page_info = "select content2, page_title, title from page_info"
    sql_comment = "select text from comment"
    sql_status = "select raw_text, m_text from status"
    cursor.execute(sql_page_info)
    res_page_info = []
    list_page_info = cursor.fetchall()
    cursor.execute(sql_comment)
    res_comment = []
    list_comment = cursor.fetchall()
    cursor.execute(sql_status)
    res_status = []
    list_status = cursor.fetchall()
    for i in list_page_info:
        if verify_str(i[0]):
            res_page_info.append(i[0])
        if verify_str(i[1]):
            res_page_info.append(i[1])
        if verify_str(i[2]):
            res_page_info.append(i[2])
    for i in list_comment:
        if verify_str(i[0]):
            res_comment.append(i[0])
    for i in list_status:
        if verify_str(i[0]):
            res_status.append(i[0])
        if verify_str(i[1]):
            res_status.append(i[1])
    return res_page_info, res_comment, res_status


def remove_tag(text):
    return re.sub('<[^<]+?>', '', text)


def split_word():
    page_list, comment_list, status_list = get_from_db()
    page_str = ''
    comment_str = ''
    status_str = ''
    for i in page_list:
        page_str += clean_chineses_text(i)

    for i in comment_list:
        comment_str += clean_chineses_text(i)

    for i in status_list:
        status_str += clean_chineses_text(i)

    print(page_str)
    with open("txt_page_info.txt", 'w') as file:
        file.write(comment_str)
    with open("txt_comment.txt", 'w') as file:
        file.write(page_str)
    with open("txt_status.txt", 'w') as file:
        file.write(status_str)
    with open("txt_all.txt", 'w') as file:
        file.write(comment_str + ' ' + page_str + ' ' + status_str)


if __name__ == "__main__":
    split_word()

