# News_Virality
Repository that stores code to anticipate likelihood of a news article being viral


Explanation of the code: 

The code scrapes information from two news websites, namely: BBC world news and Google news. There is a reason why these two websites were chosen: 
1. BBC World News: Always reports verified and trustworthy information and has a huge number of reporters thereby ensuring that most news around the world is covered. 
While anticipating the virality of a news article, I found it rudimentary that since it is news, it becomes viral only if  the major news websites picks up on it. The two aforementioned benefits I mentioned for using BBC World News seemed to satisfy this requirement. 
2. Google News: Has reports from several medium sized news websites. By using Google News, we can find out how many websites are currently reporting news related to a certain topic.

The code first scrapes news titles from both websites and compiles them into lists. It then checks each BBC news article with the Google articles to find similarities between the two articles. I reasoned that if a major news websites and several medium sized news websites were reporting the same story, it would soon be picked up by smaller networks and would soon be tweeted about and so on and so forth. 

After checking for similarites(referred to as "scores" in the code), I plotted a pie chart to show relative potential virality of each news article. The pie graph shows only the subject of each article (extracted using the spacy Natural Language Processing package) to avoid congestion. The title of the plot is the most potentially viral news article. 

Required Packages: 
-BeautifulSoup
-requests
-spacy
-matplotlib.pyplot as plt
