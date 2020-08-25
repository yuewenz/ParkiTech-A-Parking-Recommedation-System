import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Congratulation')
        self.write(greeting + ', tornado install successfully')
        #file = open('new_file' + '.txt','w')
        #file.close()
        #separate the parameter by ,-----------------------

        # ------------------------------------------------- 
        temp=""
        for i in range(len(greeting)):
            if greeting[i]=="(" or greeting[i]==")" :
                pass
            else:
                temp+=greeting[i]
        temp+=","
        str_list=[]
        temp_str=""
        for i in range(len(temp)):
            if(temp[i]!=","):
                temp_str+=temp[i]
            else:
                str_list.append(temp_str)
                temp_str=""

        para_str=""
        for i in str_list:
            para_str+=i
            para_str+=" "

        mystring_parameter='python main.py'+' '+para_str
        os.system('dir')
        os.system(mystring_parameter)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()