import numpy as np
import pandas as pd
from joblib import dump, load
from datetime import datetime, timedelta
from datetime import date
import pytz
from dateutil import parser
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# For a given coordinate (x,y), find the cluster it belongs to.
# return [cluster_number, x_coordinate, y_coordinate].
# file_path = "/data"
data_path = "../data/"

def find_cluster(x, y):
    centers = pd.read_csv(data_path + 'centers.csv')
    distance2 = (centers['0'] - x)**2 + (centers['1'] - y)**2
    nearest_cluster = np.argmin(np.array(distance2))
    print(nearest_cluster)
    return list(centers.iloc[nearest_cluster])



# For a given coordinate (x,y), find the nearest N parking lots in the same cluster
# return a Pandas DataFrame (named "nearest_N") of the N parking lots, 
# with features including ['segmentid', 'streetname', 'x', 'y', 'cluster'].


def find_nearest_N(x, y, N):
    center_info = find_cluster(x, y)
    segment_info = pd.read_csv(data_path + 'segment_info.csv')
    same_area = segment_info[segment_info['cluster']==int(center_info[0])]
    same_area['distance'] = (same_area['x'] - x)**2 + (same_area['y'] - y)**2
    nearest_N = same_area.nsmallest(N, 'distance')[['segmentid', 'streetname', 'x', 'y', 'cluster']]
    return nearest_N

 # Turn the string input of address by Google Maps API to the format suitable for processing.
# return (weekday, hour).

def compute_time(time):
    day = 0
    hour = 0
    minute = 0
    
    ##############################
    # time_str = time.split()
    # for i, each in enumerate(time_str):
    #     if each == 'day' or each == 'days':
    #         day = int(time_str[i-1])
    #     if each == 'hour' or each == 'hours':
    #         hour = int(time_str[i-1])
    #     if each == 'min' or each == 'mins':
    #         minute = int(time_str[i-1])
    ####################################
    minute = time
    arrive_time = datetime.utcnow() + timedelta(days=day, hours=hour, minutes=minute) + timedelta(hours=-7)
    return ((date.weekday(arrive_time) + 1) % 7, arrive_time.hour)

# For the N nearest parking lots, predict the availability of parking spots in each of them.
# Add a new feature (named "availability") to the Pandas DataFrame nearest_N,
# and return the DataFrame.

def predict_N(nearest_N, time):
    pred = [] # This is the buffer to hold predicted availability of each of the N nearest parking lots.
    all_lots = pd.read_csv(data_path + 'testdata.csv')
    all_segments = pd.read_csv(data_path + 'segment_info.csv')
    centers = pd.read_csv(data_path + 'centers.csv')
    
    (weekday, hour) = compute_time(time) # Compute the arrival time of user
    
    # For each of the N parking lots:
    for k in range(len(nearest_N)):
        # First find out the history record of the same parking lot from testdata.
        segmentid = nearest_N.iloc[k]['segmentid']
        idx = all_lots.index[(all_lots['segmentid']==segmentid) & (all_lots['weekday']==weekday) & (all_lots['time']==hour)]
        full_capacity = list(all_segments[all_segments['segmentid']==segmentid]['capacity'])[0]
        x = list(all_segments[all_segments['segmentid']==segmentid]['x'])[0] # The x coordinate of parking lot
        y = list(all_segments[all_segments['segmentid']==segmentid]['y'])[0] # # The y coordinate of parking lot
        cluster_num = list(all_segments[all_segments['segmentid']==segmentid]['cluster'])[0] # The number of the cluster it belongs to
        center_x = list(centers[centers['centerid']==cluster_num]['0'])[0] # The x coordinate of cluster center
        center_y = list(centers[centers['centerid']==cluster_num]['1'])[0] # The y coordinate of cluster center
        distance = np.sqrt((x-center_x)**2 + (y-center_y)**2) # Compute the distance to the cluster center
        
        # Extract from testdata and make prediction
        prediction_number = []
        for i, each in enumerate(idx):
            # Just to prevent there is no sufficient history record for a given weekday or hour.
            if i == 0:
                continue
            # Extract history record of 24 hours from testdata each time.
            extract_testdata = all_lots.iloc[each-23:each+1]
            features = ['segmentid','ratio','capacity','occupied','distance','week','hour']
            for j in range(24):
                features += [str(j+1)]
            X = pd.DataFrame(columns=features)
            X['segmentid'] = extract_testdata['segmentid']
            X['week'] = extract_testdata['weekday']
            X['hour'] = extract_testdata['time']
            X['capacity'] = full_capacity
            X['occupied'] = extract_testdata['occupied']
            X['ratio'] = X['occupied'] / X['capacity']
            X['distance'] = distance * 1000
            for j in range(24):
                index = -j - 1
                rotate_data = list(X['occupied'])[index:] + list(X['occupied'])[:index]
                X[str(j+1)] = rotate_data
            test_features = ['capacity','distance','week','hour']
            
            # Make predictions
            for i in range(24):
                test_features += [str(i+1)]
            test_X = np.array(X[test_features].iloc[0]).reshape(1, -1)
            model_name = 'area' + str(cluster_num) + '.joblib'
            reg = load(data_path + model_name)
            prediction_number.append(reg.predict(test_X))
            pred_result = np.mean(np.array(prediction_number))
            if pred_result > full_capacity:
                pred_result = full_capacity
        pred.append(full_capacity - pred_result)
        
    # Add the predicted availability to DataFrame
    nearest_N['availability'] = np.array(pred)
    return nearest_N


