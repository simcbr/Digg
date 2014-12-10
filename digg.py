import math      
import string
import random    
from diggSqlCon import DIGGSQLCONN
from datetime import datetime
import os
import threading
import getopt,sys
from random import randrange



class DIGG:
    NO_TIMER=0
    UNIFORM_TIMER=1
    EXP_TIMER=2
    EXP_TIMER_DECAY=3    
    CONS_FRIEND=4
    def __init__(self):
        #self.v_dirpath='D:\workspace\Data\Network data\citation network\Terms map\\'
        self.v_dirpath='/Users/biru/workspace/Digg/output/'
        #self.v_dirpath='D:/workspace/Data/Network data/Digg/'
        self.v_sql = DIGGSQLCONN()
        self.v_sql.openConn('localhost', 'root', 'cui', 'Digg')

    def createTabs(self):
        #this function create all tables
        self.v_sql.createTabFriends()

    def createTabUsers(self):
        self.v_sql.createTabUsers()
        
    def createTabVotes(self):
        self.v_sql.createTabVotes()
        #" (mutual, create_time, user_id, friend_id)"
        
    def createTabConnVotes(self):
        self.v_sql.createTabConnVotes()
        
    def loadFriendsCSVFiles(self):
        self.v_sql.loadCSVFile(self.v_dirpath + "digg_friends.csv", 'friends', " (mutual, create_time, user_id, friend_id)")
        print "friends-----"
        self.v_sql.commit()
        print "commit-----"
        
    def loadVotesCSVFiles(self):
        self.v_sql.loadCSVFile(self.v_dirpath + "digg_votes1.csv", 'votes', " (vote_time, voter_id, story_id)")
        print "votes-----"
        self.v_sql.commit()
        print "commit-----"        
        
    def updateFriendsNum(self):
        # the friends_num is how many users following this user, it decides how many users can be infected by this user.
        self.v_sql.updateFriendsNum()  
        
    def updateCaresNum(self):
        # this is how many people this user following
        self.v_sql.updateCaresNum()
        
    def updateProbabilitySameAct(self):
        # update the link probability using the portion of same actions
        self.v_sql.updateProbabilitySameAct()
        
    
    def updateProbabilityNetInf(self):
        # update the link probability using the netinf
        self.v_sql.updateProbanilityNetInf()
                
    def outputFriendsNum(self):
        #retrieve friends_num
        # format:  out_degree, in_degree, user_id
        N=self.v_sql.usersNum()
        fileName=self.v_dirpath + 'friends_hist.txt'  
        fo = open(fileName, "w+")
        for i in range(N):
            num = self.v_sql.friendsNum(i+1)
            fo.write(str(num))
            fo.write(" ")
            num = self.v_sql.caresNum(i+1)
            fo.write(str(num))
            fo.write(" ")
            num = self.v_sql.userId(i+1)
            fo.write(str(num))
            fo.write("\n")
        fo.close()
                

    def outputActProbHist(self):
        i=0
        interval=0.001
        fileName=self.v_dirpath + 'prob_same_act_hist.txt'  
        fo = open(fileName, "w+")
        while i <=1:
            num = self.v_sql.actProbHist(i, i + interval)
            fo.write(str(i))
            fo.write(" ")
            fo.write(str(num))
            fo.write("\n")            
            i += interval
            print i
        fo.close()
        
                
    def infectionFeatures(self):
        # each initial seed create a cascade (the cascade could be trivial: single node; or small: several nodes)
        CNUM=self.v_sql.storiesNum()
        
        # output it
        fileName=self.v_dirpath + 'digg_infected_features_9_valid_2.txt'
        foI = open(fileName, "w+")
        fileName=self.v_dirpath + 'digg_uninfected_features_9_valid_2.txt'
        foU = open(fileName, "w+")
                
        for i in range(CNUM/3, CNUM/3*2):
            # for each story
            print i,CNUM            
            # find all cascades of this story
            (infected, uninfected) = self.v_sql.extractInfectionFeatures(i+1)

            for k in infected:
                for t in k:
                    foI.write(str(t))
                    foI.write(" \t")
                foI.write("\n")
            
            for k in uninfected:
                for t in k:
                    foU.write(str(t))
                    foU.write(" \t")
                foU.write("\n")    
                
        foI.close()
        foU.close()  
        
        
    def infectionFeaturesSameNodes(self):
        # each initial seed create a cascade (the cascade could be trivial: single node; or small: several nodes)
        CNUM=self.v_sql.storiesNum()
        
        # output it
#        fileName=self.v_dirpath + 'digg_infected_features_9_sameNodes.txt'
#        foI = open(fileName, "w+")
        fileName=self.v_dirpath + 'digg_uninfected_features_9_sameNodes.txt'
        foU = open(fileName, "w+")
#        fileName=self.v_dirpath + 'digg_seeds_sameNodes.txt'
#        foS = open(fileName, "w+")
                
        cascadesDict={}
        cascadesStartTimeDict={}
        monitorNodes=set()
        seeds=[]
        for i in range(CNUM):
            # for each story
            print "infected",i,CNUM
       
            # find all cascades of this story
            (cascades, cascadesStartTime, infected, infectedNodes) = self.v_sql.extractInfectedFeatures(i+1)
            
#            for k in cascades.keys():
#                if k not in seeds:
#                    seeds.append(k)
            
            cascadesDict[i+1]=cascades
            cascadesStartTimeDict[i+1]=cascadesStartTime
            monitorNodes=monitorNodes.union(infectedNodes)
            
#            for k in infected:
#                for t in k:
#                    foI.write(str(t))
#                    foI.write(" \t")
#                foI.write("\n")              

            
          
#            
#        for s in seeds:
#            foS.write(str(s))
#            foS.write("\n")            
#            
#        foI.close()
#        foS.close()             
            
        # find uninfected samples from monitorNodes
        #M = len(infectedDict)
        for i in range(CNUM):
#            if M<=0:
#                break
            print "uninfected", i,CNUM
            for node in list(monitorNodes):
                (uninfected) = self.v_sql.extractUninfectedFeatures(cascadesDict[i+1], cascadesStartTimeDict[i+1], node)
                
                for k in uninfected:
                    for t in k:
                        foU.write(str(t))
                        foU.write(" \t")
                    foU.write("\n")    


                
        foU.close()   
                
                
    def infectionTimeDiffDistributionPerLocation(self):
        # each initial seed create a cascade (the cascade could be trivial: single node; or small: several nodes)
        CNUM=self.v_sql.storiesNum()
        
        # output it
        fileName=self.v_dirpath + 'digg_infection_time_difference_distribution_per_location.txt'
        fo = open(fileName, "w+")
    
                
        for i in range(CNUM):
            # for each story
            print i,CNUM            
            # find all cascades of this story
            (locations) = self.v_sql.extractInfectionTimeDifferencePerLocation(i+1)

            for l in locations.keys():
                for t in locations[l].keys():
                    fo.write(str(l))
                    fo.write(" \t")
                    fo.write(str(t))
                    fo.write(" \t")
                    fo.write(str(locations[l][t]))
                    fo.write("\n")
                
                
        fo.close()   
                
                
    def infectionTimeDistribution(self):
        # each initial seed create a cascade (the cascade could be trivial: single node; or small: several nodes)
        CNUM=self.v_sql.storiesNum()
        
        # output it
        fileName=self.v_dirpath + 'digg_infection_time_distribution.txt'
        fo = open(fileName, "w+")
    
                
        for i in range(CNUM):
            # for each story
            print i,CNUM            
            # find all cascades of this story
            (times) = self.v_sql.extractInfectionTime(i+1)

            for t in times.keys():
                fo.write(str(t))
                fo.write(" \t")
                fo.write(str(times[t]))
                fo.write("\n")
                
                
        fo.close()                   
    
    def infectionTimeDifferenceDistribution(self):
        # each initial seed create a cascade (the cascade could be trivial: single node; or small: several nodes)
        CNUM=self.v_sql.storiesNum()
        
        # output it
        fileName=self.v_dirpath + 'digg_infection_time_difference_distribution.txt'
        fo = open(fileName, "w+")
    
                
        for i in range(CNUM):
            # for each story
            print i,CNUM            
            # find all cascades of this story
            (times) = self.v_sql.extractInfectionTimeDifference(i+1)

            for t in times.keys():
                fo.write(str(t))
                fo.write(" \t")
                fo.write(str(times[t]))
                fo.write("\n")
                
                
        fo.close()                
                
                
    def cascadesDistribution(self):
        # each initial seed create a cascade (the cascade could be trivial: single node; or small: several nodes)
        CNUM=self.v_sql.storiesNum()
        
        # output it
        fileName=self.v_dirpath + 'digg_cascade_size_distribution.txt'
        fo = open(fileName, "w+")
         
        fo.write("storyNum \t cascadeSize \t depth \n")
        
