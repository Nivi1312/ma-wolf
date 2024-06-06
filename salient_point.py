import numpy


#Auxiliary function to detect if a  point is in trend
def check_trend(pre, cur, next):
    if(pre < 0 and cur < 0 and next < 0):
        return 1                    #upwards trend
    elif(pre > 0 and cur > 0 and next > 0):
        return -1                   #downwards trend
    else:
        return 0                    #no trend

#Calculate salient points from the sequence data, returns list of 
def calc_salient_points(data):
    #only one possible salient point
    if len(data) == 1:
        return [0, data[0]]

    #Calculate first deritivate
    dervative = numpy.gradient(data)    

    #Delete Points with derivative 0 (they contain no additional information)
    Clist = list()
    for pnt in range(len(dervative)):
        (t, dx) = (pnt, dervative[pnt])   
        if dx != 0:
            Clist.append((t, dx))       

    #No Salienpoints found, take first and last point
    if(len(Clist) == 0):
        return [[0, data[0]], [len(data)-1, data[len(data)-1]]]
    
    #List of Salient Points
    SalientPoints = list()
  
    #First point in sequence is always salient
    SalientPoints.append([0, data[0]])



    for h in range(1, len(Clist)-1):
        #Look at previously, current and next Point to detect upwards/downwards trend
        (tpre, dxpre) = Clist[h-1]
        (tcur, dxcur) = Clist[h]
        (tnxt, dxnxt) = Clist[h+1]
        trend = check_trend(dxpre, dxcur, dxnxt)

        #if the Point isnt part of trend it is salient
        if(trend == 0):         
            SalientPoints.append([tcur, data[tcur]])
        

    # Last point of sequence is always salient
    SalientPoints.append([len(data)-1, data[len(data)-1]]) 

    return SalientPoints

#Anonymize list of salient points, returns list of only the noisy y-values
def anonymize_salient_points(SalientPoints, epsilon, sensitivity):
    r = len(SalientPoints)
    #Arrays of noisy y values from salient points
    noisySP = numpy.zeros(r)

    #privacy budget per point
    ep_r = epsilon/r

    #Laplace parametrization according to the Laplace MEchanis,
    lp_cal = sensitivity/(ep_r) 

    #Add Noise to every value
    for i in range(r):
        (t, val) = SalientPoints[i]
        noise = numpy.random.laplace(0, lp_cal)
        noisySP[i] = (val + noise) 
    return noisySP

#Creates fulllength anonymized sequence by interpolation of the noisy salient points
def interpolate_salient_points(seq_len, SalientPoints, noisySP):

    #x-axis is fully constructed and contains every value
    X = range(0, seq_len)

    #Extract x-values of salient points
    SPx = list()
    for i in range(len(SalientPoints)):
        (t, val) = SalientPoints[i]
        SPx.append(t)

    #interpolation
    anon = numpy.interp(X, SPx, noisySP)
    return anon

#Anonymize the sequence compeletly
def anonymize(data, epsilon, sensitivity):
    seq_len = len(data)
    SalientPoints = calc_salient_points(data)
    noisySP = anonymize_salient_points(SalientPoints, epsilon, sensitivity)
    anonSequence = interpolate_salient_points(seq_len, SalientPoints, noisySP)
    return anonSequence