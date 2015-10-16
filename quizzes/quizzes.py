"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
import os
import sys
import json
import thread
import datetime
import re
import subprocess
import urllib
import urllib2
import httplib
import hashlib
import base64
import time

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List, Boolean
from xblock.fragment import Fragment

from config import Config
from lib_util import Util
reload(sys)
sys.setdefaultencoding('utf-8')

class MyXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    logger = Util.uc_logger()

    src = String(default="", scope=Scope.content, help="html context")
    path = String(default="", scope=Scope.content, help="file path")
    CONFIG = Config.CONFIG
 
    root_token=CONFIG["root_token"]
    repo_id=CONFIG["teacher_id"]
    git_port=CONFIG["gitlab_port"]
    git_host=CONFIG["gitlab_host"]
    github_username=CONFIG["github_username"]
    github_repo=CONFIG["github_repo"]
    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the MyXBlock, shown to students
        when viewing courses.
        """

         # runtime error
        if not hasattr(self.runtime, "anonymous_student_id"):
            return self.message_view("Error  (get anonymous student id)", "Cannot get anonymous_student_id in runtime", context)

        if self.runtime.anonymous_student_id == "student": 
            context_dict = {
            "username": "",
            "email":"",
            "name":self.src
            }

            fragment = Fragment()
            fragment.add_content(Util.render_template('static/html/myxblock.html', context_dict))
            fragment.add_css(Util.load_resource("static/css/myxblock.css"))
            fragment.add_css(Util.load_resource("static/css/quizzes.css"))
            fragment.add_css(Util.load_resource("static/css/sh_style.css"))

           
            fragment.add_javascript(Util.load_resource("static/js/src/sh_main.js"))
            fragment.add_javascript(Util.load_resource("static/js/src/sh_c.js"))
            fragment.add_javascript(Util.load_resource("static/js/src/myxblock.js"))
            fragment.initialize_js("MyXBlock")
            return fragment
 							
           
        student = self.runtime.get_real_user(self.runtime.anonymous_student_id)
        email = student.email
        name = student.first_name + " " + student.last_name
        username = student.username
        
        if name == " ":
            name = username

        context_dict = {
            "username": username,
            "email":email,
            "name":self.src
        }

        fragment = Fragment()
        
        fragment.add_content(Util.render_template("static/html/myxblock.html", context_dict))
        fragment.add_css(Util.load_resource("static/css/myxblock.css"))

        fragment.add_css(Util.load_resource("static/css/quizzes.css"))
        fragment.add_css(Util.load_resource("static/css/sh_style.css"))

        fragment.add_javascript(Util.load_resource("static/js/src/sh_main.js"))
        fragment.add_javascript(Util.load_resource("static/js/src/sh_c.js"))
        fragment.add_javascript(Util.load_resource("static/js/src/myxblock.js"))
        
        fragment.initialize_js("MyXBlock")
        return fragment

    def studio_view(self, context=None):
        context_dict = {
            "title": "",
            "message": self.path
        }

        fragment = Fragment()
        fragment.add_content(Util.render_template('static/html/studio_view_new.html', context_dict))
        fragment.add_css(Util.load_resource("static/css/studio.css"))
        fragment.add_javascript(Util.load_resource("static/js/src/myxblock.js"))
        fragment.initialize_js("MyXBlock")
        return fragment

    def message_view(self, title, message, context=None):
        context_dict = {
            "title": title,
            "message": message
        }
        fragment = Fragment()
        fragment.add_content(Util.render_template('static/html/message_view.html', context_dict))
        fragment.initialize_js("MyXBlock")
        return fragment

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def studio_submit(self, data, suffix=""):
        self.logger.info("src"+ data["src"])
        self.path=data["src"]
        
        self.logger.info("path"+self.path)
        # f=open("/edx/var/edxapp/staticfiles/_book/"+data["src"], "rb")
        # context=f.read()
        # f.close()
        url="https://api.github.com/repos/%s/%s/contents/_book/%s" %(self.github_username, self.github_repo, data["src"])
        self.logger.info("github url:"+url)
        try:
          response=urllib2.urlopen(url)
          result=response.read()

          html=base64.b64decode(json.loads(result)["content"])
        except Exception,e:
          self.logger.info(e)
        m=re.search('(<div)([\s\S]+)(<\/div>)', html, re.M)
        if m:
           context=m.group().replace('<body>','')
           context=context.replace('</body>','')
           self.src=context
           self.save()
           return {"result":True}
        else:
           return{"result":False}

    @XBlock.json_handler 
    def student_submit(self, data, suffix=""):
        self.logger.info(data["answer"])
        student = self.runtime.get_real_user(self.runtime.anonymous_student_id)
        email = student.email
        name = student.first_name + " " + student.last_name
        username = student.username
        if name == " ":
            name = username
       
        t=datetime.datetime.now()+datetime.timedelta(hours=12)
        createtime=t.strftime('%Y-%m-%d:%H:%M:%S') 
        context={"path":self.path, "username":name, "email":email, "time":createtime, "answer":data["answer"]}
        ret=self.gitpost(self.root_token, self.git_host, self.git_port, self.repo_id, context)
        self.logger.info(ret)
        if ret==0:
           return{"result":True, "number":self.path}
        else:
           return{"result":False, "number":self.path}


    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("MyXBlock",
             """<vertical_demo>
                <myxblock/>
                <myxblock/>
                <myxblock/>
                </vertical_demo>
             """),
        ]



    def gitpost(self, token, host, port, teacher_id, context):
        self.logger.info(token)
        conn = None
        try:
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            email_hash=hashlib.new('md5', context["email"]).hexdigest()[-2:]
            self.logger.info(context)      
	    filepath=email_hash+'/'+context["username"]+'/'+context["path"].replace('html', 'md')
            value= urllib.urlencode({'file_path':filepath, 'branch_name':'master', 'content':context, 'commit_message':'submit infos'})
            id =teacher_id

            url1="/api/v3/projects/%d/repository/files?private_token=%s" %(id,token)
            self.logger.info(host)
            
            
            conn = httplib.HTTPConnection(host, port, timeout=30)
            conn.request("POST", url1, value, headers)
            res1=conn.getresponse()
                        
            if res1.status==200 or res1.status==201:
                 self.logger.info("commit success")
                 self.logger.info(res1.status)
                 return 0

            if res1.status==400 and json.loads(res1.read())["message"]=='Your changes could not be committed, because file with such name exists':
                 conn.close()

                 url2="/api/v3/projects/%d/repository/files?private_token=%s&&file_path=%s&&ref=master" %(id, token, filepath)
                 params=urllib.urlencode({}) 
                 conn = httplib.HTTPConnection(host, port, timeout=30)
                 conn.request("GET", url2, params, headers) 
                 res1=conn.getresponse()
                 
                 if res1.status ==200:
                    prevresult= base64.b64decode(json.loads(res1.read())["content"])
                    #print prevresult
                    conn.close()
                    newresult=prevresult+'\n'+json.dumps(context)
                    
                    newvalue=urllib.urlencode({'file_path':filepath, 'branch_name':'master', 'content':newresult, 'commit_message':'again submit infos'})
                    conn = httplib.HTTPConnection(host, port, timeout=30)
                    conn.request("PUT", url1, newvalue, headers)
                    if conn.getresponse().status==200:
                        self.logger.info("again success")
                    conn.close()
                    return 0
            return 1
        except Exception, e:
	  self.logger.info(e)
          return 1