#        fileName2=self.v_dirpath + 'digg_cascade_steps_prob.txt'
#        fo2 = open(fileName2, "w+")
#        
#        fo2.write("storyNum \t level \t infected \t potential \n")
      
        fileName3=self.v_dirpath + 'digg_influence_size_distribution.txt'
        fo3 = open(fileName3, "w+")
        
        fo3.write("storyNum \t influenceSize \t seedsNum \n")      
      
        
        for i in range(CNUM):
            # for each story
            print i,CNUM            
            # find all cascades of this story
            (cascades, seedsHist) = self.v_sql.extractCascades(i+1)
            
            
            influenceSize=0
            for k in cascades.keys():
                fo.write(str(i))
                fo.write(" \t")
                size = cascades[k].treeSize()
                fo.write(str(size))
                influenceSize += size - 1
                fo.write(" \t")
                fo.write(str(cascades[k].treeDepth()))
                fo.write("\n")

            fo3.write(str(i))
            fo3.write("\t")
            fo3.write(str(influenceSize))
            fo3.write("\t")
            fo3.write(str(len(cascades)))
            fo3.write("\n")

#             startTime = self.v_sql.firstVoteTimeStory(i+1)
#             for k in seedsHist.keys():
#                 timediff = self.v_sql.hourDiff(startTime, seedsHist[k])
#                 fo.write(str(i))
#                 fo.write(" \t")
#                 fo.write(str(timediff))
#                 fo.write("\n")
            
        fo.close()
        fo3.close()        
#        fo2.close()
        
    
    # the function try to find the infection probability change along the time
    def cascadesProbabilityDistribution(self):
        # each initial seed create a cascade (the cascade could be trivial: single node; or small: several nodes)
        CNUM=self.v_sql.storiesNum()
        
        # output it
        fileName=self.v_dirpath + 'digg_cascade_prob_distribution.txt'
        fo = open(fileName, "w+")
        
        for i in range(CNUM):
            # for each story
            print i,CNUM   
            i=1816
            # find all cascades of this story
            (prob_dist, seedsCount) = self.v_sql.extractCascadesProb(i+1)
            
            for k in prob_dist.keys():
                fo.write(str(i))
                fo.write(" \t")
                fo.write(str(k))
                fo.write(" \t")
                fo.write(str(seedsCount[k]))
                fo.write(" \t")
                #for j in prob_dist[k]:
                #    fo.write(str(j))
                #    fo.write("\t")
                if len(prob_dist[k])==0:
                    avg=0
                else:
                    avg = sum(prob_dist[k])/float(len(prob_dist[k]))
                fo.write(str(avg))
                fo.write("\n")
                
        fo.close()        
        
        
    def cascadesSteps(self):
        # each initial seed create a cascade (the cascade could be trivial: single node; or small: several nodes)
        CNUM=self.v_sql.storiesNum()
        
        # output it
        #fileName=self.v_dirpath + 'digg_cascade_steps.txt'
        fileName=self.v_dirpath + 'digg_cascade_steps_orig_c_ext.txt'
        #fileName=self.v_dirpath + 'digg_cascade_size_life.txt'
        fo = open(fileName, "w+")
        
        for i in range(CNUM):
            # for each story
            print i,CNUM   
            # find all cascades of this story
            
            (steps_dist, cascades_steps_dist) = self.v_sql.extractCascadesStepsOrigProb(i+1)
            
#            for k in steps_dist.keys():   #time
#                for s in steps_dist[k].keys():  #depth
#                    for o in steps_dist[k][s].keys():  #orig
#                        fo.write(str(i))
#                        fo.write(" \t")
#                        fo.write(str(k))
#                        fo.write(" \t")
#                        fo.write(str(s))
#                        fo.write(" \t")
#                        fo.write(str(o))
#                        fo.write(" \t")
#                        fo.write(str(steps_dist[k][s][o]))
#                        fo.write(" \t")
#                        fo.write("\n")
                        
            # format: story_id | time | cascade_id | level (the depth of these nodes) | orig (the time its parent being infected) | number | potential nodes could being infected by its parents 
            for k in cascades_steps_dist.keys():   #time
                for c in cascades_steps_dist[k].keys(): # cascadeID
                    for s in cascades_steps_dist[k][c].keys():  #depth
                        for o in cascades_steps_dist[k][c][s].keys():  #orig
                            fo.write(str(i))
                            fo.write(" \t")
                            fo.write(str(k))
                            fo.write(" \t")
                            fo.write(str(c))
                            fo.write(" \t")
                            fo.write(str(s))
                            fo.write(" \t")
                            fo.write(str(o))
                            fo.write(" \t")
                            fo.write(str(cascades_steps_dist[k][c][s][o][0]))
                            fo.write(" \t")
                            fo.write(str(len(cascades_steps_dist[k][c][s][o][1])))
                            fo.write(" \t")
                            fo.write("\n")                        
                        
                        
