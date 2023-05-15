import PyPDF2
import io
from datetime import datetime, timedelta
import schedule
import time

'''
fetch resumes from email at a certain time of the day
convert them to text and return them in a list,

NEED TO PASS THEM TO THE MODEL AND APPLY NER FOR PARSING.

'''


import imaplib
import email
import os
import PyPDF2

import pandas as pd
import os
import spacy

import math
from datetime import datetime
import time
def generateID():
    time.sleep(0.3)
    dt=datetime.now()
    ts=datetime.timestamp(dt)
    id=ts*1000000
    return str(id)

def extractSkills(resume_doc):
    resume_doc=resume_doc.lower()
    skillset=set()
    skill_df=pd.DataFrame(pd.read_csv("Parser/home/skills.csv"))
    # tokens=resume_text.split()    #for resume text as tokens
    '''
    tokens=[]
    for token in resume_doc:
        
        if token.pos_ =='NOUN':
            tokens.append(token)
            
        if not token.is_stop:
            tokens.append(token)
    print(tokens)
    for skill in skill_df:
        for t in tokens:
            if str(t) in skill :
                skillset.add(skill)
                # print('token ',t,' present in ',skill)
    '''
    for skill in skill_df:
        '''
        if len(skill)==1:
            if ' '+skill+' ' in resume_doc or ' '+skill+',' in resume_doc:
                skillset.add(skill)
        '''
        if ' '+skill+' ' in resume_doc or ' '+skill+',' in resume_doc:
            skillset.add(skill)
    # print('SKILLSET --------------------','\n',skillset)
    return skillset



'''
code for processing resumes using model and parsing them
'''
nlp = spacy.load("en_core_web_sm")
nlp_ner = spacy.load("D:/2mscCS/sem4/project/Resume Parser with NER/Parser/home/model-best")
def parseResume(resume_text):
    # res_doc=nlp(resume_text)
    doc=nlp_ner(resume_text)
    # print('\n\n',doc,'\n')
    spacy.displacy.render(doc, style="ent") # display in Jupyter
    label_list=["ROWID","NAME","DESIGNATION","LOCATION","COMPANIES WORKED AT","SKILLS","COLLEGE NAME","DEGREE","GRADUATION YEAR","EMAIL ADDRESS","STATUS"]
    mydict={}
    for i in label_list:
        mydict[i]=[[]]
    mydict['ROWID']=generateID()
    for i in range(len(doc.ents)):
        entt=doc.ents[i]
        labl=doc.ents[i].label_
        print(doc.ents[i],"  ",doc.ents[i].label_)
        mydict[labl][0].append(str(entt))
    if mydict['NAME']==[[]]:
        mydict['NAME']=str(doc[0])+' '+str(doc[1])
    # print(mydict)
    mydict["SKILLS"][0]+=list(extractSkills(resume_text))
    df=pd.DataFrame(mydict)
    print(df)
    csv_name='D:/2mscCS/sem4/project/Resume Parser with NER/Parser/home/MY-PARSED-DATA.csv'
    df_source = None
    if os.path.exists(csv_name):
        df_source = pd.DataFrame(pd.read_csv(csv_name,index_col=0))
    if df_source is not None:
        df_source=pd.concat([df_source,df])
        # df_source=pd.concat([df_source,df],ignore_index=True)
        df_dest = df_source
    else:
        df_dest = df
    df_dest.to_csv('D:/2mscCS/sem4/project/Resume Parser with NER/Parser/home/MY-PARSED-DATA.csv')

# connect to the email account
#  vrfbueefzvtqkmte - python app password for gmail
'''
pdf from email extraction
'''


def get_resumes_from_mail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('alicebirdie30@gmail.com', 'vrfbueefzvtqkmte')
    mail.select('inbox')
    # now = datetime.now()
    now = datetime.today().strftime('%d-%b-%Y')
    # search_query = 'SINCE {0}'.format(now.strftime('%d-%b-%Y'))
    search_query = f'(SINCE "{now}") (BODY "pdf")'
    # status, email_ids = mail.search(None, '(BODY "application/pdf")')
    status, email_ids = mail.search(None, search_query)
    email_ids=email_ids[0].decode('utf-8') 
    return email_ids,mail



def get_resume_text():
    pdf_list=[]
    email_ids,mail=get_resumes_from_mail()
    for email_id in email_ids.split():
        # fetch the email data
        status, email_data = mail.fetch(email_id, '(RFC822)')
        # parse the email data using the email library
        email_message = email.message_from_bytes(email_data[0][1])
        # iterate over the email attachments
        for part in email_message.walk():
            if part.get_content_type() == 'application/pdf':
                # extract the PDF data using PyPDF2
                x = part.get_payload(decode=True)
                pdf_data=io.BytesIO(x)
                pdf_reader = PyPDF2.PdfReader(pdf_data)
                num_pages = len(pdf_reader.pages)
                page_text=''
                for page_num in range(num_pages):
                    # Get the page object for the current page
                    page_obj = pdf_reader.pages[page_num]
                    # Extract the text from the page
                    page_text = page_text+ page_obj.extract_text()
                    # Print the text for the current page
                    # print(page_text)
                pdf_list.append(page_text.strip().replace('\n',' '))
    mail.close()
    mail.logout()
    print('pdf_list has ',len(pdf_list), ' pdfs')
    # print(pdf_list)
    print('done')
    return pdf_list


def mainProcess():
    pdfs=get_resume_text()
    for pdf in pdfs:
        parseResume(pdf)

# get_resume_text()
# Schedule the script to run at a specific time each day
''''
schedule.every().day.at('05:30').do(mainProcess)

# Run the script indefinitely

while True:
    schedule.run_pending()
    time.sleep(60)
'''
mainProcess()


'''
# pdf to text code

# Open the PDF file in read-binary mode
with open('example.pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Get the total number of pages in the PDF file
    num_pages = pdf_reader.getNumPages()

    # Loop through each page in the PDF file
for page_num in range(num_pages):
    # Get the page object for the current page
    page_obj = pdf_reader.getPage(page_num)
    # Extract the text from the page
    page_text = page_obj.extractText()
    # Print the text for the current page
    print(page_text)

'''


'''
# code for scheduling

import imaplib
from datetime import datetime, timedelta
import email
import schedule
import time

def search_emails_for_current_day(username, password):
    # Connect to the IMAP server
    imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_server.login(username, password)

    # Get the current date and time
    now = datetime.now()

    # Construct the search query string
    search_query = 'SINCE {0}'.format(now.strftime('%d-%b-%Y'))

    # Search for messages that match the query
    imap_server.select('INBOX')
    result, data = imap_server.search(None, search_query)

    # Process each message
    emails = []
    for msg_id in data[0].split():
        result, msg_data = imap_server.fetch(msg_id, '(RFC822)')
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        emails.append(email_message)

    # Disconnect from the server
    imap_server.close()
    imap_server.logout()

    return emails

def extract_emails():
    # Set your email credentials
    username = 'your-email@example.com'
    password = 'your-password'

    # Search for emails sent on the current day
    emails = search_emails_for_current_day(username, password)

    # Do something with the extracted emails (e.g. save to a database or file)
    print('Extracted {0} emails.'.format(len(emails)))

# Schedule the script to run at a specific time each day
schedule.every().day.at('08:00').do(extract_emails)

# Run the script indefinitely
while True:
    schedule.run_pending()
    time.sleep(60)





'''