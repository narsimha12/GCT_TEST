import os
import cgi
import traceback
import json
import jinja2
import webapp2
import logging
import csv
import datetime
import math
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from pprint import pprint
from google.appengine.api import mail
from submit import Response,User,TestDetails,Randomize



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
ADMIN_USER_IDS=['narsimha.msit@gmail.com','ram@taramt.com','pg@taramt.com','ensreen@gmail.com','pendemdivya33@gmail.com']; 
a1_start=101;a1_end=301;a2_start=301;a2_end=401;a3_start=401;a3_end=601;a4_start=601;a4_end=701;
a5_start=701;a5_end=801;e1_start=801;e1_end=1201;e2_start=1201;e2_end=1601;e3_start=1601;e3_end=1701;
e4_start=1701;e4_end=1801;t1_start=1801;t1_end=2201;t2_start=2201;t2_end=2601;
#a1_start=101;a1_end=201;a2_start=201;a2_end=301;a3_start=301;a3_end=401;a4_start=401;a4_end=501;
#a5_start=501;a5_end=601;e1_start=601;e1_end=701;e2_start=701;e2_end=801;e3_start=801;e3_end=901;
#e4_start=901;e4_end=1001;t1_start=1001;t1_end=1101;t2_start=1101;t2_end=1201;
def getAllQuestions():
    json_temp=json.loads(open('QuestionBank_template.json').read())
    for key in json_temp:
        if  key == "section":
            section=json_temp[key]
            for s in section:
                for key in s:
                    if key == "subsection":
                        for subs in s[key]:
                            name=subs["name"]
                            types=subs["types"]
                            #print name
                            if name == "E2-Listening":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                video_list=json_subs["videoArray"]
                                subs["LRArray"]=video_list
                            if types =="question" or types =="record":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                qns_list=json_subs["questions"];
                                subs["questions"]=qns_list
                            if types == "passage":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                psglist=json_subs["passageArray"]
                                subs["LRArray"]=psglist
                            if types =="essay":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                qns_list=json_subs["questions"];
                                subs["questions"]=qns_list
                            if name == "T2-Listening":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                video_list=json_subs["videoArray"]
                                subs["LRArray"]=video_list
    #ss=json.dumps(json_temp)
    return json_temp