#            (steps_dist, cascadesTime) = self.v_sql.extractCascadesSteps(i+1)
#            for k in cascadesTime.keys():
#                fo.write(str(i))
#                fo.write(" \t")
#                fo.write(str(cascadesTime[k][0]))
#                fo.write(" \t")
#                fo.write(str(cascadesTime[k][2]-cascadesTime[k][1]+1))
#                fo.write(" \n")
            
        fo.close()               
        
        
    def ArrayToDict(self, array):
        ret={}
        for i in array:
            ret[i[0]] = i[1:]
        return ret
        
        
    def penNeighborVotedIT(self, startID, endID, option):
        # this function is to retrieve information to test information theory hypothesis
        
        if option==0:
        
            fileName=self.v_dirpath + 'digg_components_neighbors_voted_IT.txt'
            fo = open(fileName, "w+")
            
            fo.write("storyNum \t #neighborVoted \t  friendsNum  \t  caresNum \t total \n")
            for i in range(startID, endID):         # i story_id
                print i#, CNUM
                (voted, total) = self.v_sql.penNeighborVotingIT(i,option)
                Dvoted = self.ArrayToDict(voted)
                Dtotal = self.ArrayToDict(total)      
                
                for k in range(1,51):
                    #a = sum(x==k for x in Dvoted.values())  # find how many infected nodes where each of them voted and has k number of neighbors voted before it.
                    b = sum(x==k for x in Dtotal.values())  # find the total number of nodes where each of them has k number of neighbors voted.
                    #!!! so a/b is the infection probability which is defined as the (#infected nodes with k infected neighbors)/(#nodes with k infected neighbors)
                    
                    for j in Dvoted.values():
                        if j[0]==k:
                            fo.write(str(i))
                            fo.write(" \t")
                            fo.write(str(k))
                            fo.write(" \t")
                            fo.write(str(j[1]))
                            fo.write(" \t")
                            fo.write(str(j[2]))
                            fo.write(" \t")
                            fo.write(str(b))
                            fo.write("\n")
                    
            fo.close()   
                             
        elif option == 1:
            
            fileName=self.v_dirpath + 'digg_components_neighbors_voted_IT_total.txt'
            fo = open(fileName, "w+")
            
            fo.write("storyNum \t #neighborVoted \t  total \n")
            for i in range(startID, endID):         # i story_id
                print i#, CNUM
                (voted, total) = self.v_sql.penNeighborVotingIT(i,option)
                Dvoted = self.ArrayToDict(voted)
                Dtotal = self.ArrayToDict(total)      
                
                for k in range(1,51):
                    a = sum(x==k for x in Dvoted.values())  # find how many infected nodes where each of them voted and has k number of neighbors voted before it.
                    b = sum(x==k for x in Dtotal.values())  # find the total number of nodes where each of them has k number of neighbors voted.
                    #!!! so a/b is the infection probability which is defined as the (#infected nodes with k infected neighbors)/(#nodes with k infected neighbors)
                    
                    fo.write(str(i))
                    fo.write(" \t")
                    fo.write(str(k))
                    fo.write(" \t")
                    fo.write(str(a))
                    fo.write(" \t")
                    fo.write(str(b))
                    fo.write("\n")
                    
            fo.close()   
            
        
        
    def penNeighborVotedComp(self, startID, endID):
        #CNUM=self.v_sql.storiesNum()
        
        # output it
        fileName=self.v_dirpath + 'digg_components_neighbors_voted' + str(startID) + '.txt'
        fo = open(fileName, "w+")
        
        fo.write("storyNum \t #neighborVoted \t  voted  \t total \t votedNeighborsComponents \t totalNeighborsComponents \n")
        
        for i in range(startID, endID):         # i story_id
            print i#, CNUM
            (voted, total) = self.v_sql.penNeighborVoting(i)
            Dvoted = self.ArrayToDict(voted)
            Dtotal = self.ArrayToDict(total)
            for k in range(1,51):
                a = sum(x==k for x in Dvoted.values())  # find how many infected nodes where each of them voted and has k number of neighbors voted before it.
                b = sum(x==k for x in Dtotal.values())  # find the total number of nodes where each of them has k number of neighbors voted.
                #!!! so a/b is the infection probability which is defined as the (#infected nodes with k infected neighbors)/(#nodes with k infected neighbors)
                if b==0:
                    r=-1
                else:  
                    r = float( a ) / float(b )
                    
                # count the components number 
                votedNodeList = [node for node, v in Dvoted.iteritems() if v==k]
                VCN={}
                for j in range(1,51):
                    VCN[j]=0
                for node in votedNodeList:
                    cn = self.v_sql.componentsNum(node, i, 'voted')  # for every node of a, among its neighbors who voted before it, how many components exists
                    VCN[cn] += 1
                    
                totalNodeList = [node for node, v in Dtotal.iteritems() if v==k]
                TCN={}
                for j in range(1,51):
                    TCN[j]=0
                for node in totalNodeList:
                    cn = self.v_sql.componentsNum(node, i, 'total') # for every node of b, among its neighbors who voted, how many components exists within them  
                    TCN[cn] += 1
                     
                fo.write(str(i))
                fo.write(" \t")
                fo.write(str(k))
                fo.write(" \t")
                fo.write(str(a))
                fo.write(" \t")
                fo.write(str(b))
                fo.write(" \t")
                
                for cn in range(1,51):
                    fo.write(str(VCN[cn]))
                    fo.write(" \t")
                    fo.write(str(TCN[cn]))
                    fo.write(" \t")
                
                fo.write("\n")
        fo.close()
        
        
    def storyHistgram(self):
        CNUM=self.v_sql.storiesNum()
        
        # output it
        fileName=self.v_dirpath + 'digg_story_histgram.txt'
        fo = open(fileName, "w+")
        
        fo.write("storyNum \t month \t day \t hour \t hourDiff \t count \n")
        
        startTime=self.v_sql.firstVoteTime()
        
        for i in range(CNUM):
            # for each story
            print i,CNUM            
            # find all cascades of this story
            (ret) = self.v_sql.storyHist(i+1)
            pre_time=[]
            for k in ret:
                fo.write(str(i))
                fo.write(" \t")
                fo.write(str(k[0]))
                fo.write(" \t")
                fo.write(str(k[1]))
                fo.write(" \t")
                fo.write(str(k[2]))
                fo.write(" \t")
                if len(pre_time)==0:
                    hourdiff=self.v_sql.hourDiff(startTime, [k[0],k[1],k[2]])
                else:
                    hourdiff=self.v_sql.hourDiff(pre_time, [k[0],k[1],k[2]])
                pre_time = [k[0],k[1],k[2]]
                fo.write(str(hourdiff))
                fo.write("\t")    
                fo.write(str(k[3]))
                fo.write("\n")
                
        fo.close()      
        
                
    def cascadesSize(self):
        # this function find the #initial_seeds for all cascades
        CNUM=self.v_sql.storiesNum()
        initial_set=[]
        cascade_set=[]
        
        actGCCNodes=[]
        fo = open(self.v_dirpath + 'giant_nodes_actProb_prod.txt', "r")
        line=fo.readline()
        while line:
            actGCCNodes.append(int(line))
            line=fo.readline()
        fo.close()
        
        netinfGCCNodes=[]
        fo = open(self.v_dirpath + 'giant_nodes_netinfProb_prod.txt', "r")
        line=fo.readline()
        while line:
            netinfGCCNodes.append(int(line))
            line=fo.readline()
        fo.close()               
        
        # output it
        fileName=self.v_dirpath + 'initial_cascade_size_Prob_prod.txt'
        fo = open(fileName, "w+")
        
        fo.write("#seeds \t #seedsINactGCC \t #seedsINnetinfGCC \t #infected \t #infectedINactGCC \t #infectedINnetinfGCC \n")
        
        for i in range(CNUM):
            # for each story
            
            # find the initial infected nodes
            (initial_size, initial_seeds, cascade_size, infected_nodes) = self.v_sql.initialNodes(i+1)
            if cascade_size != len(infected_nodes):
                print "wrong", cascade_size, len(infected_nodes)
            initial_set.append(initial_size)
            cascade_set.append(cascade_size)
            
            # find how many initial_seeds in the giant group
            initial_intersect_act_size=len( list( set(actGCCNodes).intersection( set(initial_seeds) ) ) )
            initial_intersect_netinf_size=len( list( set(netinfGCCNodes).intersection( set(initial_seeds) ) ) )
            after_intersect_act_size=len( list( set(actGCCNodes).intersection( set(infected_nodes) ) ) )
            after_intersect_netinf_size=len( list( set(netinfGCCNodes).intersection( set(infected_nodes) ) ) )
            print i,CNUM
            
            fo.write(str(initial_size))
            fo.write(" \t")
            fo.write(str(initial_intersect_act_size))
            fo.write(" \t")
            fo.write(str(initial_intersect_netinf_size))
            fo.write(" \t")
            fo.write(str(cascade_size))
            fo.write(" \t")
            fo.write(str(after_intersect_act_size))
            fo.write(" \t")
            fo.write(str(after_intersect_netinf_size))
            fo.write("\n")
            
        fo.close()
        
        
    def pickGiantGraph(self):
        # this function pick the giant graph according to the giant_nodes.txt
        # the giant_nodes records the id of nodes, giant_nodes_graph records the links among these nodes
        nodes=[]
        fo = open(self.v_dirpath + 'giant_nodes.txt', "r")
        line=fo.readline()
        while line:
            nodes.append(int(line))
            line=fo.readline()
        fo.close()
        
        fo = open(self.v_dirpath + 'giant_nodes_graph.txt', 'w+')
        for i in range(len(nodes)):
            c=nodes[i]
            print i,len(nodes)
            friends=self.v_sql.friends(c)
            for j in range(len(friends)):
                if friends[j][0] in nodes:
                    # add this link 
                    fo.write(str(i+1))
                    fo.write(" ")
                    d=nodes.index(friends[j][0])
                    fo.write(str(d+1))
                    fo.write('\n')
        fo.close()
        
        
    def testGiantComp(self):
        # this function find the statistic information of giant nodes 
        #   such as : how many links are within the group
        
        #read nodes
        nodes=[]
        fo = open(self.v_dirpath + 'giant_nodes.txt', "r")
        line=fo.readline()
        while line:
            nodes.append(int(line))
            line=fo.readline()
        fo.close()
            
        fo = open(self.v_dirpath + 'giant_nodes_sta.txt', 'w+')
        for i in range(len(nodes)):
            print i,len(nodes)
            c=nodes[i]
            within_out=0
            friends=self.v_sql.friends(c)
            for j in range(len(friends)):
                if friends[j][0] in nodes:
                    within_out=within_out+1
            
            within_in=0
            cares=self.v_sql.cares(c)
            for j in range(len(cares)):
                if cares[j][0] in nodes:
                    within_in=within_in+1        
                    
            in_degree = self.v_sql.caresNumU(c)
            out_degree = self.v_sql.friendsNumU(c)
            
            fo.write(str(c))
            fo.write(" ")
            fo.write(str(out_degree))
            fo.write(" ")
            fo.write(str(within_out))
            fo.write(" ")
            fo.write(str(in_degree))
            fo.write(" ")
            fo.write(str(within_in))
            fo.write("\n")
        fo.close()
    
    
    def findGiant(self, prob):
        # the function goes to find giant component according to prob
        # the criteria is to make sure selected candidates have at least 1/prob outgoing links within the group
        e = 0.2
        #degree=int(1.0/prob)
        degree = int( math.log(e)/math.log(1-prob)  )
        degree = 40
        nodes=self.v_sql.giantCandidates(degree)
        candidates=[]
        for i in range(len(nodes)):
            candidates.append(nodes[i][0]) 
        
        print len(candidates)
        
        while True:
            removed=[]
            for i in range(len(candidates)):
                within=0
                c = candidates[i]
                friends=self.v_sql.friends(c)
                for j in range(len(friends)):
                    if friends[j][0] in candidates:
                        within=within+1                
                if within<degree:
                    removed.append(c)
            for i in range(len(removed)):
                candidates.remove(removed[i])
            print len(removed)
            if len(removed)==0:
                break
        
        fo = open(self.v_dirpath + 'giant_nodes.txt', 'w+')
        for i in range(len(candidates)):
            fo.write(str(candidates[i]))
            fo.write('\n')
        fo.close()
        
        
    # find GCC using same_act_prob    
    def findGiantActProb(self):
        nodes=self.v_sql.giantCandidatesActProb()
        candidates=[]
        for i in range(len(nodes)):
            candidates.append(nodes[i][0])         
    
        print len(candidates)
        epsilon=0.01
        while True:
            removed=[]
            for i in range(len(candidates)):
                prob=1
                c = candidates[i]
                friends=self.v_sql.friends(c)
                for j in range(len(friends)):
                    if friends[j][0] in candidates:
                        prob *= (1-self.v_sql.actProb(c, friends[j][0]))
                if 1- prob < 1- epsilon:
                    removed.append(c)
            for i in range(len(removed)):
                candidates.remove(removed[i])
            print len(removed)
            if len(removed)==0:
                break
        
        fo = open(self.v_dirpath + 'giant_nodes_actProb_prod.txt', 'w+')
        for i in range(len(candidates)):
            fo.write(str(candidates[i]))
            fo.write('\n')
        fo.close()    
        
        
    
    # find GCC using netInf prob    
    def findGiantNetInfProb(self):
        nodes=self.v_sql.giantCandidatesNetInfProb()
        candidates=[]
        for i in range(len(nodes)):
            candidates.append(nodes[i][0])         
    
        print len(candidates)
        epsilon=0.01
        while True:
            removed=[]
            for i in range(len(candidates)):
                prob=1
                c = candidates[i]
                friends=self.v_sql.friends(c)
                for j in range(len(friends)):
                    if friends[j][0] in candidates:
                        prob *= (1-self.v_sql.netinfProb(c, friends[j][0]))
                if 1- prob < 1- epsilon:
                    removed.append(c)
            for i in range(len(removed)):
                candidates.remove(removed[i])
            print len(removed)
            if len(removed)==0:
                break
        
        fo = open(self.v_dirpath + 'giant_nodes_netinfProb_prod.txt', 'w+')
        for i in range(len(candidates)):
            fo.write(str(candidates[i]))
            fo.write('\n')
        fo.close()  
    
        
    
    
    def findGiantAdjacency(self):
        # find adjacency nodes of the GCC 
        
        accessed={}
        fo = open(self.v_dirpath + 'giant_nodes_actProb_prod.txt', "r")
        line=fo.readline()
        while line:
            accessed[int(line)]=1
            line=fo.readline()
        fo.close()
        gcc_size = len(accessed)
    
        print len(accessed)
        hops=1
        checking=list(accessed)
        while hops<=5:
            adj={}          
            print "checking:", len(checking)
            nextChecking=[]  
            for c in checking:
                friends=self.v_sql.friends(c)
                for j in range(len(friends)):
                    if friends[j][0] not in accessed.keys():
                        if friends[j][0] not in adj.keys():
                            adj[friends[j][0]]=1-self.v_sql.actProb(c, friends[j][0])*accessed[c]
                        else:
                            adj[friends[j][0]]=(1-self.v_sql.actProb(c, friends[j][0])*accessed[c])*adj[friends[j][0]]
                        
                        if friends[j][0] not in nextChecking:
                            nextChecking.append(friends[j][0])
                            
            checking=list(nextChecking)
            
            for k in adj.keys():
                accessed[k] = 1-adj[k]
                 
            print sum(accessed.values())
            
            hops += 1
            print hops, len(adj)
        
        print len(accessed)
        estNum=0
        for k in accessed.keys():
            estNum += accessed[k]
            
        estNum -= gcc_size
        print estNum
    
    
    def oneCascade(self, seeds, prob, rounds):
        #seeds=[253955]
        candidates=seeds[:];
        accessed=[];
        #degree=self.v_sql.friendsNumU(seeds[0])
        
        while len(candidates)>0:
            #print degree, len(candidates)
            c=candidates.pop()
            # for all edges from this candidate
            friends=self.v_sql.friends(c)
            #degree -= self.v_sql.friendsNumU(c)
            for i in range(len(friends)):
                if friends[i][0] not in accessed and friends[i][0] not in candidates: 
                    r=random.random()
                    if r<prob:
                        candidates.insert(0,friends[i][0])
                        #degree += self.v_sql.friendsNumU(friends[i][0]) 
            
            accessed.append(c)
            
