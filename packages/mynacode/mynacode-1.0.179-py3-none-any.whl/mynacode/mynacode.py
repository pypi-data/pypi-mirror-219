import numpy as np
import os, sys
import json, requests, ast
import pkg_resources
import GPUtil, platform, psutil
from datetime import datetime
from sklearn import metrics
import matplotlib.pyplot as plt
import dill
import urllib.request

protocol = 'http'
#protocol = 'https'

IP = '127.0.0.1:8000'
#IP = 'mynacode.com'

username = ""
key = ""
  

def login(uname, ky):
  global username
  global key
  
  print("Logging in...")
  credentials = {'username':uname, 'key':ky, 'task':'login'}
  response = requests.post(protocol+'://'+IP+'/api/python_login', data=credentials)
  
  if response.text == '1':
    username = uname
    key = ky
    print("Successfully connected to mynacode!")
  else:
    print("Credentials could not be verified.")


def metadata(run_id):

  installed_packages = pkg_resources.working_set #Save all installed packages for that project
  installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])

  system_info_list = ['Codebase Python ' + platform.python_version()]
  
  system_info_list.append("    GPU    ")
  try:
      gpus = GPUtil.getGPUs()
      if len(gpus) == 0:
          system_info_list.append("No NVIDIA GPU found")
      else:
          for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_memory = gpu.memoryTotal
            system_info_list.append("GPU ID " + str(gpu_id))
            system_info_list.append(gpu_name)
            system_info_list.append(str(gpu_memory) + " MB")
  except:
      system_info_list.append("No NVIDIA Driver found")

  system_info_list.append("    CPU    ")
  system_info_list.append(platform.processor())
  system_info_list.append(platform.platform())
  system_info_list.append(platform.machine())
  system_info_list.append("    MEMORY    ")
  system_info_list.append("RAM " + str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB")

  data = {'run_id' : run_id, 'installed_packages': str(installed_packages_list), 'username': username, 'key': key, 'system_information': str(system_info_list)}
  
  response = requests.post(protocol+'://'+IP+'/api/add_metadata', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    print("Metadata saved")
  

def csv(run_id, dataframe, node_name="CSV"):
    columns_list = dataframe.columns.values.tolist()
    isnull_list = dataframe.isnull().sum().values.tolist()
    isunique_list = dataframe.nunique().values.tolist()
    size = sys.getsizeof(dataframe)/1024
    shape = dataframe.shape
    dtypes_list = []

    for d in dataframe.dtypes:
        dtypes_list.append(str(d))

    data = {'run_id': run_id, 'columns_list': str(columns_list), 'isnull_list': str(isnull_list),
            'isunique_list': str(isunique_list), 'dtypes_list': str(dtypes_list),
            'username': username, 'size': int(size), 'shape': str(shape), 'key': key, 'node_name': node_name}

    response = requests.post(protocol+'://'+IP+'/api/add_csv', data=data)

    if response.text == '0':
      print("Authentication failed")
    else:
      print("CSV Information saved.")  

    

def specificity(y_true, y_pred):
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_truth = np.count_nonzero(y_true == 0)
   
    return float(y_correct/y_truth)

def npv(y_true, y_pred): #Negative Predicted Value
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_predicted = np.count_nonzero(y_pred == 0)
   
    return float(y_correct/y_predicted)

def get_roc_auc(y_true, y_pred):
    fpr, tpr, threshold = metrics.roc_curve(y_true, y_pred)
    roc_auc = metrics.auc(fpr, tpr)
    gmeans = np.sqrt(tpr * (1 - fpr)) #sensitivity * specificity (element-wise)
    index = np.argmax(gmeans) #Returns index of max value
    best_threshold = threshold[index]
   
    return fpr, tpr, roc_auc, gmeans, best_threshold, index

def get_metrics(y_true, y_pred, threshold):
    y_pred_binary = (y_pred > threshold).astype('float')
   
    prec = metrics.precision_score(y_true, y_pred_binary)
    rec = metrics.recall_score(y_true, y_pred_binary)
    spec = specificity(y_true, y_pred_binary)
    f1 = metrics.f1_score(y_true, y_pred_binary)
    acc = metrics.accuracy_score(y_true, y_pred_binary)
    npv_val = npv(y_true, y_pred_binary)
   
    c_matrix = metrics.confusion_matrix(y_true, y_pred_binary, labels=[0,1])

    c_matrix = c_matrix.tolist()

    c_matrix = [item for sublist in c_matrix for item in sublist]
   
    return prec, rec, spec, f1, acc, npv_val, c_matrix


def results(run_id, y_true = [], y_predicted = [], threshold=0.5, results_dict = {}, node_name="Results", problem_type = 'binary classification', hist_bins=20):


    if len(y_true) != 0 and len(y_predicted) != 0:
      
      y_predicted = np.array(y_predicted).flatten()
      y_true = np.array(y_true).flatten()

      zero_idx = np.where(y_true == 0)[0]
      one_idx = np.where(y_true == 1)[0]
      
      prec, rec, spec, f1, acc, npv_val, c_matrix = get_metrics(y_true, y_predicted, threshold)
      fpr, tpr, roc_auc, gmeans, best_threshold, index = get_roc_auc(y_true, y_predicted)


      #pred_hist = plt.hist(y_predicted, bins=hist_bins)
      #freq = pred_hist[0]
      #bins = pred_hist[1]
      #'freq': freq.tolist(), 'bins': bins.tolist()

      binary = {'precision': round(prec, 4), 'recall': round(rec, 4), 'specificity': round(spec, 4),
              'f1': round(f1, 4), 'accuracy': round(acc, 4), 'npv': round(npv_val, 4), 'c_matrix': c_matrix,
              'test_auc': roc_auc, 'zero_prob': y_predicted[zero_idx].tolist(), 'one_prob': y_predicted[one_idx].tolist(),
                'fpr': fpr.tolist(), 'tpr': tpr.tolist(), 'threshold': round(threshold, 4)}

      results_dict.update(binary)

    data = {'run_id' : run_id, 'results_dict': str(results_dict), 'node_name': node_name, 'username': username, 'key': key}

    response = requests.post(protocol+'://'+IP+'/api/add_results', data=data)
  
    if response.text == '0':
      print("Authentication failed")
    else:
      print("Results saved")



def save_torch_model(run_id, model):
    if not os.path.exists('mynacode'):
      os.mkdir('mynacode')
      
    with open('mynacode/'+str(run_id)+'/saved_network.pkl', 'wb') as f:
        dill.dump(model, f)

    torch.save(model.state_dict(), 'mynacode/'+str(run_id)+'/saved_state_dict.pt')
        
    files = {'network': open('mynacode/'+str(run_id)+'/saved_network.pkl','rb'), 'state_dict': open('mynacode/'+str(run_id)+'/saved_state_dict.pt','rb')}
    
    response = requests.post(protocol+'://'+IP+'/api/upload_pytorch_weights', files=files, data={'run_id':run_id, 'username': username, 'key': key})


def load_torch_model(run_id):

    response = requests.post(protocol+'://'+IP+'/api/get_pytorch_weights', data={'run_id':run_id, 'username': username, 'key': key})
    response = response.json()

    if not os.path.exists('mynacode'):
      os.mkdir('mynacode')

    if not os.path.exists('mynacode/'+str(run_id)):
      os.mkdir('mynacode/'+str(run_id))

    urllib.request.urlretrieve(response['weights'], 'mynacode/'+str(run_id)+'/'+response['weights'].split('/')[-1])
    urllib.request.urlretrieve(response['network'], 'mynacode/'+str(run_id)+'/'+response['network'].split('/')[-1])

    with open('mynacode/'+str(run_id)+'/saved_network.pkl', 'rb') as f:
        net = dill.load(f)


    net.load_state_dict(torch.load('mynacode/'+str(run_id)+'/saved_state_dict.pt'))

    return net


def save_file(run_id, filepath):
    if not os.path.exists(filepath):
      print(filepath, ' doesn not exist')
      return 
        
    file = {'file': open(filepath,'rb')}
    
    response = requests.post(protocol+'://'+IP+'/api/upload_file', files=file, data={'run_id':run_id, 'username': username, 'key': key})



def dataset(run_id, dataset_dict = {}, train_set=[], train_labels=[], test_set=[], test_labels=[], val_set=[], val_labels=[], problem_type = 'binary classification',  node_name="Datasets"):
  train_set = np.array(train_set)
  val_set = np.array(val_set)
  test_set = np.array(test_set)

  train_labels = np.array(train_labels)
  val_labels = np.array(val_labels)
  test_labels = np.array(test_labels)


  if len(train_set) > 0:
    train_mean = np.mean(train_set)
    train_min = np.min(train_set)
    train_max = np.max(train_set)
    dataset_dict.update({'train_mean': train_mean, 'train_min': train_min, 'train_max': train_max})

  if len(val_set) > 0:
    val_mean = np.mean(val_set)
    val_min = np.min(val_set)
    val_max = np.max(val_set)
    dataset_dict.update({'val_mean': val_mean, 'val_min': val_min, 'val_max': val_max})

  if len(test_set) > 0:
    test_mean = np.mean(test_set)
    test_min = np.min(test_set)
    test_max = np.max(test_set)
    dataset_dict.update({'test_mean':test_mean, 'test_min':test_min, 'test_max':test_max})

  if len(train_labels) > 0:
    train_unique, train_count = numpy.unique(train_labels, return_counts=True)
    dataset_dict.update({'train_labels': train_unique, 'train_count':train_count})

  if len(val_labels) > 0:
    val_unique, val_count = numpy.unique(val_labels, return_counts=True)
    dataset_dict.update({'val_labels': val_unique, 'val_count':val_count})

  if len(test_labels) > 0:
    test_unique, test_count = numpy.unique(test_labels, return_counts=True)
    dataset_dict.update({'test_labels': test_unique, 'test_count':test_count})
      
  data = {'run_id' : run_id, 'dataset_dict': str(dataset_dict), 'node_name': node_name, 'username': username, 'key': key}
  
  response = requests.post(protocol+'://'+IP+'/api/add_dataset', data=data)


def variables(run_id, variables_dict = {}, node_name="Variables"):
  data = {'run_id' : run_id, 'variables_dict': str(variables_dict), 'node_name': node_name, 'username': username, 'key': key}
  
  response = requests.post(protocol+'://'+IP+'/api/add_variables', data=data)







  




 