def getQuestionPaper(qid_list):
    
    json_temp=json.loads(open('QP_template.json').read())
    #print qid_list
    i=0;j=0;k=0;l=0;m=0;n=0;p=0;q=0;r=0;s=0;t=0
    for qid in qid_list:
        qid=int(qid)
        if qid in range(a1_start,a1_end):
              a1_sentjson=json.loads(open('A1-Sentences.json').read())
              for key in a1_sentjson["questions"]:
                    logging.error("questions with sno")
                    print(key["id"])
                    if int(key["id"]) == qid:
                          #print key
                          json_temp["section"][0]["subsection"][0]["questions"].append(key)
                          json_temp["section"][0]["subsection"][0]["questions"][i]["serialno"] = qid_list[qid]
                          i +=1
        if qid in range(a2_start,a2_end):
              a2_readjson=json.loads(open('A2-Reading.json').read())
              for key in a2_readjson["passageArray"]:
                    pid=key["questions"][0]["id"]
                    if int(pid) == qid:
                          json_temp["section"][0]["subsection"][1]["passage"]=key["passage"]
                          json_temp["section"][0]["subsection"][1]["questions"]=key["questions"]
                          json_temp["section"][0]["subsection"][1]["questions"][0]["serialno"] = qid_list[qid]
        if qid in range(a3_start,a3_end):
              a3_numjson=json.loads(open('A3-Numerical.json').read())
              for key in a3_numjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][0]["subsection"][2]["questions"].append(key)
                          json_temp["section"][0]["subsection"][2]["questions"][j]["serialno"] = qid_list[qid]
                          j +=1
        if qid in range(a4_start,a4_end):
              a4_reasjson=json.loads(open('A4-Reasoning.json').read())
              for key in a4_reasjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][0]["subsection"][3]["questions"].append(key)
                          json_temp["section"][0]["subsection"][3]["questions"][k]["serialno"] = qid_list[qid]
                          k +=1
        if qid in range(a5_start,a5_end):
              a5_essayjson=json.loads(open('A5-Composition.json').read())
              for key in a5_essayjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][0]["subsection"][4]["questions"].append(key)
                          json_temp["section"][0]["subsection"][4]["questions"][l]["serialno"] = qid_list[qid]
                          l += 1
        if qid in range(e1_start,e1_end):
              e1_readjson=json.loads(open('E1-Reading.json').read())
              for key in e1_readjson["passageArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][1]["subsection"][0]["passage"]=key["passage"]
                                json_temp["section"][1]["subsection"][0]["questions"].append(qn)
                                json_temp["section"][1]["subsection"][0]["questions"][m]["serialno"] = qid_list[qid]
                                m +=1
        if qid in range(e2_start,e2_end):
              e2_lsnjson=json.loads(open('E2-Listening.json').read())
              for key in e2_lsnjson["videoArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][1]["subsection"][1]["link"]=key["link"]
                                json_temp["section"][1]["subsection"][1]["questions"].append(qn)
                                json_temp["section"][1]["subsection"][1]["questions"][n]["serialno"] = qid_list[qid]
                                n +=1
        if qid in range(e3_start,e3_end):
              e3_spkjson=json.loads(open('E3-Speaking.json').read())
              for key in e3_spkjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][1]["subsection"][2]["questions"].append(key)
                          json_temp["section"][1]["subsection"][2]["questions"][p]["serialno"] = qid_list[qid]
                          p += 1
        if qid in range(e4_start,e4_end):
              e4_wrtjson=json.loads(open('E4-Writing.json').read())
              for key in e4_wrtjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][1]["subsection"][3]["questions"].append(key)
                          json_temp["section"][1]["subsection"][3]["questions"][q]["serialno"] = qid_list[qid]
                          q += 1
        if qid in range(t1_start,t1_end):
              t1_readjson=json.loads(open('T1-Reading.json').read())
              for key in t1_readjson["passageArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][2]["subsection"][0]["passage"]=key["passage"]
                                json_temp["section"][2]["subsection"][0]["questions"].append(qn)
                                json_temp["section"][2]["subsection"][0]["questions"][r]["serialno"] = qid_list[qid]
                                r += 1
        if qid in range(t2_start,t2_end):
              t2_lsnjson=json.loads(open('T2-Listening.json').read())
              for key in t2_lsnjson["videoArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][2]["subsection"][1]["link"]=key["link"]
                                json_temp["section"][2]["subsection"][1]["questions"].append(qn)
                                json_temp["section"][2]["subsection"][1]["questions"][s]["serialno"] = qid_list[qid]
                                s += 1
    #ss=json.dumps(json_temp)
    return json_temp
class RankEntity(ndb.Model):
  emailid=ndb.StringProperty(indexed=True)
  score=ndb.IntegerProperty(indexed=True)
  restime=ndb.IntegerProperty(indexed=True)
  aptitudeScore=ndb.IntegerProperty(indexed=True)
  englishScore=ndb.IntegerProperty(indexed=True)
  teluguScore=ndb.IntegerProperty(indexed=True)
  aptituderestime=ndb.IntegerProperty(indexed=True)
  englishrestime=ndb.IntegerProperty(indexed=True)
  telugurestime=ndb.IntegerProperty(indexed=True)
class Invities(ndb.Model):
  """model for storing invited users"""
  emailid=ndb.StringProperty(indexed=True)
  status=ndb.StringProperty(indexed=True)

class checklogin(webapp2.RequestHandler):
    """ handles authentication and redirects to quiz page """
    def get(self):
      user = users.get_current_user()
      if user is None:
        login_url = users.create_login_url(self.request.path)
        self.redirect(login_url)
        return
      else:
        if user.email() in ADMIN_USER_IDS:
          template= JINJA_ENVIRONMENT.get_template('admin.html')
          self.response.write(template.render())
        else:
          users.create_logout_url('/')
          login_url = users.create_login_url(self.request.path)
          #self.redirect(login_url)
          self.response.write("<center><h3><font color='red'>Invalid Admin Credentials</font></h3><h3>Please <a href='%s'>Login</a> Again</h3></center>"% login_url);
class ViewQB(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user is None:
      login_url = users.create_login_url(self.request.path)
      self.redirect(login_url)
      return
    else:
      template = JINJA_ENVIRONMENT.get_template('qb_page.html')
      self.response.write(template.render())

class Home(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user is None:
      login_url = users.create_login_url(self.request.path)
      self.redirect(login_url)
      return
    else:
      if user.email() in ADMIN_USER_IDS:
        template_values = {'home':True}
        template= JINJA_ENVIRONMENT.get_template('admin.html')
        self.response.write(template.render(template_values))
      else:
        users.create_logout_url('/')
        login_url = users.create_login_url(self.request.path)
        #self.redirect(login_url)
        self.response.write("<center><h3><font color='red'>Invalid Admin Credentials</font></h3><h3>Please <a href='%s'>Login</a> Again</h3></center>"% login_url);
class AdminHome(webapp2.RequestHandler):
  def  get(self):
    user = users.get_current_user()
    if user is None:
      login_url = users.create_login_url(self.request.path)
      self.redirect(login_url)
      return
    else:
      if user.email() in ADMIN_USER_IDS:
        userslist={};
        q1= TestDetails.query();
        q1.fetch();
        count=0;
        for data in q1:
          lcenter=data.learningcenter;
          if not userslist.has_key(lcenter):
            count=1;
            userslist[lcenter]=count;
          else:
            count=int(userslist[lcenter]);
            userslist[lcenter]=count+1;
        template_values = {'tests':userslist}
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        self.response.write(template.render(template_values))
      else:
        users.create_logout_url('/')
        login_url = users.create_login_url(self.request.path)
        #self.redirect(login_url)
        self.response.write("<center><h3><font color='red'>Invalid Admin Credentials</font></h3><h3>Please <a href='%s'>Login</a> Again</h3></center>"% login_url);
class QuizDetails(webapp2.RequestHandler):
  def  get(self,lcenter):
    userslist=[];
    ranklist=[];
    q1= TestDetails.query(TestDetails.learningcenter == lcenter)
    q1.fetch();
    
    for users in q1:
      score_dict = {}
      q2= Response.query(Response.useremailid.emailid==users.email).order(Response.serialno,-Response.time)
      q2.fetch()
      aptitudescore=0;
      englishtestscore=0;
      telugutestscore=0;
      aptitude_response_time=0;
      english_response_time=0;
      telugu_response_time=0;
      total_score=0;
      responseTime=0;
      counter=0;
      for record in q2:
        if not record.currentQuestion == None:
          if not record.currentQuestion in score_dict:
            score_dict[record.currentQuestion] = (record.q_score,(record.responsetime/60))
      
      for key in range(a1_start,a5_end):
        key = str(key)
        if key in score_dict:
          aptitudescore += score_dict[key][0]
          aptitude_response_time += score_dict[key][1]

      for key in range(e1_start,e4_end):
        key = str(key)
        if key in score_dict:
          englishtestscore += score_dict[key][0]
          english_response_time += score_dict[key][1]

      for key in range(t1_start,t2_end):
        key = str(key)
        if key in score_dict:
          telugutestscore += score_dict[key][0]
          telugu_response_time += score_dict[key][1]
      print score_dict
      logging.error("dictionary values")
      total_score = aptitudescore + englishtestscore + telugutestscore;
      responseTime = aptitude_response_time + telugu_response_time + english_response_time
      rankent=RankEntity(emailid=users.email, score=total_score,
                          restime=int(responseTime),aptitudeScore=aptitudescore,
                          aptituderestime=int(aptitude_response_time),
                          englishScore=englishtestscore,
                          englishrestime=int(english_response_time),
                          teluguScore=telugutestscore,telugurestime=int(telugu_response_time))
      ranklist.append(rankent);
    template_values = {'userslist':ranklist}
    template = JINJA_ENVIRONMENT.get_template('admin.html')
    self.response.write(template.render(template_values))

class UserQuizReport(webapp2.RequestHandler):
  def  get(self,umailid):
          score_dict={}
          q1= Response.query(ndb.AND(Response.useremailid.emailid==umailid,Response.serialno!=None)).order(Response.serialno,-Response.time)
          q1.fetch()
          quizdata=[]
          qid_list={}
          score=0
          for q in q1:
          	if not q.currentQuestion == None:
	          	if not q.currentQuestion in score_dict:
		            score_dict[q.currentQuestion] = (q.q_score)
		            resp=Response(serialno=q.serialno,useremailid=User(emailid=umailid,name=""),currentQuestion=q.currentQuestion,submittedans=q.submittedans,responsetime=round(q.responsetime/10,1),q_status=q.q_status,q_score=q.q_score)
		            quizdata.append(resp);
		            if not q.q_score==None:
		              score += q.q_score;
          for respdata in quizdata:
            qid_list[int(respdata.currentQuestion)] = respdata.serialno
          json_data=getQuestionPaper(qid_list)
          questionslist=[];
          correctAnslist=[];
          for currentSection in json_data["section"]:
              for currentSubsection in currentSection["subsection"]:
                    logging.error("This is an error message that will show in the console")
                    for q in currentSubsection["questions"]:
                      questionName=q["question"];
                      questionslist.append(questionName);
                      type=currentSubsection["types"]
                      if (type=="essay" or type=="record"):
                        correctAnslist.append("");
                      else:
                        for option in q["options"]:
                          if option[0]== "=":
                            correctAns=option[1:len(option)];
                            correctAnslist.append(correctAns);
          template_values = {
                'quizdata': quizdata,
                'score':score,
                'questionslist':questionslist,
                'correctAnslist':correctAnslist,
                'useremailid':umailid,
                
                }
          template = JINJA_ENVIRONMENT.get_template('admin.html')
          self.response.write(template.render(template_values))

class DownloadCSV(webapp2.RequestHandler):
  def get(self,filename):
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.headers['Content-Disposition'] = 'attachment; filename='+filename+'_report.csv'
    writer = csv.writer(self.response.out)
    #writer.writerow(['UserEmailID', 'Aptitude Score','Aptitude Response Time','English Comprehension Score','English Comprehension Response Time','Telugu Comprehension Score','Telugu Comprehension Response Time','Total Score','Total Response Time','Rank' ]);
    #writer.writerow(['UserEmailID', 'EnS','EnS-RT','Num','Num-RT','RC','RC-RT','LC','LC-RT','Te','Te-RT','Score','RT','Rank' ])
    writer.writerow(['UserEmailID', 'Sentences/10','Memo/1','Num/5','Reasoning/2','Eng-RC/4','Eng-LC/4','Te-RC/4','Te-LC/4','TotalScore'])
    userslist=[];
    ranklist=[];
    f = open(filename+".csv")
    for line in f:
      rec = line.strip().split(",")
      userslist.append(rec[0])
    f.close();
   
    for users in userslist:
      score_dict = {}
      q2= Response.query(Response.useremailid.emailid==users).order(Response.serialno,-Response.time)
      q2.fetch()
      Score=0;
      RT=0;
      EnS=0;
      EnS_RT=0;
      Num=0;
      Num_RT=0;
      RC=0;
      RC_RT=0;
      LC=0;
      LC_RT=0;
      Te=0;
      Te_RT=0;
      memo=0;
      memo_RT=0;
      reas=0;reas_RT=0;
      Te_lc=0;Te_lc_RT=0;
      counter=0;
      for record in q2:
        if not record.currentQuestion == None:
          if not record.currentQuestion in score_dict:
            score_dict[record.currentQuestion] = (record.q_score,record.responsetime)
      
      for key in range(a1_start,a1_end):
        key = str(key)
        if key in score_dict:
          EnS += score_dict[key][0]
          EnS_RT += score_dict[key][1]
      for key in range(a2_start,a2_end):
        key = str(key)
        if key in score_dict:
          memo += score_dict[key][0]
          memo_RT += score_dict[key][1]
      for key in range(a3_start,a3_end):
        key = str(key)
        if key in score_dict:
          Num += score_dict[key][0]
          Num_RT += score_dict[key][1]
      for key in range(a4_start,a4_end):
        key = str(key)
        if key in score_dict:
          reas += score_dict[key][0]
          reas_RT += score_dict[key][1]

      for key in range(e1_start,e1_end):
        key = str(key)
        if key in score_dict:
          RC += score_dict[key][0]
          RC_RT += score_dict[key][1]
      
      for key in range(e2_start,e2_end):
        key = str(key)
        if key in score_dict:
          LC += score_dict[key][0]
          LC_RT += score_dict[key][1]
      for key in range(t1_start,t1_end):
        key = str(key)
        if key in score_dict:
          Te += score_dict[key][0]
          Te_RT += score_dict[key][1]
      for key in range(t2_start,t2_end):
        key = str(key)
        if key in score_dict:
          Te_lc += score_dict[key][0]
          Te_lc_RT += score_dict[key][1]
      print score_dict
      logging.error("dictionary values")
      Score = EnS + memo+Num +reas+ RC + LC + Te+Te_lc;
      RT = EnS_RT +memo_RT+ Num_RT +reas_RT +RC_RT + LC_RT + Te_RT+Te_lc_RT;
      row=[users.encode('utf-8'),EnS,memo,Num,reas,RC,LC,Te,Te_lc,Score]
      writer.writerow(row);
class GetEssay(webapp2.RequestHandler):
  def get(self,filename):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.headers['Content-Disposition'] = 'attachment; filename='+filename+'_Essay.txt'
    userslist=[];
    f = open(filename+".csv")
    for line in f:
      rec = line.strip().split(",")
      userslist.append(rec[0])
    f.close();
    
    user_qn_dict={}
    for user in userslist:
    	q1=Randomize.query(Randomize.user1==user).fetch();
    	qn1=0;qn2=0;
    	for key in q1:
    		qno=int(key.qno);
    		if qno in range(a5_start,a5_end):
    			qn1=qno
    		if qno in range(e4_start,e4_end):
    			qn2=qno
    	user_qn_dict[user]=(qn1,qn2)
    count=0;
    for key,value in user_qn_dict.items():
    	count += 1
    	q2=Response.query(ndb.AND(Response.useremailid.emailid==key,ndb.OR(Response.serialno==value[0],Response.serialno==value[1]))).order(Response.serialno,-Response.time)
    	q2.fetch();
    	qid_list=[]
    	self.response.write("\n"+str(count)+" :- "+key+"\n");
    	self.response.write("========================================================\n");
    	for data in q2:
    		print data.serialno
    		logging.error("testing msg")
    		if not data.serialno in qid_list:
    			qid_list.append(data.serialno);
    			self.response.write(data.submittedans+"\n");
    			self.response.write("--------------------------------------------------------\n");      
class getMeanStd(webapp2.RequestHandler):
	def get(self,filename):
		self.response.headers['Content-Type'] = 'text/csv'
		self.response.headers['Content-Disposition'] = 'attachment; filename='+filename+'_Aptitude_Mean_sd.csv'
		writer = csv.writer(self.response.out)
		writer.writerow(['Student Mail id', 'Aptitude score/18','TOEFL score/8','Aptitude_totalTime','TOEFL_totalTime','Aptitude_correct_Ans_time','TOEFL_correct_Ans_time'])
		userslist=[];
		users_total_score=[];
		f = open(filename+".csv")
		for line in f:
			rec = line.strip().split(",")
			userslist.append(rec[0])
		f.close();
		usercount=0
		for user in userslist:
			score_dict = {}
			q2= Response.query(Response.useremailid.emailid==user).order(Response.serialno,-Response.time)
			q2.fetch()
			apt_score=0;
			toefl_score=0;
			apt_rt=0;
			toefl_rt=0;
			apt_correct_rt=0;
			toefl_correct_rt=0;
			total_score=0;
			for record in q2:
				if not record.currentQuestion == None:
					if not record.currentQuestion in score_dict:
						score_dict[record.currentQuestion] = (record.q_score,record.responsetime)
			for key in range(a1_start,a5_end):
				key = str(key)
				if key in score_dict:
					apt_score += score_dict[key][0]
					apt_rt +=score_dict[key][1]
					if score_dict[key][0] == 1:
						apt_correct_rt += score_dict[key][1]
			for key in range(e1_start,e4_end):
				key = str(key)
				if key in score_dict:
					toefl_score += score_dict[key][0]
					toefl_rt += score_dict[key][1]
					if score_dict[key][0] == 1:
						toefl_correct_rt += score_dict[key][1]
			total_score = apt_score+toefl_score;
			users_total_score.append(total_score);
			if not apt_rt == 0:
				usercount +=1;
				row=[user,apt_score,toefl_score,round(apt_rt,1),round(toefl_rt,1),round(apt_correct_rt,1),round(toefl_correct_rt,1)];
				writer.writerow(row);
		final_score=0;
		for sc in users_total_score:
			final_score += sc
		#num=len(userslist);
		mean = float(final_score)/float(usercount);
		square_sum=0
		for uscore in users_total_score:
			if not uscore == 0:
				square_sum +=(uscore-mean)**2
		stdv=math.sqrt(square_sum/(usercount-1))
		writer.writerow(['','']);
		writer.writerow(['MEAN OF TOTAL SCORE :', mean]);
		writer.writerow(['STANDARD DEVIATION  :',stdv]);
class getMeanStd_Apti(webapp2.RequestHandler):
	def get(self,filename):
		self.response.headers['Content-Type'] = 'text/csv'
		self.response.headers['Content-Disposition'] = 'attachment; filename='+filename+'_Aptitude_Meansd.csv'
		writer = csv.writer(self.response.out)
		writer.writerow(['Student Mail id', 'Aptitude score/18','Totaltime','Time taken for correct_Answers'])
		userslist=[];
		users_total_score=[];
		users_total_rt=[];
		data_dict={}
		f = open(filename+".csv")
		for line in f:
			rec = line.strip().split(",")
			userslist.append(rec[0])
		f.close();
		usercount=0
		for user in userslist:
			score_dict = {}
			q2= Response.query(Response.useremailid.emailid==user).order(Response.serialno,-Response.time)
			q2.fetch()
			apt_score=0;
			apt_rt=0;
			apt_correct_rt=0;
			total_score=0;
			for record in q2:
				if not record.currentQuestion == None:
					if not record.currentQuestion in score_dict:
						score_dict[record.currentQuestion] = (record.q_score,record.responsetime)
			for key in range(a1_start,a4_end):
				key = str(key)
				if key in score_dict:
					apt_score += score_dict[key][0]
					apt_rt +=score_dict[key][1]
					if score_dict[key][0] == 1:
						apt_correct_rt += score_dict[key][1]
			#if apt_score > 9:
			users_total_score.append(apt_score);
			users_total_rt.append(apt_correct_rt/60);
			if not apt_rt == 0:
				#if apt_score > 9:
				usercount +=1;
				data_dict[user]=(apt_score,apt_rt/60,apt_correct_rt/60);
				row=[user,apt_score,apt_rt/60,apt_correct_rt/60];
				writer.writerow(row);
		final_score=0;
		if usercount>0:
			for sc in users_total_score:
				final_score += sc
			#num=len(userslist);
			mean = float(final_score)/float(usercount);
			square_sum=0
			for uscore in users_total_score:
				#if uscore > 9:
				square_sum +=(uscore-mean)**2
			stdv=math.sqrt(square_sum/(usercount-1))
			writer.writerow(['','']);
			writer.writerow(['MEAN OF TOTAL SCORE :', mean]);
			writer.writerow(['STANDARD DEVIATION  :',stdv]);

			final_rt=0;
			for r in users_total_rt:
				final_rt += r;
			mean1 = float(final_rt)/float(usercount);
			square_sum1=0
			for uscore in users_total_rt:
				square_sum1 +=(uscore-mean1)**2
			stdv1=math.sqrt(square_sum1/(usercount-1))
			writer.writerow(['MEAN OF TIME TAKEN FOR CORRECT ANSWERS :', mean1]);
			writer.writerow(['STANDARD DEVIATION FOR CORRECT ANSWERS RT :',stdv1]);

class getMeanStd_toefl(webapp2.RequestHandler):
	def get(self,filename):
		self.response.headers['Content-Type'] = 'text/csv'
		self.response.headers['Content-Disposition'] = 'attachment; filename='+filename+'_TOEFL_Meansd.csv'
		writer = csv.writer(self.response.out)
		writer.writerow(['Student Mail id', 'TOEFL score/8','Totaltime','Time taken for correct_Answers'])
		userslist=[];
		users_total_score=[];
		users_total_rt=[];
		f = open(filename+".csv")
		for line in f:
			rec = line.strip().split(",")
			userslist.append(rec[0])
		f.close();
		usercount=0
		for user in userslist:
			score_dict = {}
			q2= Response.query(Response.useremailid.emailid==user).order(Response.serialno,-Response.time)
			q2.fetch()
			tfl_score=0;
			tfl_rt=0;
			tfl_correct_rt=0;
			total_score=0;
			for record in q2:
				if not record.currentQuestion == None:
					if not record.currentQuestion in score_dict:
						score_dict[record.currentQuestion] = (record.q_score,record.responsetime)
			for key in range(e1_start,e2_end):
				key = str(key)
				if key in score_dict:
					tfl_score += score_dict[key][0]
					tfl_rt +=score_dict[key][1]
					if score_dict[key][0] == 1:
						tfl_correct_rt += score_dict[key][1]

			users_total_score.append(tfl_score);
			users_total_rt.append(tfl_correct_rt/60);
			if not tfl_correct_rt == 0:
				usercount +=1;
				row=[user,tfl_score,tfl_rt/60,tfl_correct_rt/60];
				writer.writerow(row);
		final_score=0;
		for sc in users_total_score:
			final_score += sc
		#num=len(userslist);
		mean = float(final_score)/float(usercount);

		final_rt=0;
		for r in users_total_rt:
			final_rt += r
		mean1 = float(final_rt)/float(usercount);
		square_sum=0
		for uscore in users_total_score:
			if not uscore == 0:
				square_sum +=(uscore-mean)**2
		stdv=math.sqrt(square_sum/(usercount-1))
		square_sum1=0
		for uscore in users_total_rt:
			if not uscore == 0:
				square_sum1 +=(uscore-mean1)**2
		stdv1=math.sqrt(square_sum1/(usercount-1))
		writer.writerow(['','']);
		writer.writerow(['MEAN OF TOTAL SCORE :', mean]);
		writer.writerow(['STANDARD DEVIATION  :',stdv]);
		writer.writerow(['MEAN OF TIME TAKEN FOR CORRECT ANSWERS :', mean1]);
		writer.writerow(['STANDARD DEVIATION FOR CORRECT ANSWERS RT :',stdv1]);
class getMeanStd_telugu(webapp2.RequestHandler):
  def get(self,filename):
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.headers['Content-Disposition'] = 'attachment; filename='+filename+'_TELUGU_Meansd.csv'
    writer = csv.writer(self.response.out)
    writer.writerow(['Student Mail id', 'Telugu score/8','Totaltime','Time taken for correct_Answers'])
    userslist=[];
    users_total_score=[];
    users_total_rt=[];
    f = open(filename+".csv")
    for line in f:
      rec = line.strip().split(",")
      userslist.append(rec[0])
    f.close();
    usercount=0
    for user in userslist:
      score_dict = {}
      q2= Response.query(Response.useremailid.emailid==user).order(Response.serialno,-Response.time)
      q2.fetch()
      tfl_score=0;
      tfl_rt=0;
      tfl_correct_rt=0;
      total_score=0;
      for record in q2:
        if not record.currentQuestion == None:
          if not record.currentQuestion in score_dict:
            score_dict[record.currentQuestion] = (record.q_score,record.responsetime)
      for key in range(t1_start,t2_end):
        key = str(key)
        if key in score_dict:
          tfl_score += score_dict[key][0]
          tfl_rt +=score_dict[key][1]
          if score_dict[key][0] == 1:
            tfl_correct_rt += score_dict[key][1]

      users_total_score.append(tfl_score);
      users_total_rt.append(tfl_correct_rt/60);
      if not tfl_correct_rt == 0:
        usercount +=1;
        row=[user,tfl_score,tfl_rt/60,tfl_correct_rt/60];
        writer.writerow(row);
    final_score=0;
    for sc in users_total_score:
      final_score += sc
    #num=len(userslist);
    mean = float(final_score)/float(usercount);

    final_rt=0;
    for r in users_total_rt:
      final_rt += r
    mean1 = float(final_rt)/float(usercount);
    square_sum=0
    for uscore in users_total_score:
      if not uscore == 0:
        square_sum +=(uscore-mean)**2
    stdv=math.sqrt(square_sum/(usercount-1))
    square_sum1=0
    for uscore in users_total_rt:
      if not uscore == 0:
        square_sum1 +=(uscore-mean1)**2
    stdv1=math.sqrt(square_sum1/(usercount-1))
    writer.writerow(['','']);
    writer.writerow(['MEAN OF TOTAL SCORE :', mean]);
    writer.writerow(['STANDARD DEVIATION  :',stdv]);
    writer.writerow(['MEAN OF TIME TAKEN FOR CORRECT ANSWERS :', mean1]);
    writer.writerow(['STANDARD DEVIATION FOR CORRECT ANSWERS RT :',stdv1]);

class get_QB(webapp2.RequestHandler):
  def post(self):
    json_data=getAllQuestions()
    print json_data
    logging.error("question data")
    ss=json.dumps(json_data)
    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
    self.response.write(ss)
class getAudiolinks(webapp2.RequestHandler):
  def get(self,learningcenter):
    userid_list=[]
    audio_dict={}
    td = TestDetails.query(TestDetails.learningcenter==learningcenter)
    td.fetch()
    for record in td:
      userid_list.append(record.email);
    for user in userid_list:
      q2= Response.query(Response.useremailid.emailid==user).order(Response.serialno,-Response.time)
      q2.fetch()
      for resdata in q2:
        if not resdata.currentQuestion == None:
          qno=int(resdata.currentQuestion)
          if qno in range(e3_start,e3_end):
            audio_dict[user]=resdata.submittedans
    template_values = {
                'audiodata': audio_dict,
                }
    template = JINJA_ENVIRONMENT.get_template('admin.html')
    self.response.write(template.render(template_values))
application = webapp2.WSGIApplication([
    ('/admin/?',Home),
    ('/admin/adminhome',AdminHome),
    ('/admin/viewqb',ViewQB),
    ('/admin/quizdetails/([^/]+)?',QuizDetails),
    ('/admin/userquizreport/([^/]+)?',UserQuizReport), 
    ('/admin/downloadcsv/([^/]+)?',DownloadCSV),
    ('/admin/getessay/([^/]+)?',GetEssay),
    ('/admin/getmeanstd/([^/]+)?',getMeanStd),
    ('/admin/getmeanstd_apti/([^/]+)?',getMeanStd_Apti),
    ('/admin/getmeanstd_toefl/([^/]+)?',getMeanStd_toefl),
    ('/admin/getMeanStd_telugu/([^/]+)?',getMeanStd_telugu),
    ('/admin/get_qb',get_QB),
    ('/admin/getaudiolinks/([^/]+)?',getAudiolinks),
       ], debug=True)