#        if rounds and len(accessed)>2800:
#            #output 
#            fileName=self.v_dirpath + 'cascade_nodes_2800_' + str(rounds) + '.txt'
#            fo = open(fileName, "w+")
#            for i in range(len(accessed)):
#                fo.write(str(accessed[i]))
#                fo.write('\n')
#            fo.close            
            
        return len(accessed)    
    
    
    def loadNeighbors(self, suspicious, parents, accessed):
        for p in parents:
            friends=self.v_sql.friends(p)
            for f in friends:
                if f[0] not in accessed:
                    if f[0] not in suspicious.keys():
                        suspicious[f[0]]=randrange(9)+1
                    else:
                        #multiple nodes infect the same one
                        suspicious[f[0]]+=(randrange(9)+1)*10
        return suspicious


    # include the time, once a node is infected, each neighbor is modelled as a time function to see this information
    def oneWaitingTimeCascade(self, seeds, prob):
        candidates=seeds[:]
        accessed=[seeds[0]]
        suspicious={}
        suspicious=self.loadNeighbors(suspicious, candidates, accessed)
        while len(suspicious)>0:
            
            for s in suspicious.keys():
                suspicious[s] -=1
                if suspicious[s]%10==0:
                    r=random.random()
                    if r<prob:
                        self.loadNeighbors(suspicious, [s], accessed)
                        if s not in accessed:
                            accessed.append(s)
                        del suspicious[s]
                    else:
                        if suspicious[s]>=10:
                            suspicious[s] = suspicious[s] / 10
                        if suspicious[s] == 0:
                            del suspicious[s] 
        return len(accessed)          


    def loadNeighborsProbAct(self, suspicious, parents, accessed):
        for p in parents:
            ret = self.v_sql.actProbs(p)
            for ele in ret:
                if ele[0] not in accessed:
                    prob = ele[1]
                    if ele[0] not in suspicious.keys():
                        suspicious[ele[0]]=[]
                        suspicious[ele[0]].append([randrange(99)+1, prob])
                    else:
                        #multiple nodes infect the same one
                        suspicious[ele[0]].append([randrange(99)+1, prob])                
            
