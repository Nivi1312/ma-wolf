import numpy

#Heart rate increase that symbolize stress
SIG_HR = 13

#Detect stress full times by checking which heart rate is higher significantly higher
def detect_stress_times(avg_data):
    #Calculate Median
    med = numpy.median(avg_data)
    stress_times = list()
    #Check for every value
    for t in range(len(avg_data)):
        
        if avg_data[t] >= med + SIG_HR:
            print('Hallo')
            stress_times.append(t)
    return stress_times