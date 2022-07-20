from SearchEngines.Google import Google
from Tools import GetCSV

googleSE = Google("Past hour","Machine Learning", 2, "https://www.google.com/search?q=&source=lnms&tbm=nws")
GetCSV.get_CSV(googleSE.Start(),"Machine Learnig","Past hour")
