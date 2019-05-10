import tushare as ts
import datetime
import calendar
import os
import time

Savedir="D:\\download\\Doc\\MLshare\\data\\";




#load zz500 and save to csv
zz500s_list=ts.get_zz500s()
zz500s_list.to_csv("D:\\download\\Doc\\MLshare\\data\\zz500s.csv")


#load zz500 and save to csv
stock_basics = ts.get_stock_basics()
stock_basics.to_csv("D:\\download\\Doc\\MLshare\\data\\stock_basics.csv")


#load zz500 history by month to csv



def DownloadToFile(Scode,Startdate,Enddate=None):
    try:
        
       
        if Enddate==None or Enddate>Startdate+datetime.timedelta(days=calendar.monthrange(Startdate.year, Startdate.month)[1]-1):
            Enddate=Startdate+datetime.timedelta(days=calendar.monthrange(Startdate.year, Startdate.month)[1]-1)
            if Enddate>datetime.datetime.now():Enddate=datetime.datetime.now()
    
            
        Startdate_S1=Startdate.strftime("%Y_%m_%d")
        Enddate_S1  =Enddate.strftime("%Y_%m_%d")
            
        Startdate_S2=Startdate.strftime("%Y-%m-%d")
        Enddate_S2  =Enddate.strftime("%Y-%m-%d")
    
        print("Downloading:",Scode,Startdate_S1,Enddate_S1)
    
    
        if Startdate<datetime.datetime.strptime(str(stock_basics.ix[Scode]['timeToMarket']),"%Y%m%d"):  
            print(">>>>Downloading:",Scode,Startdate_S1,Enddate_S1,'Start<2market')
            return(True)
        tofilename=Savedir+"{Scode}_{Startdate_S1}_{Enddate_S1}.csv".format(Scode=Scode,Startdate_S1=Startdate_S1,Enddate_S1=Enddate_S1)
        if os.path.isfile(tofilename):
            print(">>>>Downloading:",Scode,Startdate_S1,Enddate_S1,'alreadydownload')
            return(True)
    
        files=os.listdir(Savedir)
        scodefile=[x for x in files if x[:(len(Scode)+11)]==Scode+'_'+Startdate_S1 ]
        for tmpf in scodefile:
            os.remove(Savedir+tmpf)
            print("remove:",Savedir,tmpf)
    

        tmphs=ts.get_hist_data(Scode, start=Startdate_S2, end=Enddate_S2)
        if tmphs.shape[0]>0:tmphs.to_csv(tofilename)
    except Exception as e:
        print("Exception:",e)
        return(False)
    else:
        print(">>>>Downloading:",Scode,Startdate_S1,Enddate_S1,"Shape:",tmphs.shape,'Done')
        return(True)




def downloadallfile(Scodelist):

        
    for Scode in Scodelist:
        Enddate  =datetime.datetime(2008,1,1)+datetime.timedelta(days=-1)

        while(1):
            Startdate=Enddate+datetime.timedelta(days= 1)
            Enddate  =Startdate+datetime.timedelta(days=calendar.monthrange(Startdate.year, Startdate.month)[1]-1)
            if Enddate+datetime.timedelta(days=1)>datetime.datetime.now():break
            
            try3times=1
            while(try3times<=3):
                print("Try Scode:",try3times);
                dresult=DownloadToFile(Scode,Startdate,Enddate)
                if dresult==True:break
                time.sleep(5)
                try3times=try3times+1


    return(True);


tmpd=downloadallfile(zz500s_list['code'])
        
        
