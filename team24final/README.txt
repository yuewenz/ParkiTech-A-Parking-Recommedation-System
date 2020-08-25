1.DESCRIPTION:
(1) 'Final Code' folder contains all necessary codes to run our final work.
'Final Code\code' folder contains all the core code including the back-end part and the server.py to creat a listening handler
'Final Code\data' folder contains all the data we use
'Final Code\html' folder contains the html file and image source fo rthe web page.
(2) 'Data Clean' folder contains all codes required for data clean. You don't need to run them. They are just for reference. Just in case you are interested, before running any notebook file, you should put the data source file (link in section 5) in side the folder.

2.INSTALLATION:
Download the tornado. Tornado is a Python web framework and asynchronous networking library. 
Please make sure you download the correct version for your system. After downloading it,
please unzip and install it under the directory where you installed your python. 
Put 'myfolder' directly under the directory of tornado-master.
Use Anaconda to execute the server.py script in 'code' folder. It will create a listening handler.
Use ‘python -m http.server [port number]’ to construct a server on PC. You can use any port number except 8000.
Because We use it as the URL for receiving request from web page. And if you didn't type in a specific one, cmd will use 
the default number 8000, which will lead to an error by all means.

3.EXECUATION:
Use FireFox browser to open our html file(in the 'html' folder), and you can operate it now.

4.ABOUT VIDEO:
According to my own experience, we need to know the python environment explicitly in advance.
It's because tornado frame requires python’s support and our sophisticated back-end programs also relies on python. 
Make sure you update relative libraries to correct versions.I will also attach a video to show my demo’s good performance.
If you failed to run it, you can watch the demo video. 
https://youtu.be/-fOp2qo7tDM

5.DATA SOURCE:
https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/YLWCSU/JR6JYL&version=2.0