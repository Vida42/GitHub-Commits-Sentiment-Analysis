import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from scipy import stats

def myVader(each):
    comments_set = []

    try:
        view = each.strip().replace('\r','').split('\n')
        # print(res)
        # print(type(res))
    except:
        view = list(str(each))
        # print(res)
        # print(type(res))
    # print(view)
    sid = SentimentIntensityAnalyzer()
    # emotion = []

    emotion_view = []
    try:
        for sentence in view:
            # print(sentence)
            ss = sid.polarity_scores(sentence)
            emotion_view.append(ss['compound'])
            # for k in sorted(ss):
            #     print('{0}: {1}, '.format(k, ss[k]), end='')
            # print()
        mean = stats.tmean(emotion_view)
        # emotion.append(mean)
    except:
        mean = 0
    # print(mean)
    return mean
