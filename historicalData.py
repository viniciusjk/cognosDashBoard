#%%
import pandas as pd
import os 
import datetime as dt
import xlsxwriter

#%%
def getInFolder(directoryName):
    os.chdir(directoryName)


def listFilesInDirectory():
    return [file for file in os.listdir() if os.path.isfile(file)]

def getAssetListFiles(files):
    assetList = [file for file in files if file[11:-5]=='assetList']
    assetList.sort()
    return assetList

def getHistoricalFiles(files):
    historicalList = [file for file in files if file[11:-5]=='historicalData']
    historicalList.sort()
    return historicalList

def convertKWtoFloat(f):
    try:
        f.KW_Load = f.KW_Load.str.replace(',','.').apply(float)

    except:
        f.KW_Load = f.KW_Load.apply(float)

    
    return f

def pivotHistoricalData(assetListNames):
    df = pd.read_excel(assetListNames, sheet_name='list')
    df.loc[:,'dateReport'] = assetListNames[:10]
    df.dateReport = pd.to_datetime(df.dateReport, dayfirst=False)
    df = convertKWtoFloat(df)
    isActive = df.Asset_Operational_Status.str.contains('Active')
    df = df.loc[isActive,:]
    pivot = df.pivot_table(index=['dateReport', 'City'], values=['KW_Load', 'AssetID'], aggfunc={'KW_Load':sum, 'AssetID':len}).reset_index()
    return pivot

def write2Excel(tables, sheetsName, filename, columnsList, index):

    today = dt.datetime.strftime(dt.datetime.today(), '%Y-%m-%d_')
    def convert_range(x):
        return 'A1:'+xlsxwriter.utility.xl_col_to_name(x[1]-1)+str(x[0]+1)
    w = pd.ExcelWriter(today+filename+'.xlsx', engine='xlsxwriter')
    for tab, name, index, columns in zip(tables, sheetsName, index, columnsList):
        headers = []
        for i in columns:
            headers.append({'header': i})
        tab.to_excel(w, sheet_name=name, index=index)
        sh = w.sheets[name]
        if not(index):
            sh.add_table(convert_range(tab.shape),{'header_row': 1,'columns': headers})
    w.save()



def historicalLastToday(historicalList):

    today = dt.datetime.strftime(dt.datetime.today(), '%Y-%m-%d')
    return today  == historicalList[-1][0:10]

#%%

def historicalMerge():

    files = listFilesInDirectory()
    assetList = getAssetListFiles(files)
    historicalList = getHistoricalFiles(files)
    pivot = pivotHistoricalData(assetList[-1])
    if historicalLastToday(historicalList):
        historicalDf = pd.read_excel(historicalList[-2])
        
    else:
        historicalDf = pd.read_excel(historicalList[-1])
        

    historicalDf.dateReport = pd.to_datetime(historicalDf.dateReport, dayfirst=False)


    historicalDf = pd.concat([historicalDf, pivot])

    write2Excel(tables=[historicalDf], sheetsName=['historicalData'], filename='historicalData', columnsList=[['dateReport', 'City', 'AssetID', 'KW_Load']], index=[False])

def createNewHistoricalFile():
    historicalDf = pd.DataFrame(columns=['dateReport', 'City', 'AssetID', 'KW_Load'])
    today = dt.datetime.strftime(dt.datetime.today(), '%Y-%m-%d_')
    historicalDf.to_excel(today+'historicalData.xlsx', sheet_name='historicalData', index=False)




def main():
    try:
        historicalMerge()
    except:
        createNewHistoricalFile()
        historicalMerge()
#%%
if __name__ == '__main__':
    main()





#%%



#%%
