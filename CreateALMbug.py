
from jira import JIRA
import imapclient
import pprint
import pyzmail
import threading
import SendMail
from im.ImHandler import ImHandler


def create_issue():
    imapObj = imapclient.IMAPClient('imaphz.qiye.163.com', ssl=True)
    imapObj.login('service.jira@t2mobile.com', 'bBDCP5ZKQ72QUzcP')
    imapObj.select_folder('INBOX')

    InstanceJira = JIRA('http://172.16.11.219:8080', auth=('guxiaocong', '123456'))

    UIDS = []
    UIDS = imapObj.search('UNSEEN')  # get all unread mails and store into UIDs
    print 'start to search mail.....'
    rawMessages = imapObj.fetch(UIDS, ['BODY[]'])  # get all ID of each mails according to the UIDs
    
    if len(UIDS) !=0:
        for num in rawMessages:
            messageObj = pyzmail.PyzMessage.factory(rawMessages[num]['BODY[]'])
            if messageObj.text_part:
                print 'text'
            else:
                if (messageObj.html_part):
                    mailBody = messageObj.html_part.get_payload().decode(messageObj.html_part.charset)
                  #  pprint.pprint(mailBody)
                    print 'html'
                    if mailBody.find('<strong>created</strong>') != -1 and mailBody.find('Issue template (WBSGantt)')!=-1:
                        searchsummary_start =mailBody.find('T2M_BUG_SYS')
                        summaryStart= mailBody.find('href',searchsummary_start)
                        summaryEnd=mailBody.find('"',summaryStart+10)
                        almsummary = mailBody[summaryStart+6 : summaryEnd]

                        searchAffectsVersion_start = mailBody.find('Affects Versions:')
                        versionStart = mailBody.find('top',searchAffectsVersion_start)
                        versionEnd = mailBody.find('<' ,versionStart)
                        almversion = mailBody[versionStart+7:versionEnd]

                        jirabugid = almsummary[almsummary.rfind('/',0,len(almsummary))+1: len(almsummary)]

                        almbug_id, out, err = ImHandler.create_defect("/TCT/QCT SDM450/T2-PM45 PM85 P upgrade", almsummary.strip(), almversion.strip(),"pm85p-devel", 'yan.han', '1Q2w3e4r!')
                        print('Alm bug created: %s' % almbug_id)
                        if almbug_id != None:            #start to fill in ALM ID
                            issue = InstanceJira.issue(jirabugid)
                            issue.update(fields={'customfield_10400': almbug_id})
                            print('Jira field updated. Jira ID: %s, Alm ID: %s' % (jirabugid, almbug_id))
                        else:
                            print 'cannot find the almbug of: ' +jirabugid
                            SendMail.send_email_by_smtp('cannot find the almbug of: ' +jirabugid,
                                                        'Error on bug %s\n====> stdout\n%s\n====>stderr\n%s' % (jirabugid, out, err),
                                                        'yujin.huang@t2mobile.com')
                    else:
                        print "this is not a bug creation"
    imapObj.logout()

count =0

def fun_create_issue():

    global count

    try:
        create_issue()
        count=0
    except Exception,e:
        count +=1
        SendMail.send_email_by_smtp('create ALM BUG error', e.message, 'yujin.huang@t2mobile.com')

    if count<5:
        global timer
        timer = threading.Timer(300,fun_create_issue)
        timer.start()
    else:
        SendMail.send_email_by_smtp('create ALM BUG error', e.message, 'yujin.huang@t2mobile.com')


if __name__ == '__main__':
    fun_create_issue()
