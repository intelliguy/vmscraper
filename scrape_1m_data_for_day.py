#!/usr/bin/python3

import requests, json, pickle, sys, getopt, time
import os.path
from os import path

MINDATAFILE='/home/siim/bithumb/vmhistory.pickle'
#MINDATAFILE='rawdata.pickle'
TOP30VM=[
  "USDT", "BTC", "ETH", "USDC", "BUSD", "VNDC", "WETH", "GGT", "BNB", "SOL", "TRX", "XRP", "ABC", "ADA", "FLEX", "ZT", "BTMC", "DAI", "WBTC", "LINK", "AVAX", "DOGE", "LTC", "DOT", "MANA", "MATIC", "SHIB", "GMT", "BCH", "APE"
]

def do_request(url, payload = {} ):
  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
  }
  if len(payload) > 0:
    response = requests.get(url, json=payload, headers=headers)
  else:
    response = requests.get(url, headers=headers)

  return json.loads(response.text)

# 차트 간격, 기본값 : 24h {1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h 사용 가능
def get_candlestick(code, interval):
  return do_request("https://api.bithumb.com/public/candlestick/"+code+"_KRW/"+interval)

def get_price():
  return do_request("https://api.bithumb.com/public/ticker/ALL_KRW")

#######################################
## 1분 데이터를 가져옴, bithumb에서 최대 1500개의 데이터를 넘겨주고 이는 하루를 조금 넘기는 데이터
def scrape_1m_data_for_day(picklefile):
  if path.exists(picklefile):
    ## load pickle file
    # open a file, where you stored the pickled data
    file = open(picklefile, 'rb')
    # dump information to that file
    data = pickle.load(file)
    # close the file
    file.close()

    # print('Showing the pickled data:')
    # for k in data.keys():
    #   print('The vmcode ', k, ' have ', len(data[k]),' recodes')
  else:
    data={}
    handlelist=get_price()['data']
    for k in TOP30VM:
      if(handlelist.get(k)!=None):
        data[k]={}

  from datetime import datetime

  print ('> scrape is launched: '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

  for k in data.keys():  
    if len(data[k])>0:
      print(f'{k}: data size from {len(data[k])}', end =" ")
    else:
      print(f'{k}: first scrape', end =" ")
    permin=get_candlestick(k,'1m')
    for record in permin['data']:
      data[k][record[0]]=record[1:]

    since=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(list(sorted(data[k].keys()))[0]/1000))
    print (f'to {len(data[k])} since {since}')

  ## save pickle file
  # open a file, where you ant to store the data
  file = open(picklefile, 'wb')
  # dump information to that file
  pickle.dump(data, file)
  # close the file
  file.close()

def printhelp():
  print(('''scape price history for top 30 major coins from bithumb

    Usage:{0} -d PICKLE
     -d --data=PICKLE   the pickle file name. It generates or appends data to the file depends on existance. 
     
    Examples:
     - {0} -d /tmp/myfile.pickle
    ''').format(sys.argv[0]))

def main(argv):
  pfile='/home/siim/bithumb/vmhistory.pickle'
  try:
    opts, args = getopt.getopt(argv,"d:",["data=","base=","workflow=","kubeconfig=","output=","verbose="])
  except getopt.GetoptError:
    printhelp()
    sys.exit(-1)
  
  for opt, arg in opts:
    if opt == '-h':
      printhelp()
      sys.exit(0)
    elif opt in ("-d", "--data"):
      pfile = arg

  scrape_1m_data_for_day(pfile)


if __name__ == "__main__":
  main(sys.argv[1:])