#            friends=self.v_sql.friends(p)
#            for f in friends:
#                if f[0] not in accessed:
#                    prob = self.v_sql.actProb(p, f[0])
#                    if f[0] not in suspicious.keys():
#                        suspicious[f[0]]=[]
#                        suspicious[f[0]].append([randrange(9)+1, prob])
#                    else:
#                        #multiple nodes infect the same one
#                        suspicious[f[0]].append([randrange(9)+1, prob])
        return suspicious
    
    def loadNeighborsProbActDecay(self, suspicious, parents, accessed):
        for p in parents:
            ret = self.v_sql.actProbs(p)
            for ele in ret:
                if ele[0] not in accessed:
                    prob = ele[1]
                    timer = randrange(99)+1
                    #prob *= math.exp(-0.03*timer)
                    if ele[0] not in suspicious.keys():
                        suspicious[ele[0]]=[]
                        suspicious[ele[0]].append([timer, prob])
                    else:
                        #multiple nodes infect the same one
                        suspicious[ele[0]].append([timer, prob])                
            
#            friends=self.v_sql.friends(p)
#            for f in friends:
#                if f[0] not in accessed:
#                    prob = self.v_sql.actProb(p, f[0])
#                    if f[0] not in suspicious.keys():
#                        suspicious[f[0]]=[]
#                        suspicious[f[0]].append([randrange(9)+1, prob])
#                    else:
#                        #multiple nodes infect the same one
#                        suspicious[f[0]].append([randrange(9)+1, prob])
        return suspicious    
    

    def gaussianFit(self, x):
        
        # a1*exp(-((x-b1)/c1)^2) + a2*exp(-((x-b2)/c2)^2) + a3*exp(-((x-b3)/c3)^2)
        a1 =      0.8965
        b1 =       13.34
        c1 =       16.41
        a2 =      0.0347
        b2 =       706.5
        c2 =       423.2
        a3 =  3.115e+011
        b3 = -1.903e+004
        c3 =        3542
        
        y = a1*math.exp(-math.pow( (x-b1)/c1,2 ) ) + a2*math.exp(-math.pow( (x-b2)/c2, 2 ) ) + a3*math.exp(-math.pow( (x-b3)/c3,2 ) )
        return y

    # include the time, once a node is infected, each neighbor is modelled as a time function to see this information
    def oneWaitingTimeCascadeDecay(self, seeds, prob):
        candidates=seeds[:]
        accessed=[seeds[0]]
        suspicious={}
        suspicious=self.loadNeighbors(suspicious, candidates, accessed)
        timestick=0;
        while len(suspicious)>0:
            
            timestick+=1
            for s in suspicious.keys():
                suspicious[s] -=1
                if suspicious[s]%10==0:
                    r=random.random()
                    
                    
                    #prob = prob*self.gaussianFit(timestick)
                    if r<prob*math.exp(-0.03*timestick/10):
                    #if r<prob:
                        self.loadNeighbors(suspicious, [s], accessed)
                        if s not in accessed:
                            accessed.append(s)
                        del suspicious[s]
                    else:
                        if suspicious[s]>=10:
                            suspicious[s] = suspicious[s] / 10
                        if suspicious[s] == 0:
                            del suspicious[s] 
        return len(accessed)    
    
    
    def loadNeighborsProbActLocationDecay(self, suspicious, parents, accessed):
        p=parents[0]
        ret = self.v_sql.actProbs(p)
        location = parents[1][1] + 1
        for ele in ret:
            if ele[0] not in accessed:
                prob = ele[1]
                timer = randrange(99)+1
                #timer=1
                #prob *= math.exp(-0.03*timer -0.2*(location-1))
                prob *= math.exp(-0.2*(location-1))
                if ele[0] not in suspicious.keys():
                    suspicious[ele[0]]=[]
                    suspicious[ele[0]].append([timer, location, prob])
                else:
                    #multiple nodes infect the same one
                    suspicious[ele[0]].append([timer, location, prob])                
            
        return suspicious      

    # include the time, once a node is infected, each neighbor is modelled as a time function to see this information
    def oneWaitingTimeCascadeProbAct(self, seeds):
        candidates=seeds[:]
        accessed=[seeds[0]]
        suspicious={}
        suspicious=self.loadNeighborsProbAct(suspicious, candidates, accessed)
        while len(suspicious)>0:
            
            for s in suspicious.keys():
                suspicious[s][0][0] -=1
                if suspicious[s][0][0]==0:
                    prob = suspicious[s][0][1]
                    r=random.random()
                    if r<prob:
                        self.loadNeighborsProbAct(suspicious, [s], accessed)
                        if s not in accessed:
                            accessed.append(s)
                        del suspicious[s]
                    else:
                        suspicious[s].pop(0)
                        if len(suspicious[s])==0:
                            del suspicious[s]
        return len(accessed)  

    def oneWaitingTimeCascadeProbActDecay(self, seeds):
        candidates=seeds[:]
        accessed=[seeds[0]]
        suspicious={}
        suspicious=self.loadNeighborsProbActDecay(suspicious, candidates, accessed)
        time=0
        while len(suspicious)>0:
            time+=1
            for s in suspicious.keys():
                suspicious[s][0][0] -=1
                if suspicious[s][0][0]==0:
                    prob = suspicious[s][0][1]
                    r=random.random()
                    y=self.gaussianFit(time*1.0/30)
                    if r<prob*y:
                        self.loadNeighborsProbActDecay(suspicious, [s], accessed)
                        if s not in accessed:
                            accessed.append(s)
                        del suspicious[s]
                    else:
                        suspicious[s].pop(0)
                        if len(suspicious[s])==0:
                            del suspicious[s]
        return len(accessed)  


    # include the time, once a node is infected, each neighbor is modelled as a time function to see this information
    def oneWaitingTimeLocationCascadeDecay(self, seeds):
        seeds=[253955]
        accessed=[seeds[0]]
        suspicious={}
        suspicious=self.loadNeighborsProbActLocationDecay(suspicious, [seeds[0],[0,0,0]], accessed)
        timestick=0;
        while len(suspicious)>0:
            timestick+=1
            for s in suspicious.keys():
                suspicious[s][0][0] -=1
                if suspicious[s][0][0]==0:
                    r=random.random()
                    prob = suspicious[s][0][2]
                    if r<prob:
                        self.loadNeighborsProbActLocationDecay(suspicious, [s,suspicious[s][0]], accessed)
                        if s not in accessed:
                            accessed.append(s)
                        del suspicious[s]
                    else:
                        suspicious[s].pop(0)
                        if len(suspicious[s])==0:
                            del suspicious[s] 
        return len(accessed)  
    
    
    def loadNeighborsProbActCome(self, suspicious, parents, accessed, option):
        p=parents[0]
        ret = self.v_sql.actProbs(p)
        for ele in ret:
            if ele[0] not in accessed:
                prob = ele[1]
                if option==self.EXP_TIMER_DECAY:
                    timer = int(random.expovariate(0.03))+1
                    if timer>100:
                        timer=100
                    prob = prob*self.gaussianFit(timer)
                elif option == self.NO_TIMER:
                    timer=1
                    prob *= math.exp(-0.03*timer)
                elif option == self.UNIFORM_TIMER:
                    timer = random.randrange(99)+1
                    prob *= math.exp(-0.03*timer)
                else:
                    timer = int(random.expovariate(0.03))+1
                    if timer>100:
                        timer=100 
                    #prob=0.013
                    
                if ele[0] not in suspicious.keys():
                    suspicious[ele[0]]=[]
                    suspicious[ele[0]].append([timer, prob])
                else:
                    #multiple nodes infect the same one
                    suspicious[ele[0]].append([timer, prob])                
            
        return suspicious   
    
    
    def oneWaitingTimeComeCascade(self, seeds, option):
        #seeds=[253955]
        candidates=seeds[:]
        accessed=[seeds[0]]
        suspicious={}
        
        suspicious=self.loadNeighborsProbActCome(suspicious, candidates, accessed, option)
        while len(suspicious)>0:
            for s in suspicious.keys():
                for ele in suspicious[s]:
                    ele[0] -=1                    
                    # if any timer is triggered
                    if ele[0]<=0:
                        prob = ele[1]
                        r=random.random()
                        if r<prob:
                            self.loadNeighborsProbActCome(suspicious, [s], accessed, option)
                            if s not in accessed:
                                accessed.append(s)
                                del suspicious[s]
                                break
                        else:
                            if option==self.CONS_FRIEND:
                                del suspicious[s]
                                break
                            else:
                                suspicious[s].remove(ele)
                                if len(suspicious[s])==0:
                                    del suspicious[s]
                                    break

        return len(accessed)  
    
    
    def loadNeighborsAssess(self, suspicious, parent, parentTime, location, accessed):
        ret = self.v_sql.actProbs(parent[0])
        for ele in ret:
            if ele[0] not in accessed:
                prob = ele[1]
                if prob > 0:
                    timer = int(random.expovariate(0.11))
                    if timer>100:
                        timer=100
                        
                    if ele[0] not in suspicious.keys():
                        suspicious[ele[0]]=[]
                        suspicious[ele[0]].append([timer + parentTime, parentTime, location+1, prob])
                    else:
                        #multiple nodes infect the same one
                        suspicious[ele[0]].append([timer + parentTime, parentTime, location+1, prob])                
            
        return suspicious         
    
    def logistic(self, f1,f2,f3,f4,f5,f6,f7,f8,f9,f10):
        b0 = 5.868
        b1 = -0.0015
        b2 = -0.0466
        b3 = -2.2591
        b4 = 4.5271
        b5 = -2.1257
        b6 = -0.0441
        b7 = -0.0494
        b8 = 0.0683
        b9 = -1.0311
        b10 = -6.9781        
        
        com = b0*1 + b1*f1 + b2*f2 + b3*f3 + b4*f4 + b5*f5 + b6*f6 + b7*f7 + b8*f8 + b9*f9 + b10*f10
        ret = 1.0/(1+math.exp(-com))
        return ret
    
    def oneAssessmentCascade(self, seeds):
        #seeds=[253955]
        
        candidates=seeds[:]
        accessed=[seeds[0]]
        infected=[seeds[0]]
        suspicious={}
        
        suspicious=self.loadNeighborsAssess(suspicious, candidates, 0, 1, accessed)
        timer=0
        
        
        while len(suspicious)>0:
            timer += 1
            for s in suspicious.keys():  # iterate all suspicious
                for ele in suspicious[s]:
                    # if any timer is triggered, we assess this node according to its environment
                    if ele[0]<=timer:
                        
                        # load features:
                        #f1 = self.v_sql.caresNumU(s)  # total number of neighbors 
                        f2 = len(suspicious[s])  # number of infected neighbors
                        f3 = 0                        # max link weight
                        f4 = 0                        # avg link weight
                        f5 = -1                       # min link weight
                        f6 = 0                        # max infection time of infected neighbors
                        f7 = 0                        # avg infection time of infected neighbors
                        f8 = -1                       # min infection time of infected neighbors
                        f9 = -1                        # location
                        num=0
                        for neighbor in suspicious[s]:
                            #t = neighbor[3] * math.exp(-0.03*neighbor[1]) * math.exp(-0.2*(neighbor[2]-1))
                            t = neighbor[3]
                            # link weight
                            if f3 < t:
                                f3 = neighbor[3]
                                
                            if t >0:
                                f4 += t
                                num += 1
                            
                            if f5 == -1 or f5 > neighbor[3]:
                                f5 = neighbor[3]
                            
                            # elapsed time
                            if f6 < neighbor[1]:
                                f6 = neighbor[1]
                                
                            f7 += neighbor[1]
                            
                            if f8 == -1 or f8 > neighbor[1]:
                                f8 = neighbor[1]
                            
                            if f9 == -1 or f9 > neighbor[2]:
                                f9 = neighbor[2]
                            
                        f4 = 1.0*f4/len(suspicious[s])  
                        f7 = 1.0*f7/len(suspicious[s])  
                        
                        #f10 = 1.0*f2/f1
                        

                        #prob=self.logistic(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10) # this is the probability a node being infected
                        r=random.random()
                        prob = f3;#*math.exp(-0.03*timer -0.2*(f9-2));
                        
                        if r<=prob: # infected
                            self.loadNeighborsAssess(suspicious, [s], timer, f9, accessed)
                            if s not in infected:
                                infected.append(s)
                                if len(infected)%1000==0:
                                    print len(infected)
                                
                        del suspicious[s]  # after classification done, remove the node regardless it's infected or not
                        accessed.append(s)
                        break
        
        
        return len(infected)
    
    
    # sample a cascade according to infection probability changing function
    def oneCascadeTimely(self, seeds, prob):
        candidates=seeds[:];
        accessed=[];
        step=0;
        a=0.1741;
        b=-5.22;
        while len(candidates)>0:
            stepCandidates=list(candidates);
            p = a*math.exp(b*step*0.1)*prob*10; 
            p= math.exp(-0.1*step)*prob
            #p=prob
            while len(stepCandidates)>0:                
                candidates.pop()
                c=stepCandidates.pop()
                # for all edges from this candidate
                friends=self.v_sql.friends(c)
                for i in range(len(friends)):
                    if friends[i][0] not in accessed and friends[i][0] not in candidates: 
                        r=random.random()
                        if r<p:
                            candidates.insert(0,friends[i][0])
                        
                accessed.append(c)
            step +=1;    
            if len(accessed)>1000:
                print p;
        
        return len(accessed)   
        
    
    def oneCascadeProbAct(self, seeds):
        candidates=seeds[:];
        accessed=[];
        while len(candidates)>0:
            c=candidates.pop()
            # for all edges from this candidate
            friends=self.v_sql.friends(c)
            for i in range(len(friends)):
                if friends[i][0] not in accessed and friends[i][0] not in candidates: 
                    r=random.random()
                    prob = self.v_sql.actProb(c, friends[i][0]) # we want to know the prob c infect its follower friends[i][0]
                    if r<prob:
                        candidates.insert(0,friends[i][0])
                    
            accessed.append(c)
            
        return accessed   
        

    def oneCascadeProbAct2(self, seeds):
        candidates=seeds[:];
        accessed=[];
        while len(candidates)>0:
            friends=[]
            tmpCandidates=[]
            for c in candidates:
                friends=friends + self.v_sql.friends(c)  # all nodes could be infected by candidates
            for f in friends:
                f=f[0]
                if f not in accessed and f not in candidates and f not in tmpCandidates:
                    parents = self.v_sql.cares(f)
                    parents = self.filterList(parents)
                    parents = list( set(parents).intersection( set(candidates) ) )
                    r = random.random()
                    prb = 1
                    for p in parents:
                        prb = self.v_sql.actProb(p, f)
                        if r<prb:
                            tmpCandidates.append(f)   # the node has been affected by one of its parent
                            break
            
            accessed = list ( set(candidates).union(set(accessed)) )
            candidates=tmpCandidates
                
        return accessed
   
   
    def filterList(self, L):
        F=[]
        for i in L:
            F.append(i[0])
        return F

    def oneCascadeUniIT(self, seeds):
        lbd=0.013
        candidates=seeds[:];
        accessed=[];
        while len(candidates)>0:
            friends=[]
            tmpCandidates=[]
            for c in candidates:
                friends=friends + self.v_sql.friends(c)
            for f in friends:
                f=f[0]
                if f not in accessed and f not in candidates:
                    origParents = self.v_sql.cares(f)
                    origParents = self.filterList(origParents)
                    parents = list( set(origParents).intersection( set(candidates) ) )
                    r = random.random()
                    #prb = 1
                    #or p in parents:
                        #prb = prb * (1-self.v_sql.actProb(p, f))
                    
                    factor = ( -math.log( 1.0*len(parents)/len(origParents),2 ) )/24
                    
                    prb = (1-math.pow(1-lbd, len(parents)))*factor
                    prbN = 1 - math.exp( math.log(1-prb)/len(parents) )
                    
                    if r<prbN:
                        tmpCandidates.append(f)
            
            accessed = list ( set(candidates).union(set(accessed)) )
            candidates=tmpCandidates
                
        return accessed


    def checkBigCascades(self):
        files = os.listdir(self.v_dirpath)
        #print len(files)
        prefix = 'cascade_nodes_2800'
        commonSet=[]
        nodes={}
        for f in files:
            if string.find(f,prefix)!=-1:
                f = self.v_dirpath + f
                #print f
                fi = open(f, "r")
                lines = fi.read().splitlines()
                #lines = [int(i) for i in lines]
                for i in lines:
                    if int(i) in nodes.keys():
                        nodes[int(i)] += 1
                    else:
                        nodes[int(i)]=1
                        
                #print len(lines)
                if len(commonSet)==0:
                    commonSet=lines
                else:
                    commonSet = list( set(lines).intersection(set(commonSet)) )
                fi.close()
        #print len(commonSet), commonSet
        
        for i in nodes.keys():
            print nodes[i]
        

 
    def sampleCascade(self, seedsNum, option):
        

        
        N=self.v_sql.usersNum()
        
        if option==1:    
        # given seeds, we d sampling.
            prob=0.015
            fileName=self.v_dirpath + 'cascade_size_time_fixed_' + str(seedsNum) + str(prob) +'.txt'
            fo = open(fileName, "w+")
            for j in range(100000):
                
                seeds=[]
                while len(seeds)<seedsNum:
                    c=int(random.random()*N)
                    if c>0:
                        if c not in seeds:
                            uid = self.v_sql.userId(c)
                            seeds.insert(0,uid)            
                
                
                sizes=[]
                for i in range(1):
                    #ret=self.oneCascadeTimely(seeds, prob)
                    ret=self.oneCascade(seeds, prob, j)
                    #ret=self.oneWaitingTimeCascade(seeds, prob)
                    #ret=self.oneWaitingTimeCascadeDecay(seeds, prob)
                    print ret, j
                    sizes.append(ret)
                
                fo.write(str(sizes[i]))
                fo.write('\n')
            
            fo.close()   
            
        elif option==2:
            fileName=self.v_dirpath + 'cascade_size_time_probact_' + str(seedsNum) +'.txt'
            fo = open(fileName, "w+")
            for j in range(100000):
                
                seeds=[]
                while len(seeds)<seedsNum:
                    c=int(random.random()*N)
                    if c>0:
                        if c not in seeds:
                            uid = self.v_sql.userId(c)
                            seeds.insert(0,uid)            
                
                
                sizes=[]
                for i in range(1):
                    #ret=self.oneCascadeTimely(seeds, prob)
                    #ret=self.oneCascade(seeds, prob, j)
                    ret=self.oneWaitingTimeCascadeProbAct(seeds)
                    #ret=self.oneWaitingTimeCascadeDecay(seeds, prob)
                    print ret, j
                    sizes.append(ret)
                
                fo.write(str(sizes[i]))
                fo.write('\n')
            
            fo.close()      
        elif option==3:
            prob=0.013
            #fileName=self.v_dirpath + 'cascade_size_timely_decay_fixed_' + str(seedsNum) +'.txt'
            fileName=self.v_dirpath + 'cascade_size_timely_decay_' + str(seedsNum) +'.txt'
            fo = open(fileName, "w+")
            for j in range(100000):
                
                seeds=[]
                while len(seeds)<seedsNum:
                    c=int(random.random()*N)
                    if c>0:
                        if c not in seeds:
                            uid = self.v_sql.userId(c)
                            seeds.insert(0,uid)            
                
                sizes=[]
                for i in range(1):
                    #ret=self.oneWaitingTimeCascadeDecay(seeds, prob)
                    ret=self.oneCascadeTimely(seeds, prob)
                    print ret, j
                    sizes.append(ret)
                
                fo.write(str(sizes[i]))
                fo.write('\n')
            
            fo.close()
                     
        elif option==4:
            fileName=self.v_dirpath + 'cascade_size_time_decay_probact_' + str(seedsNum) +'.txt'
            fo = open(fileName, "w+")
            for j in range(100000):
                
                seeds=[]
                while len(seeds)<seedsNum:
                    c=int(random.random()*N)
                    if c>0:
                        if c not in seeds:
                            uid = self.v_sql.userId(c)
                            seeds.insert(0,uid)            
                
                sizes=[]
                for i in range(1):
                    ret=self.oneWaitingTimeCascadeProbActDecay(seeds)
                    print ret, j
                    sizes.append(ret)
                
                fo.write(str(sizes[i]))
                fo.write('\n')
            
            fo.close()            
            
        elif option==5:
            fileName=self.v_dirpath + 'cascade_size_time_location_decay_probact_' + str(seedsNum) +'.txt'
            fo = open(fileName, "w+")
            for j in range(100000):
                
                seeds=[]
                while len(seeds)<seedsNum:
                    c=int(random.random()*N)
                    if c>0:
                        if c not in seeds:
                            uid = self.v_sql.userId(c)
                            seeds.insert(0,uid)            
                
                sizes=[]
                for i in range(1):
                    ret=self.oneWaitingTimeLocationCascadeDecay(seeds)
                    print ret, j
                    sizes.append(ret)
                
                fo.write(str(sizes[i]))
                fo.write('\n')
            
            fo.close()             
            
        elif option==6:
            fileName=self.v_dirpath + 'cascade_size_time_instant_come_probact_' + str(seedsNum) +'.txt'
            fo = open(fileName, "w+")
            for j in range(10000):
                
                seeds=[]
                while len(seeds)<seedsNum:
                    c=int(random.random()*N)
                    if c>0:
                        if c not in seeds:
                            uid = self.v_sql.userId(c)
                            seeds.insert(0,uid)            
                
                sizes=[]
                for i in range(1):
                    ret=self.oneWaitingTimeComeCascade(seeds, self.NO_TIMER)
                    print ret, j
                    sizes.append(ret)
                
                fo.write(str(sizes[i]))
                fo.write('\n')
            
            fo.close()     
            
        elif option==7:
            fileName=self.v_dirpath + 'cascade_size_time_exp_come_probact_decay_' + str(seedsNum) +'.txt'
            fo = open(fileName, "w+")
            for j in range(100000):
                
                seeds=[]
                while len(seeds)<seedsNum:
                    c=int(random.random()*N)
                    if c>0:
                        if c not in seeds:
                            uid = self.v_sql.userId(c)
                            seeds.insert(0,uid)            
                
                sizes=[]
                for i in range(1):
                    ret=self.oneWaitingTimeComeCascade(seeds, self.EXP_TIMER_DECAY)
                    print ret, j
                    sizes.append(ret)
                
                fo.write(str(sizes[i]))
                fo.write('\n')
                
        elif option==8:
            fileName=self.v_dirpath + 'cascade_size_constant_friend_effect_fixed_' + str(seedsNum) +'.txt'
            fo = open(fileName, "w+")
            for j in range(100000):
                
                seeds=[]
                while len(seeds)<seedsNum:
                    c=int(random.random()*N)
                    if c>0:
                        if c not in seeds:
                            uid = self.v_sql.userId(c)
                            seeds.insert(0,uid)            
                
                sizes=[]
                for i in range(1):
                    ret=self.oneWaitingTimeComeCascade(seeds, self.CONS_FRIEND)
                    print ret, j
                    sizes.append(ret)
                
                fo.write(str(sizes[i]))
                fo.write('\n')                
                
        elif option==9:
            fileName=self.v_dirpath + 'cascade_size_assess_6.txt'
            fo = open(fileName, "w+")
            seeds=[]
            fileName=self.v_dirpath + 'digg_seeds_sameNodes.txt'
            with open(fileName) as f:
                for line in f:
                    seeds.append( int(line) ) 
            j=0
            for s in seeds:          
                j+=1
                sizes=[]
                for i in range(1):
                    ret=self.oneAssessmentCascade([s])
                    print ret, j
                    sizes.append(ret)
                
                fo.write(str(sizes[i]))
                fo.write('\n')            
            
            fo.close()              
            
        elif option==10:
            fileName=self.v_dirpath + 'cascade_size_assess_7.txt'
            fo = open(fileName, "w+")
            for j in range(10000):
                
                seeds=[]
                while len(seeds)<seedsNum:
                    c=int(random.random()*N)
                    if c>0:
                        if c not in seeds:
                            uid = self.v_sql.userId(c)
                            seeds.insert(0,uid)            
                
                sizes=[]
                for i in range(1):
                    ret=self.oneAssessmentCascade(seeds)
                    print ret, j
                    sizes.append(ret)
                
                fo.write(str(sizes[i]))
                fo.write('\n')               
                           
       

    # sample cascades according to probability derived from actionNum
    def sampleCascadeProb2(self, samples):
        N=self.v_sql.usersNum()

        fileName=self.v_dirpath + 'cascade_size_dist_prob.txt'
        fo=open(fileName, "w+")
        for i in range(samples):
            seeds=[]  # only use one seed
            while len(seeds)<1:
                c=int(random.random()*N)
                if c not in seeds:
                    uid = self.v_sql.userId(c)
                    seeds.insert(0,uid)
 
            infected=self.oneCascadeProbAct(seeds)
            fo.write(str(len(infected)))
            fo.write("\n")
            print i,"/",samples,"/",len(infected)
        fo.close()
        
        
    # sample cascades with Information Uncertainty Decay
    def sampleCascadeUniIT(self, samples):
        N=self.v_sql.usersNum()

        fileName=self.v_dirpath + 'cascade_size_dist_IT.txt'
        fo=open(fileName, "w+")
        for i in range(samples):
            seeds=[]  # only use one seed
            while len(seeds)<1:
                c=int(random.random()*N)
                if c not in seeds:
                    uid = self.v_sql.userId(c)
                    seeds.insert(0,uid)
 
            infected=self.oneCascadeUniIT(seeds)
            fo.write(str(len(infected)))
            fo.write("\n")
            print i,"/",samples,"/",len(infected)
        fo.close()        
        
        
    # sample cascades accoring to probability derived from actionNUm
    def sampleCascadeProb(self, seedsNums):
        
        N=self.v_sql.usersNum()
        # given seeds, we d sampling.
        
        nodes=[]
        fo = open(self.v_dirpath + 'giant_nodes_actProb_prod.txt', "r")
        line=fo.readline()
        while line:
            nodes.append(int(line))
            line=fo.readline()
        fo.close()        
        
        fileName=self.v_dirpath + 'cascade_size_prob_t' + str(seedsNums[0]) + '.txt'
        fo = open(fileName, "w+")        
        
        for i in seedsNums:
            if i < 100:
                samples = max(10, 100/i)
            else:
                samples = max(2, 1000/i)
            
            for j in range(samples):
                
                seeds=[]
                while len(seeds)<i:
                    c=int(random.random()*N)
                    if c not in seeds:
                        uid = self.v_sql.userId(c)
                        seeds.insert(0,uid)            
            
                infected=self.oneCascadeProbAct(seeds)
                initial_intersect_size=len( list( set(nodes).intersection( set(seeds) ) ) )
                after_intersect_size=len( list( set(nodes).intersection( set(infected) ) ) )
                    #ret=self.oneCascade(seeds, 0.02, j)
                print i, j, len(infected),  initial_intersect_size, after_intersect_size
            
                #output the result into a file
                fo.write(str(i))
                fo.write(" ")
                fo.write(str(len(infected)))
                fo.write(" ")
                fo.write(str(initial_intersect_size))
                fo.write(" ")
                fo.write(str(after_intersect_size))
                fo.write('\n')
                
        fo.close()               
        
          

        




    def prob(self, seedsNum, extraNum, M):
        # find the probability of infecting extraNum nodes
        
        #N=len(M)
        N=self.v_sql.usersNum()
        seeds=[]
        while len(seeds)<seedsNum:
            c=int(random.random()*N)
            if c not in seeds:
                uid = self.v_sql.userId(c)
                seeds.insert(0,uid)              
        seeds.insert(0,0)
        
        results=[]
        results_nodes=[]
        queue=[]
        self.DFS(seeds, extraNum, results, results_nodes, queue, M)
        
        # calculate prob
        pr=0
        N=len(M)
        for i in range(len(results)): # for each queue
            tmp=1
            for j in range(len(results[i])): # for each edge
                r = results[i][j][0]
                l = results[i][j][1]
                tmp = tmp * M[r][l]
                
            #calculate the complimentary edges' probability
            comp=1;    
            for j in range(len(results_nodes[i])):
                c=results_nodes[i][j]
                for k in range(N):
                    e=[c,k]
                    if M[c][k]>0 and (e not in results[i]):
                        comp=comp*(1-M[c][k])
                
            pr = pr + tmp*comp
        return pr
        
        
    def existSet(self, queue, results):
        for i in range(len(results)):
            ret=1
            for j in range(len(queue)):
                if queue[j] not in results[i]:
                    ret=0
            if ret==1:
                return 1
        return 0
        
        
    def DFS(self, infected, extraNum, results, results_nodes, queue):
        myqueue = queue[:]
        myinfected = infected[:]
        #N=len(M)
        
        for i in range(len(myinfected)):
            c=myinfected[i]
            #for j in range(N): # for all neighbors of c
            friends=self.v_sql.friends(c)
            for j in range(len(friends)):
                #if M[c][friends[j]]>0 and (friends[j] not in myinfected):
                if friends[j] not in myinfected:
                    myinfected.append(friends[j])
                    myqueue.append([c,friends[j]])
                    if extraNum==1:
                        if self.existSet(myqueue, results)==0:
                            results.append(myqueue) # find one
                            results_nodes.append(myinfected)
                        myqueue=queue[:]
                        myinfected=infected[:]
                    else:
                        self.DFS(myinfected, extraNum-1, results, results_nodes, myqueue)
                        myqueue=queue[:]
                        myinfected=infected[:]  
                        


    def pageRank(self):
        return
    
    
    
