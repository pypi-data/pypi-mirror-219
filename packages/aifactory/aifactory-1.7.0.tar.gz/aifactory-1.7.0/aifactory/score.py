import os
import requests
import zipfile
import subprocess
import gdown
import time
import json
from IPython import get_ipython
import ipynbname

bridge_url = "https://grade-bridge.aifactory.space/grade"
bridge_test_url = "https://grade-bridge-test.aifactory.space/grade"

api_url = "https://api.aifactory.space/competition-submission/getResultByRequestID/"
api_test_url = "https://api-test.aifactory.space/competition-submission/getResultByRequestID/"

# test
getUrl = 'https://signed.aifactory.site/getUrl'
bridgeUrl = 'https://apc1.aifactory.site'
apiUrl ="https://api-renewal.aifactory.space"
getResultUrl = "https://api-renewal.aifactory.space/submission/getResultByRequestID/"

def make_zip(main_name):
  run_type = 0
  main_filename = ''
  main_pyfilename = ''
  current_cwd = os.getcwd()  

  if '.py' not in main_name:
    run_type = 1

  if run_type == 1 and 'google.colab' in str(get_ipython()):
    print('Running on CoLab')
    run_type =2
  
  if run_type == 0: 
    print("python")    
  elif run_type == 1:     
    print("jupyter notebook")    
  elif run_type == 2: 
    print("google colab")    
    strs = main_name.split('=')
    ipynb_url = 'https://drive.google.com/uc?id=' + strs[1]
    main_filename = 'task.ipynb'
    output = '/content/' + main_filename
    gdown.download(ipynb_url, output)
  else: 
    print("not supported environments")
    return 
    
  zip_file = zipfile.ZipFile("./aif.zip", "w")  
  for (path, dir, files) in os.walk("./"):
    for file in files:       
      if "train" not in path and "drive" not in path and "sample_data" not in path and "aif.zip" not in file :      
        zip_file.write(os.path.join(path, file), compress_type=zipfile.ZIP_DEFLATED)
  zip_file.close()
  
def submit(model_name, key, func):

  main_name = ''
  try: 
    main_name = ipynbname.name()
  except Exception as e:
    main_name = "task.py"

  print("file : {0}".format(main_name))
  make_zip(main_name)
  
  values = {"key": key, "modelname": model_name}
  res = requests.post(bridge_url, files = {'file': open("./aif.zip",'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    requestID = res.text
    print("request id : {id} processing...".format(id= requestID))
    
    while True:
      try:
        res = requests.get(api_url + requestID)  
        if res.status_code == 200:
          data_json = json.loads(res.text)     
          if data_json["ct"] == 0 or data_json["ct"] == 3:
            print(data_json["message"])
            break

          if data_json["ct"] == 1: 
            print('{0} \r'.format(data_json["message"]), end="")
            
          time.sleep(10)
        else:
          print(res.status_code)  
          print(res.text)
          break
      except Exception as e:          
        print(" error :" + str(e))
        break    
    return
  print(res.status_code)  
  print(res.text)

def submit_test(model_name, key, func):
  main_name = ''
  try: 
    main_name = ipynbname.name()
  except Exception as e:
    main_name = "task.py"

  print("file : {0}".format(main_name))
  make_zip(main_name)
  
  with open('./aif.zip', 'rb') as f:
    data = f.read()
    
  try:        
    submitData = {"key" : key, "modelname" : model_name, "RequestID": "0", "FileName": "0"}    
    res = requests.post(bridgeUrl + "/submit", json=submitData)
    if res.status_code != 200:
      print("중계서버 오류")
      return 
    
    dataJson = json.loads(res.text)  
    requestID = dataJson['requestID']
      
    while True:
      res = requests.get(apiUrl + "/score-request/" + requestID)  
      if res.status_code != 200:
        print("중계서버 오류")
        return
      dataJson = json.loads(res.text)  
      status = dataJson["status"]
      if status == -1 :
        print(dataJson["error"])
        return
      elif status == 1 :
        break
      time.sleep(10)

    fileName = "%s-%s-%s.zip" % (dataJson["taskId"],dataJson["submissionIdPublic"], dataJson["submissionIdTotal"])  
    signedData = {"taskId": dataJson["taskId"], "fileName": fileName}      
    res = requests.post(
      getUrl,
      json=signedData,    
    )
        
    signedUrl = ""
    if res.status_code == 200:
       data_json = json.loads(res.text)
       if data_json["ct"] == 0 :
          signedUrl = data_json['url']
       else :
        print("파일 전송 오류")       
        return
    else :
      print("파일 전송 오류")       
      return
    res = requests.put(
      signedUrl,
      headers={'Content-Type': "application/octet-stream"},
      data=data
    ) 

    if res.status_code != 200 :
      print("파일 전송 오류")       
      return 
    
    submitData = {"key" : key, "modelname" : "test111", "RequestID": requestID, "FileName": fileName}
    res = requests.post(bridgeUrl + "/uploadCompleted", json=submitData)
    if res.status_code != 200:
      print("중계 서버 오류 : uploadCompleted")
      return 
    
    print("파일 전송 완료")

    while True:
      try:
        res = requests.get(getResultUrl + requestID)  
        if res.status_code == 200:
          data_json = json.loads(res.text)     
          if data_json["ct"] == 0 or data_json["ct"] == 3:
            print(data_json["message"])
            break

          if data_json["ct"] == 1: 
            print('{0} \r'.format(data_json["message"]), end="")
            
          time.sleep(10)
        else:
          print(res.status_code)  
          print(res.text)
          break
      except Exception as e:          
        print(" error :" + str(e))
        break  

  except Exception as e:
    print(str(e))

def submit_result(model_name, key, file_name):
  
  values = {"key": key, "modelname": model_name}
  res = requests.post(bridge_url, files = {'file': open(file_name,'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    print("ok")
    return
  print(res.status_code)  
  print(res.text)

def submit_result_test(model_name, key, file_name):
  
  values = {"key": key, "modelname": model_name}
  res = requests.post(bridge_test_url, files = {'file': open(file_name,'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    print("ok")
    return
  print(res.status_code)  
  print(res.text)

def submit_kwargs(**kwargs):

  main_name = ''
  try: 
    main_name = ipynbname.name()
  except Exception as e:
    main_name = "task.py"

  print("file : {0}".format(main_name))
  make_zip(main_name)
  
  values = {"key": kwargs['key'], "modelname": kwargs['model_name']}
  res = requests.post(bridge_url, files = {'file': open("./aif.zip",'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    requestID = res.text
    print("request id : {id} processing...".format(id= requestID))
    
    while True:
      try:
        res = requests.get(api_url + requestID)  
        if res.status_code == 200:
          data_json = json.loads(res.text)     
          if data_json["ct"] == 0 or data_json["ct"] == 3:
            print(data_json["message"])
            break

          if data_json["ct"] == 1: 
            print('{0} \r'.format(data_json["message"]), end="")
            
          time.sleep(10)
        else:
          print(res.status_code)  
          print(res.text)
          break
      except Exception as e:          
        print(" error :" + str(e))
        break    
    return
  print(res.status_code)  
  print(res.text)
