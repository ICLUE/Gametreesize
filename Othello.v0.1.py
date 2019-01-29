# Othello program: Importance Sampling Estimator v0.1
# Code for "An estimation method for game complexity"
# By Alexander Yong and David Yong @ Urbana, Illinois
# January 28, 2019

import random
import math
import time
import sys
import copy
import multiprocessing

bigtotal=0
firstwintotal=0
secondwintotal=0
drawtotal=0
totalgamelength=0

def main():		
        sampleval=int(input('Sample size : '))
        numberofprocessors=int(input('Number of processor cores to use (0 if you want to use all) : '))
        print("Sample size; cores used", sampleval, numberofprocessors)
        theans=actualestimator(sampleval, numberofprocessors)

def startingposition():
	y=[["_","_","_","_","_","_","_","_"],
           ["_","_","_","_","_","_","_","_"],
	   ["_","_","_","_","_","_","_","_"],
	   ["_","_","_","1","0","_","_","_"],
           ["_","_","_","0","1","_","_","_"],
	   ["_","_","_","_","_","_","_","_"],
           ["_","_","_","_","_","_","_","_"],
	   ["_","_","_","_","_","_","_","_"]]
	import numpy as np
	z=np.reshape(y,(8,8))
	return z;

def makemove(theposition,rowval,colval,tomove):
	
	newpos=copy.deepcopy(theposition)
	if(newpos[rowval,colval]<>"_"):
		return -911
	else:
		nottomove=1-tomove
		islegal=0

		# look below
		if(rowval<7):
			if(newpos[rowval+1,colval]==str(nottomove)):
				stillok=1
				doneflag=0
				currow=rowval+1
				while(stillok==1 and doneflag==0 and currow<=7):
					if(newpos[currow,colval]=="_"):
						stillok=0
						doneflag=1
					elif(newpos[currow,colval]==str(nottomove)):
						if(currow<7):
							currow=currow+1
						else:
							stillok=0
					else:
						bottomflip=currow-1	
						doneflag=1
				if(stillok==1):
					newpos[rowval,colval]=tomove

					# now flip the in-between stuff
					for yyy in range(rowval+1,bottomflip+1):
						newpos[yyy,colval]=str(tomove)
					islegal=1

		#look up
		if(rowval>0):
		   if(newpos[rowval-1,colval]==str(nottomove)):
			stillok=1
			doneflag=0
			currow=rowval-1
			while(stillok==1 and doneflag==0 and currow>=0):
				if(newpos[currow,colval]=="_"):
					stillok=0
					doneflag=1
				elif(newpos[currow,colval]==str(nottomove)):
					if(currow>0):
						currow=currow-1
					else:
						stillok=0	
				else:
					topflip=currow+1
					doneflag=1
			if(stillok==1):
				newpos[rowval,colval]=tomove

				# now flip the in-between stuff
				for yyy in range(topflip,rowval):
					newpos[yyy,colval]=str(tomove)
				islegal=1

		#look right
		if(colval<7):
		   if(newpos[rowval,colval+1]==str(nottomove)):
			stillok=1
			doneflag=0
			curcol=colval+1
			while(stillok==1 and doneflag==0 and curcol<=7):
				if(newpos[rowval,curcol]=="_"):
					stillok=0
					doneflag=1
				elif(newpos[rowval,curcol]==str(nottomove)):
					if(curcol<7):
						curcol=curcol+1
					else:
						stillok=0
				else:
					rightflip=curcol-1
					doneflag=1
			if(stillok==1):
				newpos[rowval,colval]=tomove
				# now flip the in-between stuff
				for yyy in range(colval,rightflip+1):
					newpos[rowval,yyy]=str(tomove)
				islegal=1

		#look left
		if(colval>0):
		    if(newpos[rowval,colval-1]==str(nottomove)):
			stillok=1
			doneflag=0
			curcol=colval-1
			while(stillok==1 and doneflag==0 and curcol>=0):
				if(newpos[rowval,curcol]=="_"):
					stillok=0
					doneflag=1
				elif(newpos[rowval,curcol]==str(nottomove)):
					if(curcol>0):
						curcol=curcol-1
					else:
						stillok=0
				else:
					leftflip=curcol+1
					doneflag=1
			if(stillok==1):
				newpos[rowval,colval]=tomove
                                # now flip the in-between stuff
                                for yyy in range(leftflip,colval):
                                       newpos[rowval,yyy]=str(tomove)
                                islegal=1

		#look southwest
		if(colval>0 and rowval<7):
                    if(newpos[rowval+1,colval-1]==str(nottomove)):
                        stillok=1
                        doneflag=0
                        curcol=colval-1
			currow=rowval+1
                        while(stillok==1 and doneflag==0 and curcol>=0 and currow<=7):
                                if(newpos[currow,curcol]=="_"):
                                        stillok=0
                                        doneflag=1
                                elif(newpos[currow,curcol]==str(nottomove)):
					if(curcol>0 and currow<7):	
                                        	curcol=curcol-1
						currow=currow+1
					else:
						stillok=0
                                else:
					southwestflip=currow-1
                                        doneflag=1
                        if(stillok==1):
                                newpos[rowval,colval]=tomove
                                # now flip the in-between stuff
                                for yyy in range(rowval+1,southwestflip+1):
                                       newpos[yyy,colval-(yyy-rowval)]=str(tomove)
                                islegal=1

		#look northeast
		if(colval<7 and rowval>0):
                    if(newpos[rowval-1,colval+1]==str(nottomove)):
                        stillok=1
                        doneflag=0
                        curcol=colval+1
                        currow=rowval-1
                        while(stillok==1 and doneflag==0 and curcol<=7 and currow>=0):
                                if(newpos[currow,curcol]=="_"):
                                        stillok=0
                                        doneflag=1
                                elif(newpos[currow,curcol]==str(nottomove)):
					if(curcol<7 and currow>0):
                                        	curcol=curcol+1
                                        	currow=currow-1
					else:
						stillok=0
                                else:
					northeastflip=curcol-1
                                        doneflag=1
                        if(stillok==1):
                                newpos[rowval,colval]=tomove
                                # now flip the in-between stuff
                                for yyy in range(colval+1,northeastflip+1):
                                       newpos[rowval-(yyy-colval),yyy]=str(tomove)
                                islegal=1

		#look southeast
		if(colval<7 and rowval<7):
                    if(newpos[rowval+1,colval+1]==str(nottomove)):
                        stillok=1
                        doneflag=0
                        curcol=colval+1
                        currow=rowval+1
                        while(stillok==1 and doneflag==0 and curcol<=7 and currow<=7):
                                if(newpos[currow,curcol]=="_"):
                                        stillok=0
                                        doneflag=1
                                elif(newpos[currow,curcol]==str(nottomove)):
					if(curcol<7 and currow<7):
                                        	curcol=curcol+1
                                        	currow=currow+1
					else:
						stillok=0
                                else:
					southeastflip=currow-1
                                        doneflag=1
                        if(stillok==1):
                                newpos[rowval,colval]=tomove
                                # now flip the in-between stuff
                                for yyy in range(rowval+1,southeastflip+1):
                                       newpos[yyy,colval+(yyy-rowval)]=str(tomove)
                                islegal=1

		#look northwest
		if(colval>0 and rowval>0):
                    if(newpos[rowval-1,colval-1]==str(nottomove)):
                        stillok=1
                        doneflag=0
                        curcol=colval-1
                        currow=rowval-1
                        while(stillok==1 and doneflag==0 and curcol>=0 and currow>=0):
                                if(newpos[currow,curcol]=="_"):
                                        stillok=0
                                        doneflag=1
                                elif(newpos[currow,curcol]==str(nottomove)):
					if(curcol>0 and currow>0):
                                        	curcol=curcol-1
                                        	currow=currow-1
					else:	
						stillok=0
                                else:
					northwestflip=currow+1
                                        doneflag=1
                        if(stillok==1):
                                newpos[rowval,colval]=tomove
                                # now flip the in-between stuff
                                for yyy in range(northwestflip,rowval):
                                       newpos[yyy,curcol+1+(yyy-northwestflip)]=str(tomove)
                                islegal=1

		if(islegal==0):
			return -911
		
	return newpos;