class DiggThread(threading.Thread):
    def __init__(self, seedsNums):
        threading.Thread.__init__(self)
        self.seedsNums=seedsNums
        self.digg=DIGG()
        
    def run(self):
        self.digg.sampleCascadeProb(self.seedsNums)


def actProbCascadThreading():
    seedsNums={}
    i=1
    while i < 1000:
        if i/100 not in seedsNums.keys():
            seedsNums[i/100]=[]
            seedsNums[i/100].append(i)
        else:
            seedsNums[i/100].append(i)
            
        if i==1:
            i=10
        else:
            i += 10                
   
         
    for i in range(10):
        thread=DiggThread(seedsNums[i])
        thread.start()
            

def main(argv):
    optlist,args=getopt.getopt(argv,'')
    digg=DIGG()
    #digg.createTabs()
    #digg.loadCSVFiles()
    #digg.createTabUsers()
    #digg.createTabVotes()
    #digg.loadFriendsCSVFiles()
    #digg.loadVotesCSVFiles()
    #digg.createTabConnVotes()
    #digg.updateFriendsNum()
    #digg.updateCaresNum()
    #digg.outputFriendsNum()

    #digg.cascadesSize()
    #digg.sampleCascade(1,10)
    #digg.infectionTimeDistribution()
    #digg.infectionFeatures()
    #digg.infectionFeaturesSameNodes()
    #digg.infectionTimeDiffDistributionPerLocation()
    #digg.infectionTimeDistribution()
    #digg.cascadesSteps()
    #digg.cascadesDistribution()

    #digg.penNeighborVoted(int(args[0]), int(args[1]))
    #digg.penNeighborVotedIT(1, 3554, 1)
    #digg.sampleCascadeProb2(1780522)
    #digg.sampleCascadeUniIT(1780522)
    
    #digg.cascadesDistribution()
    
    #digg.findGiantActProb()
    #digg.findGiantAdjacency()
    
    #digg.updateProbabilityNetInf()
    #digg.storyHistgram()
    #digg.cascadesDistribution()
    #digg.cascadesProbabilityDistribution()
    #actProbCascadThreading()
    #digg.outputActProbHist()
    
    #digg.findGiant(0.013)
    #digg.checkBigCascades()
    #digg.testGiantComp()
    
    #digg.updateProbabilitySameAct()
    #digg.pickGiantGraph()
    
    #M=[[0, 0.02, 0.02, 0, 0, 0], [0, 0, 0, 0, 0.02, 0.02], [0, 0, 0, 0.02, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    #M=[[0, 0.02, 0.02], [0, 0, 0.02], [0, 0, 0]]
    #pr = digg.prob(0,1,M)
    #print pr
    
    
if __name__ == '__main__':
    main(sys.argv[1:])
