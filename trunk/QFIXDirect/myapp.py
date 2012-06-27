import re
import datetime
import setting
import quickfix
import quickfix.field
from java.util import Date
from java.text import SimpleDateFormat
import logging
log = logging.getLogger(__name__)

import default_cfg

import stomp
class Order_Sender(stomp.ConnectionListener):
    """
    """
    ##  stomp implementation
    def on_message(self,headers,msg):
        """
            stomp interface
        """
        try:
            log.debug(headers)
            log.debug(msg)
            session = headers.get('session')
            log.info("on stomp message from fix_out, send to %s" % session)
            ## Session send msg here
            if session in default_cfg.SESS_CFG.keys():
                fix_session = default_cfg.SESS_CFG[session]
                log.info("sending message to session %s, %s" % (session,fix_session))
                fix_msg =  quickfix.Message(msg,True)
                sess_id = quickfix.SessionID(fix_session)
                log.info("%s, %s" %(sess_id,fix_msg))
                quickfix.Session.sendToTarget(fix_msg,sess_id)

            else:
                print "unknown session?? no message send"

        # except JMSException , e:
            # print e.toString()
        except quickfix.InvalidMessage, e:
            print "received invalid message"
            print e.toString()
        except quickfix.SessionNotFound, e:
            print "session not found"
            print e.toString()


    def on_error(self,headers,message):
        """
            stomp interface
        """
        print "on error"
        print headers
        print message

import pprint
import pyfix42
import StringIO

class MyApp(quickfix.Application):
    """
        quickfix app
    """
    def __init__(self,url):
        """ init stomp MQ connection """
        self.conn = stomp.Connection(host_and_ports=[("mtxent12",61612)])     # default localhost:61613

    def onCreate(self, sessionID):
        print sessionID.toString()
        print ("onCreate %s" % (sessionID.getSenderCompID()))

    def onLogon(self, sessionID): 
        print("onLogon %s" % (sessionID.getSenderCompID()))
        # reset connection
        #if self.conn:
        assert(self.conn)
        if not self.conn.is_connected():
            self.conn.set_listener('order',Order_Sender())
            self.conn.start()
            self.conn.connect()
            self.conn.subscribe(destination=default_cfg.OUT_Q, ack='auto') 

    def onLogout(self, sessionID): 
        print("onLogout %s" % (sessionID.getSenderCompID()))
        assert(self.conn)
        self.conn.stop()
        if self.conn.is_connected():
            self.conn.disconnect()
        if self.conn.get_listener('order') != None:
            self.conn.remove_listener('order')

    def toAdmin(self, message, sessionID): 
        '''
        '''
        #print("inbound Admin msg: %s: %s" % (sessionID.getSenderCompID(),type(message)))

    def toApp(self, message, sessionID): 
        '''
        '''
        # print("OUT app msg %s: %s" % (sessionID.getSenderCompID(),type(message)))
        msg = pyfix42.parse(message.toString().strip())[0]
        print sessionID.toString(),"->",msg['MsgType'],msg.get("OrdType",""),msg['Symbol'],msg["Side"],msg.get('Price',""),msg['OrderQty'],msg["ClOrdID"],msg.get('OrigClOrdID',"")
        ## 
        log.info("<- %s" % message)
        if msg['MsgType'] not in pyfix42.IGNORE:
            for k,v in pyfix42.WTAGS_HEADER.iteritems():
                if msg.get(k):
                    msg.pop(k)
        io = StringIO.StringIO()
        pprint.pprint(msg,io,indent=2,depth=4)
        output = io.getvalue()
        log.info(output)

    def fromAdmin(self, message, sessionID):
        """
        received inbound admin msg
        """
        #print("from admin %s: %s" % (sessionID.getSenderCompID(),type(message)))
        session = quickfix.Session.lookupSession(sessionID)
        if (session == None):
            raise SessionNotFound(sessionID.toString())
        senderSeqNum = session.getExpectedSenderNum() 
        targetSeqNum = session.getExpectedTargetNum() 
        #print("senderSeq: %d: targetSeq: %d" % (senderSeqNum,targetSeqNum))

    def fromApp(self, message, sessionID):
        '''
            received inbound app msg
        '''
        #print "IN app msg %s: %s" % (sessionID.getSenderCompID(),type(message))
        #print "message is: %s" % (message.toString())
        msg = pyfix42.parse(message.toString().strip())[0]
        print sessionID.toString(),"<-",msg['MsgType'],msg.get('OrdType',''),msg.get('OrdStatus',''),msg.get('ExecType',''),msg.get('Symbol',''),\
          msg.get('LastShares',''),msg.get('LastPx',''),msg.get("ClOrdID"),msg.get('OrderID','')
        ## 
        log.info("<- %s" % message)
        if msg['MsgType'] not in pyfix42.IGNORE:
            for k,v in pyfix42.WTAGS_HEADER.iteritems():
                if msg.get(k):
                    msg.pop(k)
        io = StringIO.StringIO()
        pprint.pprint(msg,io,indent=2,depth=4)
        output = io.getvalue()
        log.info(output)
        ### push into queue fix_in
        if self.conn.is_connected():
            self.conn.send(message.toString(),destination=default_cfg.IN_Q)
