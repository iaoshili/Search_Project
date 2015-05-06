To start the server, simply use
```python
python starter.py
```

The url where our system is running on is: http://linserv2.cims.nyu.edu:40010/

What you can play with this url:
1 In the home page, you can upload a document (preferably txt format) of one English article. And we will try to find out in what big category this document belongs to.

But if you would like to see our recommending tags, (tags here refer to more fine domain than category) please upload a document talking about technology as our training set in this part comes from MIT news. Or you could simply just download an article from MIT news to get the best performance.

P.S. Once uploaded a file, it will upload the file to uploads/ folder and generate a uuid4 for the file.
2 In the "Search" tab, you can search among the articles we crawled from Verge.com. You could choose your domain of interest and search
for articles by inputing keywords in the text field.

The code you can play with:
3 In directory "final_server/" there is a python file called "SampleClassifier.py". This program does the job of suggesting tags in our url.
You need Python 2.7, and nltk to run it. There is a demo in this file in the end. Just uncomment the line below "#Demo" and test it.
http://www.nltk.org

4 You could also play with our tags suggestion program. This is an experimental "offline" program located in folder "Tag recommendation".
You will need python to run the code there.
There are two programs in particular:
"tagRecomenderChinese.py": Chinese tag recommender. Just directly run this program and see the result. The data is "Notes.enex" which is exported from 38 of my notes Recipe Evernote book. The code is easy to be understood.


5 You could also run the web application on your own computer.
Just change working directory to `Search_Project/final_server' and use command `python starter.py' to start the application. 

6 In case you would like to try out our crawler. 
The source code is written in java. You could go to "java" directory, import all the jar dependencies and the codes in "java/src" directory. And run "Main.java". 