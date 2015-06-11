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
# a1_start=101;a1_end=301;a2_start=301;a2_end=401;a3_start=401;a3_end=601;a4_start=601;a4_end=701;
# a5_start=701;a5_end=801;e1_start=801;e1_end=1201;e2_start=1201;e2_end=1601;e3_start=1601;e3_end=1701;
# e4_start=1701;e4_end=1801;t1_start=1801;t1_end=2201;t2_start=2201;t2_end=2601;
a1_start=101;a1_end=201;a2_start=201;a2_end=301;a3_start=301;a3_end=401;a4_start=401;a4_end=501;
a5_start=501;a5_end=601;e1_start=601;e1_end=701;e2_start=701;e2_end=801;e3_start=801;e3_end=901;
e4_start=901;e4_end=1001;t1_start=1001;t1_end=1101;t2_start=1101;t2_end=1201;
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
                                subs["videoArray"]=video_list
                            if types =="question" or types =="record":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                qns_list=json_subs["questions"];
                                subs["questions"]=qns_list
                            if types == "passage":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                psglist=json_subs["passageArray"]
                                subs["passageArray"]=psglist
                            if types =="essay":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                qns_list=json_subs["questions"];
                                subs["questions"]=qns_list
                            if name == "T2-Listening":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                video_list=json_subs["videoArray"]
                                subs["videoArray"]=video_list
    #ss=json.dumps(json_temp)
    return json_temp
class Invities(ndb.Model):
  """model for storing invited users"""
  emailid=ndb.StringProperty(indexed=True)
  status=ndb.StringProperty(indexed=True)

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
class RankEntity1(ndb.Model):
  emailid=ndb.StringProperty(indexed=True)
  Score=ndb.IntegerProperty(indexed=True)
  RT=ndb.IntegerProperty(indexed=True)
  EnS=ndb.IntegerProperty(indexed=True)
  EnS_RT=ndb.IntegerProperty(indexed=True)
  Num=ndb.IntegerProperty(indexed=True)
  Num_RT=ndb.IntegerProperty(indexed=True)
  RC=ndb.IntegerProperty(indexed=True)
  RC_RT=ndb.IntegerProperty(indexed=True)
  LC=ndb.IntegerProperty(indexed=True)
  LC_RT=ndb.IntegerProperty(indexed=True)
  Te=ndb.IntegerProperty(indexed=True)
  Te_RT=ndb.IntegerProperty(indexed=True)

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
          template= JINJA_ENVIRONMENT.get_template('qb_page.html')
          self.response.write(template.render())
        else:
          #Response(useremailid=User(emailid=user.email(),name=user.nickname())).put()
          template= JINJA_ENVIRONMENT.get_template('qb_page.html')
          self.response.write(template.render())

