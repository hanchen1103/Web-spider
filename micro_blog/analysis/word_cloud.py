from wordcloud import WordCloud
import matplotlib.pyplot as plt


def img_grearte():
    with open("txt_comment.txt", "r") as file:
        txt = file.read()
    word = WordCloud(background_color="white",
                     width=800,
                     height=800,
                     font_path='Songti.ttc',
                     ).generate(txt)
    word.to_file("comment_word_cloud.png")
    plt.imshow(word)
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    img_grearte()