def getallmoves(theposition, tomove):
	legalmovespossible=[]
	for rr in range(0,8):
		for cc in range(0,8):
			temppos=copy.deepcopy(theposition)
			temp = makemove(temppos, rr, cc, tomove) 
			if(temp<>-911):
				legalmovespossible.append([rr, cc])

	return legalmovespossible

def randommove(theposition, tomove):

	movelist=[]
	temppos=copy.deepcopy(theposition)
	movelist=getallmoves(theposition,tomove)
	if(len(movelist)>0):
		randval=random.randint(0,len(movelist)-1)
                themovewemake=movelist[randval]
                anothertemppos=copy.deepcopy(theposition)
                finalanswer=makemove(anothertemppos,themovewemake[0],themovewemake[1],tomove)
                morefinalpos=copy.deepcopy(finalanswer)
                return [morefinalpos, len(movelist)]	
	else:
		return [0,0]		

def checkwinner(theposition):

    numones=0
    numzeros=0
    for ii in range (0,8):
        for jj in range (0,8):
            if(theposition[ii,jj]=="1"):
                numones=numones+1
            if(theposition[ii,jj]=="0"):
                numzeros=numzeros+1
    if numzeros>numones:
        return 0
    if numzeros<numones:
        return 1
    if numzeros==numones:
        return -1