class Home(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user is None:
      login_url = users.create_login_url(self.request.path)
      self.redirect(login_url)
      return
    else:
      template_values = {'home':True}
      #template = JINJA_ENVIRONMENT.get_template('admin.html')
      template = JINJA_ENVIRONMENT.get_template('qb_page.html')
      self.response.write(template.render(template_values))


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
          dt=data.teststime;
          dateval=dt.date()
          if not userslist.has_key(dateval):
            count=1;
            userslist[dateval]=count;
          else:
            count=int(userslist[dateval]);
            userslist[dateval]=count+1;
        template_values = {'tests':userslist}
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        self.response.write(template.render(template_values))
      else:
        users.create_logout_url('/')
        login_url = users.create_login_url(self.request.path)
        #self.redirect(login_url)
        self.response.write("<center><h3><font color='red'>Invalid Admin Credentials</font></h3><h3>Please <a href='%s'>Login</a> Again</h3></center>"% login_url);
class QuizDetails(webapp2.RequestHandler):
  def  get(self,dateval):
    userslist=[];
    ranklist=[];
    date=datetime.datetime.strptime(dateval,"%Y-%m-%d")
    year=int(date.year);
    month=int(date.month);
    day=int(date.day);
    startdatetime=datetime.datetime(year,month,day, 0, 0, 0);
    enddatetime=datetime.datetime(year,month,day,23,59,59);
    q1= TestDetails.query(ndb.AND(TestDetails.teststime>startdatetime,TestDetails.teststime<enddatetime));
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
    
    n=len(ranklist);
    for j in range(0,n-1):
      Max=j
      for i in range(j+1,n):
        if(ranklist[i].score>ranklist[Max].score):
          Max=i;
        elif (ranklist[i].score==ranklist[Max].score):
          if(ranklist[i].restime<ranklist[Max].restime):
            Max=i;
      if(not Max==j):
        ranklist[j],ranklist[Max]=ranklist[Max],ranklist[j];
    template_values = {'userslist':ranklist,'dateval':dateval}
    template = JINJA_ENVIRONMENT.get_template('admin.html')
    self.response.write(template.render(template_values))

class UserQuizReport(webapp2.RequestHandler):
  def  get(self,umailid):
          score_dict={}
          q1= Response.query(ndb.AND(Response.useremailid.emailid==umailid,Response.serialno!=None)).order(Response.serialno,-Response.time)
          q1.fetch()
          quizdata=[]
          score=0
          for q in q1:
          	if not q.currentQuestion == None:
	          	if not q.currentQuestion in score_dict:
		            score_dict[q.currentQuestion] = (q.q_score)
		            resp=Response(serialno=q.serialno,useremailid=User(emailid=umailid,name=""),currentQuestion=q.currentQuestion,submittedans=q.submittedans,responsetime=round(q.responsetime/10,1),q_status=q.q_status,q_score=q.q_score)
		            quizdata.append(resp);
		            if not q.q_score==None:
		              score += q.q_score;
          json_data=json.loads(open('quizdata.json').read())
            #print(json_data )
            #logging.error("This is an error message that will show in the console")
            # finding the correct answer and updating the score
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
class DownloadCSV_User(webapp2.RequestHandler):
  def get(self,useremailid):
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.headers['Content-Disposition'] = 'attachment; filename='+useremailid+'_report.csv'
    writer = csv.writer(self.response.out)
    writer.writerow(['Question ID', 'Question','Score','Submitted Answer','Correct Answer','Response time' ])
    json_data=json.loads(open('quizdata.json').read())
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
    q1= Response.query(ndb.AND(Response.useremailid.emailid==useremailid,Response.serialno!=None)).order(Response.serialno,-Response.time)
    q1.fetch()
    score=0
    i=0;
    for q in q1:
      qname=questionslist[i];
      cans=correctAnslist[i];
      restime=round(q.responsetime/10,1);
      row=[i+1,qname.encode('utf-8'),q.q_score,q.submittedans.encode('utf-8'),cans.encode('utf-8'),restime]

      writer.writerow(row);
      if not q.q_score==None:
        score += q.q_score;
      i +=1;
# class DownloadCSV(webapp2.RequestHandler):
#   def get(self,dateval):
#     self.response.headers['Content-Type'] = 'text/csv'
#     self.response.headers['Content-Disposition'] = 'attachment; filename='+dateval+'_report.csv'
#     writer = csv.writer(self.response.out)
#     #writer.writerow(['UserEmailID', 'Aptitude Score','Aptitude Response Time','English Comprehension Score','English Comprehension Response Time','Telugu Comprehension Score','Telugu Comprehension Response Time','Total Score','Total Response Time','Rank' ]);
#     writer.writerow(['UserEmailID', 'EnS','EnS-RT','Num','Num-RT','RC','RC-RT','LC','LC-RT','Te','Te-RT','Score','RT','Rank' ])
#     userslist=[];
#     ranklist=[];
#     date=datetime.datetime.strptime(dateval,"%Y-%m-%d")
#     year=int(date.year);
#     month=int(date.month);
#     day=int(date.day);
#     startdatetime=datetime.datetime(year,month,day, 0, 0, 0);
#     enddatetime=datetime.datetime(year,month,day,23,59,59);
#     q1= TestDetails.query(ndb.AND(TestDetails.teststime>startdatetime,TestDetails.teststime<enddatetime));
#     q1.fetch();
   
#     for users in q1:
#       score_dict = {}
#       q2= Response.query(Response.useremailid.emailid==users.email).order(Response.serialno,-Response.time)
#       q2.fetch()
#       aptitudescore=0;
#       englishtestscore=0;
#       telugutestscore=0;
#       aptitude_response_time=0;
#       english_response_time=0;
#       telugu_response_time=0;
#       total_score=0;
#       responseTime=0;
#       counter=0;
#       for record in q2:
#         if not record.currentQuestion == None:
#           if not record.currentQuestion in score_dict:
#             score_dict[record.currentQuestion] = (record.q_score,record.responsetime)
      
#       for key in range(0,19):
#         key = str(key)
#         if key in score_dict:
#           aptitudescore += score_dict[key][0]
#           aptitude_response_time += score_dict[key][1]

#       for key in range(19,28):
#         key = str(key)
#         if key in score_dict:
#           englishtestscore += score_dict[key][0]
#           english_response_time += score_dict[key][1]

#       for key in range(28, 35):
#         key = str(key)
#         if key in score_dict:
#           telugutestscore += score_dict[key][0]
#           telugu_response_time += score_dict[key][1]
#       print score_dict
#       logging.error("dictionary values")
#       total_score = aptitudescore + englishtestscore + telugutestscore;
#       responseTime = aptitude_response_time + telugu_response_time + english_response_time
        
#       rankent=RankEntity(emailid=users.email, score=total_score,
#                           restime=int(round(responseTime)),aptitudeScore=aptitudescore,
#                           aptituderestime=int(round(aptitude_response_time)),
#                           englishScore=englishtestscore,
#                           englishrestime=int(round(english_response_time)),
#                           teluguScore=telugutestscore,telugurestime=int(round(telugu_response_time)))
#       ranklist.append(rankent);
#     n=len(ranklist);
#     for j in range(0,n-1):
#       Max=j
#       for i in range(j+1,n):
#         if(ranklist[i].score>ranklist[Max].score):
#           Max=i;
#         elif (ranklist[i].score==ranklist[Max].score):
#           if(ranklist[i].restime<ranklist[Max].restime):
#             Max=i;
#       if(not Max==j):
#         ranklist[j],ranklist[Max]=ranklist[Max],ranklist[j];
#     i=0;
#     for q in ranklist:
#       row=[q.emailid.encode('utf-8'),q.aptitudeScore,q.aptituderestime,q.englishScore,q.englishrestime,q.teluguScore,q.telugurestime,q.score,q.restime,i+1]
#       writer.writerow(row);
#       i +=1;
class SendInvites(webapp2.RequestHandler):
  def post(self):
    emails=self.request.get("mailids");
    msg=self.request.get("msg");
    message = mail.EmailMessage(sender="narsimha898@gmail.com",
                            subject="Test invitation")
    message.body = msg;
    mailids=emails.split(',');
    for email in mailids:
      message.to = email;
      invities = Invities(emailid=email, status="Invited")
      invities.put()
      message.send()

    self.response.write("<center><h2>The invitations are successfully sent</h2>");
    self.response.write("<center><h2>Click<a href='/admin/'>adminhome</a>to go to adminhome</h2>");
    
class SendInvitesView(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('sendinvites.html')
    self.response.write(template.render())
# class QuestionStatistics(webapp2.RequestHandler):
#   def get(self,dateval):
#       date=datetime.datetime.strptime(dateval,"%Y-%m-%d")
#       year=int(date.year);
#       month=int(date.month);
#       day=int(date.day);
#       startdatetime=datetime.datetime(year,month,day, 0, 0, 0);
#       enddatetime=datetime.datetime(year,month,day,23,59,59);
      
#       question_dict={}
#       correct_Ans_count=0
#       wrong_Ans_count=0
#       for qid in range(1,36):
#         q2= Response.query(ndb.AND(Response.time>startdatetime,Response.time<enddatetime),Response.serialno==qid).order(Response.serialno,-Response.time)
#         q2.fetch()
#         user_list =[]
#         for record in q2:
#           if not record.useremailid.emailid in user_list:
#             user_list.append(record.useremailid.emailid);
#             if record.serialno in question_dict:
#               if record.q_score==1:
#                 correct_Ans_count = question_dict[record.serialno][0]
#                 correct_Ans_count +=1
#               else:
#                 wrong_Ans_count= question_dict[record.serialno][1]
#                 wrong_Ans_count +=1
#               question_dict[record.serialno]=(correct_Ans_count,wrong_Ans_count)
#             else:
#               if record.q_score==1:
#                 correct_Ans_count =1
#                 wrong_Ans_count=0
#               else:
#                 correct_Ans_count=0
#                 wrong_Ans_count =1
#               question_dict[record.serialno]=(correct_Ans_count,wrong_Ans_count)
          
      
#       template_values = {'question_dict':question_dict}
#       template = JINJA_ENVIRONMENT.get_template('admin.html')
#       self.response.write(template.render(template_values))
class QuestionStatistics(webapp2.RequestHandler):
  def get(self,filename):
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.headers['Content-Disposition'] = 'attachment; filename='+filename+'_question_report.csv'
    writer = csv.writer(self.response.out)
    writer.writerow(['Question Id', 'Total Time','User_count','Mean','SD'])
    userslist=[]
    all_dict={}
    f = open(filename+".csv")
    for line in f:
      rec = line.strip().split(",")
      userslist.append(rec[0])
    f.close();
    for key in range(1,19):
    	total_restime=0
    	restime_list=[]
    	num = 0;
    	for eid in userslist:
    		q2= Response.query(ndb.AND(Response.useremailid.emailid==eid,Response.serialno==key)).order(Response.serialno,-Response.time)
    		q2.fetch()
    		for ls in q2:
    			if ls.q_score == 1:
    				num += 1;
    				total_restime +=(ls.responsetime/10);
    				restime_list.append(ls.responsetime/10);
    			break;
    	#num=len(restime_list);
    	if num > 0 :
    		mean=total_restime/num;
    		square_sum=0
    		for data in restime_list:
    			square_sum +=(data-mean)**2;
    		if num==1:
    			stdv=math.sqrt(square_sum/(num));
    		else:
    			stdv=math.sqrt(square_sum/(num-1));
    		writer.writerow([key,total_restime,num,mean,stdv]);
    	else:
    		writer.writerow([key,0,0,'N/A','N/A'])
	
class QuestionStatistics_Toefl(webapp2.RequestHandler):
	def get(self,filename):
		self.response.headers['Content-Type'] = 'text/csv'
		self.response.headers['Content-Disposition'] = 'attachment; filename='+filename+'_question_report_toefl.csv';
		writer = csv.writer(self.response.out)
		writer.writerow(['Question Id', 'Total Time','User_count','Mean','SD'])
		userslist=[]
		all_dict={}
		f = open(filename+".csv")
		for line in f:
			rec = line.strip().split(",")
			userslist.append(rec[0])
		f.close();
		for  key in range(20,28):
			total_restime=0
			restime_list=[]
			for eid in userslist:
				q3= Response.query(ndb.AND(Response.useremailid.emailid==eid,Response.serialno==key)).order(Response.serialno,-Response.time)
				q3.fetch(1)
				for ls in q3:
					if ls.q_score == 1:
						total_restime +=(ls.responsetime/10);
						restime_list.append((ls.responsetime)/10);
					break;
			num=len(restime_list);
			if num>0:
				mean=total_restime/num;
				square_sum=0
				for data in restime_list:
					square_sum +=(data-mean)**2;
				if num==1:
					stdv=math.sqrt(square_sum/num);
				else:
					stdv=math.sqrt(square_sum/(num-1));
				writer.writerow([key,total_restime,num,mean,stdv]);
			else:
				writer.writerow([key,0,0,'N/A','N/A'])
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
        
    #   rankent=RankEntity1(emailid=users, Score=Score,RT=int(round(RT)),
    #                       EnS=EnS,EnS_RT=int(round(EnS_RT)),
    #                       Num=Num,Num_RT=int(round(Num_RT)),
    #                       RC=RC,RC_RT=int(round(RC_RT)),
    #                       LC=LC,LC_RT=int(round(LC_RT)),
    #                       Te=Te,Te_RT=int(round(Te_RT)))
    #   ranklist.append(rankent);
    # n=len(ranklist);
    # for j in range(0,n-1):
    #   Max=j
    #   for i in range(j+1,n):
    #     if(ranklist[i].Score>ranklist[Max].Score):
    #       Max=i;
    #     elif (ranklist[i].Score==ranklist[Max].Score):
    #       if(ranklist[i].RT<ranklist[Max].RT):
    #         Max=i;
    #   if(not Max==j):
    #     ranklist[j],ranklist[Max]=ranklist[Max],ranklist[j];
    # i=0;
    # for q in ranklist:
    #   row=[q.emailid.encode('utf-8'),q.EnS,q.EnS_RT,q.Num,q.Num_RT,q.RC,q.RC_RT,q.LC,q.LC_RT,q.Te,q.Te_RT,q.Score,q.RT,i+1]
    #   writer.writerow(row);
    #   i +=1;
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
			for key in range(1,19):
				key = str(key)
				if key in score_dict:
					apt_score += score_dict[key][0]
					apt_rt +=score_dict[key][1]
					if score_dict[key][0] == 1:
						apt_correct_rt += score_dict[key][1]
			for key in range(20,28):
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
				row=[user,apt_score,toefl_score,round(apt_rt/10,1),round(toefl_rt/10,1),round(apt_correct_rt/10,1),round(toefl_correct_rt/10,1)];
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
class User_apti_questions_data(webapp2.RequestHandler):
	def get(self,filename):
		self.response.headers['Content-Type'] = 'text/csv'
		self.response.headers['Content-Disposition'] = 'attachment; filename='+filename+'_Question_details.csv'
		writer = csv.writer(self.response.out)
		writer.writerow(['Mail id','Q1_score','Q1_RT','Q2_score','Q2_RT','Q3_score','Q3_RT','Q4_score','Q4_RT','Q5_score','Q5_RT','Q6_score','Q6_RT','Q7_score','Q7_RT','Q8_score','Q8_RT','Q9_score','Q9_RT','Q10_score','Q10_RT','Q11_score','Q11_RT','Q12_score','Q12_RT','Q13_score','Q13_RT','Q14_score','Q14_RT','Q15_score','Q15_RT','Q16_score','Q16_RT','Q17_score','Q17_RT','Q18_score','Q18_RT'])
		userslist=[];
		f = open(filename+".csv")
		for line in f:
			rec = line.strip().split(",")
			userslist.append(rec[0])
		f.close();
		for user in userslist:
			score_list=[]
			rt_list=[]
			for qid in range(101,501):
				q3= Response.query(ndb.AND(Response.useremailid.emailid==user,Response.serialno==qid)).order(Response.serialno,-Response.time)
				q3.fetch(1)
				for data in q3:
					score_list.append(data.q_score);
					if data.q_score == 1:
						rt_list.append(round(data.responsetime/60,1));
					else:
						rt_list.append(0);
			if score_list:
				if rt_list:
					writer.writerow([user,score_list[0],rt_list[0],score_list[1],rt_list[1],score_list[2],rt_list[2],score_list[3],rt_list[3],score_list[4],rt_list[4],score_list[5],rt_list[5],score_list[6],rt_list[6],score_list[7],rt_list[7],score_list[8],rt_list[8],score_list[9],rt_list[9],score_list[10],rt_list[10],
					score_list[11],rt_list[11],score_list[12],rt_list[12],score_list[13],rt_list[13],score_list[14],rt_list[14],score_list[15],rt_list[15],score_list[16],rt_list[16],score_list[17],rt_list[17]])


class User_toefl_questions_data(webapp2.RequestHandler):
	def get(self,filename):
		self.response.headers['Content-Type'] = 'text/csv'
		self.response.headers['Content-Disposition'] = 'attachment; filename='+filename+'_tfl_Question_details.csv'
		writer = csv.writer(self.response.out)
		writer.writerow(['Mail id','Q1_score','Q1_RT','Q2_score','Q2_RT','Q3_score','Q3_RT','Q4_score','Q4_RT','Q5_score','Q5_RT','Q6_score','Q6_RT','Q7_score','Q7_RT','Q8_score','Q8_RT'])
		userslist=[];
		f = open(filename+".csv")
		for line in f:
			rec = line.strip().split(",")
			userslist.append(rec[0])
		f.close();
		for user in userslist:
			score_list=[]
			rt_list=[]
			for qid in range(601,801):
				q3= Response.query(ndb.AND(Response.useremailid.emailid==user,Response.serialno == qid)).order(Response.serialno,-Response.time)
				q3.fetch(1)
				for data in q3:
					score_list.append(data.q_score);
					if data.q_score == 1:
						rt_list.append(round(data.responsetime/10,1));
					else:
						rt_list.append(0);
			print score_list;
			logging.error("score");
			print rt_list;
			logging.error("rt");
			if score_list:
				if rt_list:
					writer.writerow([user,score_list[0],rt_list[0],score_list[1],rt_list[1],score_list[2],rt_list[2],score_list[3],rt_list[3],score_list[4],rt_list[4],score_list[5],rt_list[5],score_list[6],rt_list[6],score_list[7],rt_list[7]])

class updateEnsScore(webapp2.RequestHandler):
  def get(self,filename):
    userslist=[];
    f = open(filename+".csv")
    for line in f:
      rec = line.strip().split(",")
      userslist.append(rec[0])
    f.close();
    for user in userslist:
    	q2= Response.query(ndb.AND(Response.useremailid.emailid==user,Response.serialno==27)).order(Response.serialno,-Response.time)
    	q2.fetch()
    	for rec in q2:
    		if rec.submittedans == "Whenever she thinks of her father" :
    			score=1
    		else :
    			score=0
    		q3=Response(serialno=rec.serialno,useremailid=User(emailid=rec.useremailid.emailid,name=rec.useremailid.name),
	                  currentQuestion=rec.currentQuestion,submittedans=rec.submittedans,time=rec.time,
	                  responsetime=rec.responsetime,q_status=rec.q_status,q_score=score)
    		rec.key.delete();
    		q3.put();
    self.response.write("Updated success");
class get_QB(webapp2.RequestHandler):
  def post(self):
    json_data=getAllQuestions()
    print json_data
    logging.error("question data")
    ss=json.dumps(json_data)
    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
    self.response.write(ss)
application = webapp2.WSGIApplication([
    ('/admin/?',Home),
    ('/admin/adminhome',AdminHome),
    ('/admin/quizdetails/([^/]+)?',QuizDetails),
    ('/admin/userquizreport/([^/]+)?',UserQuizReport), 
    ('/admin/downloadcsv/([^/]+)?',DownloadCSV),
    ('/admin/downloadcsv_user/([^/]+)?',DownloadCSV_User),
    ('/admin/sendinvitesview',SendInvitesView),
    ('/admin/sendinvites',SendInvites),
    ('/admin/questionstatistics/([^/]+)?',QuestionStatistics),
    ('/admin/getessay/([^/]+)?',GetEssay),
    ('/admin/getmeanstd/([^/]+)?',getMeanStd),
    ('/admin/getmeanstd_apti/([^/]+)?',getMeanStd_Apti),
    ('/admin/getmeanstd_toefl/([^/]+)?',getMeanStd_toefl),
    ('/admin/getMeanStd_telugu/([^/]+)?',getMeanStd_telugu),
    ('/admin/questionstatistics_toefl/([^/]+)?',QuestionStatistics_Toefl),
    ('/admin/user_apti_questions_data/([^/]+)?',User_apti_questions_data),
    ('/admin/user_toefl_questions_data/([^/]+)?',User_toefl_questions_data),
    ('/admin/update_ens/([^/]+)?',updateEnsScore),
    ('/admin/get_qb',get_QB),
       ], debug=True)