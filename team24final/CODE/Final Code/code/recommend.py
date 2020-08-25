from predict import *

def w(x1,y1,x2,y2):
#     walking distance caculation 
#     manhhatan
# 87.8km/degree
# 111.15km/degree
    a = np.array([x1,y1])
    if len(a.shape) == 1:
        a = a[:,np.newaxis]
    b = np.array([x2,y2]) 
    if len(b.shape) == 1:
        b = b[:,np.newaxis]
    diff = np.multiply(a-b,np.array([[87.8],[111.15]]) )
    dist = np.abs(diff[0,:]) +  np.abs(diff[1,:])
    return dist * 15  #avg walking speed 15min/km



def d(x1,y1,x2,y2):
#     walking distance caculation 
#     manhhatan
# 87.8km/degree
# 111.15km/degree
    a = np.array([x1,y1])
    if len(a.shape) == 1:
        a = a[:,np.newaxis]
    b = np.array([x2,y2]) 
    if len(b.shape) == 1:
        b = b[:,np.newaxis]
    diff = np.multiply(a-b,np.array([[87.8],[111.15]]) )
    dist = np.abs(diff[0,:]) +  np.abs(diff[1,:])
    return dist * 4.4 #avg driving speed 15min/km

def eval_aval(aval,a=0.3):
    return 1- np.exp(-a*aval)
# def score(v)
#    return  v*  


def park_score(x1, y1, x2, y2, nearest_N, plot = False, test = False):
# x1,y1: origin's coordinate
# x2,y2: target's coordinate 
# test: when test set visited parking lot aval t0 0 manually
    # Initialization
    penalty_1 = 50 # penalty for not finding a parking space in the end
    penalty_2 = 10 # penalty for moving around in a parking lot and finding it's full 
    idx = nearest_N.axes[0]
    segmentid = nearest_N["segmentid"]
    x = nearest_N["x"]
    y = nearest_N["y"]
    aval = nearest_N["availability"]
    ##########################
    # Test Mode
    if test:
        for i in test:
            if i in nearest_N.index:
                aval[i] = 0
    ##########################
#     eval avalability as a (0,1) prob
    p = eval_aval(aval,0.3)
#     initialize the evaluation value for each park
    v = p * w(x,y,x2,y2) + (1 - p) * penalty_1
    v_init = v.copy()
    for i in range(100):
        for n in idx:
            v_old = v.copy()
            temp = v.copy() 
            for m in idx:
                if n!= m and v[m] > v[n]:
                    temp[m] += d(x[m],y[m], x[n],y[n])
                else:
                    temp[m]+= 99999         
            v_m = min(temp)
            if v_m > 99999:
                v_m = max(v)
            v[n] = p[n]* w(x[n],y[n],x2,y2) +  (1 - p[n])  * (v_m + penalty_2)
        if (np.linalg.norm(v-v_old) < 1e-6 ):
            break
    v += d(x,y, x1,y1)
    
    if plot:
        x_pos = x*87.8
        y_pos = y*111.15
        
        plt.figure(figsize=(15,10))
        # initialized recommendation level
        plt.scatter(x_pos , y_pos, c = aval, s = 200000/v_init/v_init/v_init ,cmap = 'Reds'  )
        plt.scatter(x1*87.8, y1*111.15, s=100 , marker = "*", label ="origin",c = 'b')
        plt.scatter(x2*87.8, y2*111.15, s=100, marker = "X", label ="destination",c ='g')
        plt.legend()
        for i in idx:
            plt.annotate(i, (x_pos [i], y_pos[i]))
    
        plt.figure(figsize=(15,10))
        # coveged recommendation level
        plt.scatter(x_pos , y_pos, c = aval, s = np.exp(200000/v/v/v)/30 ,cmap = 'Reds')
        plt.scatter(x1*87.8, y1*111.15, s=100, marker = "*", label ="origin", c = 'b')
        plt.scatter(x2*87.8, y2*111.15, s=100, marker = "X", label ="destination", c ='g')
        plt.legend()
        for i in idx:
            plt.annotate(i, (x_pos [i], y_pos[i]))
        
    return v


def park_recommd(x1, y1, x2, y2, time, N, M, plot = False , test = False):
# x1,y1: origin's coordinate
# x2,y2: target's coordinate
# time: expeected arriving time 
# Select best M from N nearest parking lots 
    # find N nearest parking lots
    find_cluster(x2,y2)
    nearest_N = find_nearest_N(x2, y2, N)
    (weekday, hour) = compute_time(time)
    nearest_N = predict_N(nearest_N, time)
    # get the each ones infomation (including expected time to find parking space with each choice)
    park_val = park_score(x1, y1, x2, y2, nearest_N, plot ,test)
    v_info = pd.DataFrame({'exp_time':park_val,'x':nearest_N['x'],'y':nearest_N['y'], 'availability': nearest_N['availability'] })
    
    return v_info.nsmallest(M,'exp_time',keep='first')