def checkgameended(theposition):
	temppos1=copy.deepcopy(theposition)
	onemove=randommove(temppos1,1)
	temppos0=copy.deepcopy(theposition)
	zeromove=randommove(temppos0,0)
	if(onemove[1]==0 and zeromove[1]==0):
		return 1
	else:
		return 0	

def actualestimator(samplevalin, numberofprocessors, seed=None):

	global totalgamelength
	global bigtotal
	global gamelengthlist
	global firstwintotal
	global secondwintotal
	global drawtotal
	
	start=time.time()

	if seed is not None:
		random.seed(seed)

        if(numberofprocessors==0):
                num_workers = multiprocessing.cpu_count()
        else:
                num_workers=numberofprocessors

	sampleval=samplevalin

	while sampleval > 10000:
		pool=multiprocessing.Pool(num_workers)
        	for i in range(10000):
            		a = pool.apply_async(run_trial, args=(), callback=process_result)
        	pool.close()
        	pool.join()
        	sampleval -= 10000
    	pool = multiprocessing.Pool(num_workers)
    	for i in range(sampleval):
        	a = pool.apply_async(run_trial, args=(), callback=process_result)
    	pool.close()
    	pool.join()

	print("--------------------------------------")
	print("            RESULTS                   ")
	print("--------------------------------------")

	averageestimate=bigtotal/float(samplevalin)
	sumofgamelengths=totalgamelength/float(samplevalin)
	drawtotal=drawtotal/float(samplevalin)
	firstwintotal=firstwintotal/float(samplevalin)
	secondwintotal=secondwintotal/float(samplevalin)

	print("* Estimated number of games of Othello is", float(averageestimate))

	estgamelength=sumofgamelengths/averageestimate
	print("* Estimated average game length is ", float(estgamelength))

	estfirstwinpercent=firstwintotal/float(averageestimate)
	print("* Estimated percentage of first player wins is ", estfirstwinpercent)

	estsecondwinpercent=secondwintotal/float(averageestimate)
	print("* Estimated percentage of second player wins is ", estsecondwinpercent)

	estdrawpercent=drawtotal/float(averageestimate)
	print("* Estimated percentage of draws is ", estdrawpercent)

	end=time.time()
	print('Executed in seconds: ', end - start)

def run_trial():
	z=startingposition()
	thepos=z
	tomove=0
	con=1
	estimate=1
	gamelength=0
	gameended=0

	while con == 1:
		randommovepos=copy.deepcopy(thepos)
		tempans=randommove(thepos,tomove)
		if(tempans[1]<>0):
			thepos=copy.deepcopy(tempans[0])
			estimate=estimate*tempans[1]
                	gamelength=gamelength+1
			flag=0
		else:
			flag=0

		gameended=checkgameended(thepos)
		if gameended==1:
    			whowon=checkwinner(thepos)
			if whowon==0:
				con=0
			elif whowon==1:
				con=0
			elif whowon==-1:
				con=0
		if tomove==0:
			tomove=1
		else:
			tomove=0

	return(estimate,whowon, gamelength)

def process_result(thepair):

	global totalgamelength
	global bigtotal
	global firstwintotal
	global secondwintotal
	global drawtotal

	estimate=thepair[0]
	thewinner=thepair[1]
	thelength=thepair[2]
	bigtotal=bigtotal+float(estimate)

	totalgamelength = totalgamelength+float(thelength*estimate)

	if(thewinner==0):
		firstwintotal=float(firstwintotal+estimate)

	if(thewinner==1):
		secondwintotal=float(secondwintotal+estimate)

        if(thewinner==-1):
                drawtotal=float(drawtotal+estimate)

if __name__ == '__main__':
    main()
