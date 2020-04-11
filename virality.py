from bs4 import BeautifulSoup
import requests
import spacy
import matplotlib.pyplot as plt

def ret_val(first,second):			#function to compare two given strings
	val=0
	l = abs(len(first)-len(second))
	for k in range(0,(min(len(first),len(second)))):
		i = first[k]
		j = second[k]
		val = val+(abs(ord(i)-ord(j)))
	val = val + l
	return val

def plot():								#function to plot a pie chart based on virality
	tot_score=0
	weight=[]
	for i in bbc:
		score=0
		for j in news:
			score=score+abs(ret_val(i,j))
		weight.append(score)
		m = weight.index(max(weight))
		exp = []
		for i in range (0,len(weight)):
			if i==m:
				exp.append(0.1)
			else:
				exp.append(0)
		tot_score= tot_score+score
	cnames = ['mediumseagreen',
	'mediumslateblue',
	'mediumspringgreen',
	'mediumturquoise',
	'mediumvioletred',
	'midnightblue',
	'mintcream',
	'mistyrose',
	'moccasin',
	'navajowhite',
	'navy',
	'oldlace',
	'olive',
	'olivedrab',
	'orange',
	'orangered',
	'orchid',
	'palegoldenrod',
	'palegreen',
	'palevioletred',
	'papayawhip',
	'peachpuff',
	'peru',
	'pink',
	'plum',
	'powderblue',
	'purple',
	'red',
	'rosybrown',
	'royalblue',
	'saddlebrown',
	'salmon',
	'sandybrown',
	'seagreen',
	'seashell',
	'sienna',
	'silver',
	'skyblue',
	'slateblue',
	'slategray',
	'snow',
	'springgreen',
	'steelblue',
	'tan',
	'teal',
	'thistle',
	'tomato',
	'turquoise',
	'violet',
	'wheat',
	'white',
	'whitesmoke',
	'yellow',
	'yellowgreen']
	patches, texts = plt.pie(weight, explode = exp, colors=cnames, shadow=True, startangle=90)
	plt.legend(patches, labels, loc="best")
	plt.axis('equal')
	plt.tight_layout()
	plt.suptitle("Most likely viral: "+"\'"+str(bbc[m])+"\'",fontsize=10)
	plt.show()
labels=[]														#to store subject of each news heading
nlp = spacy.load("en_core_web_sm");
#-------------------------------------------------------------Google news extraction---------------------------------------------------------
headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
count = 0
url_main = "https://news.google.com/?hl=en-IN&gl=IN&ceid=IN:en"
response_main = requests.get(url_main,timeout=20000)
content_main = BeautifulSoup(response_main.content,"html.parser")
news=[]
check=0
reps=0
for out in content_main.find_all('main',attrs = {"jsname": "fjw8sb"}):
	for tweet in out.find_all('article',attrs = {"jscontroller": "mhFxVb"}):
		word=""
		for q in tweet.find('a', attrs={'class': 'DY5T1d'}).text:
			if ((ord(q)>=32) and (ord(q)<=127)):
				word = word+q
		if word not in news:
			news.append(word)
			link = tweet.find('a', attrs={'class': 'DY5T1d'})['href']
			temp=link
			link = "news.google.com"+(str(temp))[1:]
			time_date = tweet.find('time', attrs={'class':'WW6dff uQIVzc Sksgp'})['datetime']
			date=time_date[0:10]
			time=time_date[11:(len(time_date)-1)]
		else:
			reps=reps+1
			if reps>len(news):
				check=1
		if check==1:
			break
#---------------------------------------------------------------BBC news extraction--------------------------------------------------------
bbc=[]
headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
current=[]
count = 0
current.append("/news/world-asia-india-52255011")
for i in range(0,12):
	url_main = "https://bbc.com"+current[i]
	response_main = requests.get(url_main,timeout=20000, headers=headers)
	content_main = BeautifulSoup(response_main.content,"html.parser")
	subs=[]
	intermediate=""
	qwe=''
	tweet=''
	for qwe in content_main.find_all('div',attrs = {"class": "group story-alsos more-on-this-story"}):
		for tweet in qwe.find_all('li',attrs = {"class": "unit unit--regular"}):
			intermediate = tweet.find('a', attrs={'class': 'unit__link-wrapper'})['href']
			if intermediate not in subs and intermediate not in current:
				subs.append(intermediate);
	title1=""
	if (content_main.find('h1', attrs={'class': 'story-body__h1'})):
				title1 = content_main.find('h1', attrs={'class': 'story-body__h1'}).text
	bbc.append(title1)
	doc = nlp(title1)
	for token in doc:
		if token.dep_=="nsubj":
			labels.append(str(token))
	if (i%2==0):
		for j in subs:
			url = "https://bbc.com"+j
			response = requests.get(url,timeout=20000, headers=headers)
			content = BeautifulSoup(response.content,"html.parser")
			for qwe in content_main.find_all('div',attrs = {"class": "group story-alsos more-on-this-story"}):
				for tweet in qwe.find_all('li',attrs = {"class": "unit unit--regular"}):
					intermediate = tweet.find('a', attrs={'class': 'unit__link-wrapper'})['href']
					if intermediate not in current:
						current.append(intermediate);
			if (content.find('h1', attrs={'class': 'story-body__h1'})):
				title = content.find('h1', attrs={'class': 'story-body__h1'}).text
			bbc.append(title)
			doc = nlp(title)
			for token in doc:
				if token.dep_=="nsubj":
					labels.append(str(token))
	elif (i%2==1):
		for j in range (0,len(subs)-1):
			url = "https://bbc.com"+subs[j]
			response = requests.get(url,timeout=20000, headers=headers)
			content = BeautifulSoup(response.content,"html.parser")
			for qwe in content_main.find_all('div',attrs = {"class": "group story-alsos more-on-this-story"}):
				for tweet in qwe.find_all('li',attrs = {"class": "unit unit--regular"}):
					intermediate = tweet.find('a', attrs={'class': 'unit__link-wrapper'})['href']
					if intermediate not in current:
						current.append(intermediate);
			if (content.find('h1', attrs={'class': 'story-body__h1'})):
				title = content.find('h1', attrs={'class': 'story-body__h1'}).text
			bbc.append(title)
			doc = nlp(title)
			for token in doc:
				if token.dep_=="nsubj":
					labels.append(str(token))
plot()