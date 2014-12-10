import math      
import string
import random    
from diggSqlCon import DIGGSQLCONN
from datetime import datetime
import os
import threading
import getopt,sys
from random import randrange


# user_id   -> friend_id:    user_id is a friend of friend_id. 
# from the information propagation perspective, friend_id is the ego, and user_id is the later.   ego -> alter  
# once information is posted by ego(friend_id), it may be copied by its alter (user_id)
# In following, we will think the link direction is from ego to alter (for convenience of nodes' reachability).


class DIGGGCC:
    NO_TIMER=0
    UNIFORM_TIMER=1
    EXP_TIMER=2
    EXP_TIMER_DECAY=3    
    CONS_FRIEND=4
    def __init__(self):
        #self.v_dirpath='D:\workspace\Data\Network data\citation network\Terms map\\'
        self.v_dirpath='/Users/biru/workspace/Digg/'
        #self.v_dirpath='D:/workspace/Data/Network data/Digg/'
        self.v_sql = DIGGSQLCONN()
        self.v_sql.openConn('localhost', 'root', 'cui', 'Digg')

    def strip(self, l):
        ret=[]
        for i in l:
            ret.append(i[0])
        return ret


    def updateFriendsNum(self):   #outgoing link, the alters ego node can affect
        # the friends_num is how many users following this user, it decides how many users can be infected by this user.
        self.v_sql.updateFriendsNum()  
        
    def updateCaresNum(self):     # incoming link
        # this is how many people this user following
        self.v_sql.updateCaresNum()

    # the function extracts the in and out degrees of every node, and save it to users
    def degrees(self):
        self.updateFriendsNum()
        self.updateCaresNum()


    def reachability(self):
        self.v_sql.updateReachability()

    # find the giant connected components
    def findGCC(self):
        allUsers=self.strip(self.v_sql.allUsers())
        
        CC={}
        while len(allUsers):
            # check whether this node is connected to existing CC
            # find all nodes connected to i
            n = allUsers[0]
            print n
            friends=self.strip(self.v_sql.friends(n))
            merge=[]
            for cc in CC:
                if len(set(friends).intersection(set(CC[cc][1])))>0:
                    merge.append(cc)
            
            if len(merge):
                #merge             
                m=merge[0]
                for cc in merge:
                    if m != cc:
                        CC[m][1]=CC[m][1] | CC[cc][1]
                        CC[m][2]+=CC[cc][2]
                        del CC[cc]
                CC[m][0].add(n)
                check = m
            else:
                CC[n]=[set(),set(),0] #contained, accessed, length
                CC[n][0].add(n)
                check = n
                
            while len(CC[check][0]):
                a = list(CC[check][0])[0]
                friends=self.strip(self.v_sql.friends(a))
                for f in friends:
                    if f not in CC[check][1]:
                        CC[check][0].add(f)
                CC[check][0].remove(a)
                CC[check][1].add(a)
                if a in allUsers:
                    allUsers.remove(a)
                CC[check][2] +=1
                if CC[check][2]%100==0:
                    print CC[check][2], len(CC[check][0]), len(CC[check][1])
        
        
        fileName=self.v_dirpath + '/output/CCsize.txt'
        fo = open(fileName, "w+") 
        for c in CC.keys():
            for i in CC[c][1]:
                fo.write(str(i))
                fo.write(" ")
            fo.write("\n")
        fo.close()
            
            
def main():
    digg=DIGGGCC()
    digg.reachability()
            
if __name__ == '__main__':
    main()
