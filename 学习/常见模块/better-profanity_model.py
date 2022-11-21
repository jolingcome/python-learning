# 敏感词过滤的工具，better-profanity，它是基于 Ben Friedland 开发的 profanity，在其基础上，
# 由原来的基于正则的方法改成了现在的字符串比对，速度上提升了不少，同时支持拼写上的一些修改，
# 如 b*tch、p0rn 等，不过可惜的是，目前这个库还不支持中文。
# https://xugaoxiang.com/2022/08/19/python-module-34-better-profanity/
# pip install better_profanity==0.6.1

from better_profanity import profanity
if __name__=="__main__":
    profanity.load_censor_words() # load_censor_words会导入profanity_wordlist.txt默认的敏感词库，使用特定的算法(可以去读源码 better_profanity.py)，衍生出一些常见的变种写法
    text = "what a fcuk"
    censored_text=profanity.censor(text)
    print(censored_text)

#2.发现敏感词后，默认会将目标字符串用4个 * 号来代替，当然，这个也是可以更改的
    text_1= "You p1ec3 of sHit."
    censored_text=profanity.censor(text_1,'-')
    print(censored_text)
#3.可以自己来维护一个敏感词文件
    profanity.load_censor_words('my_word.txt')
    text_2="xijiangping is fcuk"
    censored_text_2=profanity.censor(text_2)
    print(censored_text_2)
#4.如果想将某些词从敏感词中暂时剔除，可以使用白名单机制
    profanity.load_censor_words_from_file('my_word.txt', whitelist_words=['merry'])
