import numpy
import salient_point

#Minimal and Maximal human heart rate per Minute
MIN_HR = 50
MAX_HR = 210

'''
Default SP scheme, which also function as superclass for the other schemes
'''
class SP:

    #expect data dict constructed in data_input
    def __init__(self, data: dict[str, int]):
        self.rawdata = self.modifications(data)
        self.alldata = self.join(self.rawdata)
        self.sensitvities = self.calc_sensitvities()

    #No data modification in default scheme, just for children class
    def modifications(self, data: dict[str, int]):
        return data
    
    #Creates global stream database
    def join(self, data: dict[str, int]):
        #Intitliaze with empty array
        alldata = numpy.array([])
        keys = list(data.keys())
        for id in keys:
            id_data = data[id]
            alldata = numpy.concatenate((alldata, id_data))
        return alldata

    
    #Return the theoretical minimal value, might need to be changed in child class
    def theo_min(self):
        return MIN_HR
    
    #Return the theoretical maximal value, might need to be changed in child class
    def theo_max(self):
        return MAX_HR
    
    #Creates dictionary with theoretical , empircal, quantile, and corrected sensitivities
    def calc_sensitvities(self):
        sensitivities = dict()
        #Theoretical Sensitivity
        sensitivities['theo'] = self.theo_max() - self.theo_min()
        #Empirical Minimum and Maximum
        emp_max = numpy.max(self.alldata)
        emp_min = numpy.min(self.alldata)

        #Empirical Sensitivity
        sensitivities['emp'] = emp_max - emp_min

        #Corrected Sensitivity
        sensitivities['cor'] = min(self.theo_max(), emp_max) - max(self.theo_min(), emp_min)

        return sensitivities
    
    #Build anonymized database
    def anonymize_database(self, epsilon, sensitivity_id):
        anon_database = dict()
        sensitivity = self.sensitvities[sensitivity_id]
        keys = list(self.rawdata.keys())
        #Iterate every employee
        for id in keys:
            #Sequence of employee with id
            id_seq = self.rawdata[id]
            #Anonymize that sequence
            anon_id_seq = salient_point.anonymize(id_seq, epsilon, sensitivity)
            #Add to database
            anon_database[id] = anon_id_seq
        return anon_database








''' Class that realize SPA: Salient Point with Pre-Aggregation, child class of SP'''
class SPAvg(SP):


    def __init__(self, k, data):
        self.k = k
        super().__init__(data)

    #overwrite modification to condense data to k averages
    def modifications(self, data: dict[str, int]):
        k = self.k
        #averaging function
        kAvgData = averaging(k, data)
        
        return kAvgData




''' Class that realize SPC: Salient Point with C-Categories, child class of SP'''
class SPCat(SP):

    def __init__(self, C,  data: dict[str, int]):
        self.C = C
        super().__init__(data)

    def modifications(self, data: dict[str, int]):
        CatData = categorize(self.C, data)
        return CatData

    #adjust theoretical minimum value to its category
    def theo_min(self):
        org_min = super().theo_min()
        return org_min // self.C
    
    #adjust theoretical maximal value to its category
    def theo_max(self):
        org_max = super().theo_max()
        return org_max // self.C
    

'''Class realize SPAC: Salient Points with k-Average and then Categorization, Child class is SPC too avoid categorization redundacy'''
class SPAvgCat(SPCat):

    def __init__(self, k, C,  data: dict[str, int]):
        self.k = k
        self.C = C
        super().__init__(C, data)

    #Data dict is first averaged and then categorized
    def modifications(self, data: dict[str, int]):
        AvgData = averaging(self.k, data)
        AvgCatData = categorize(self.C, AvgData)
        return AvgCatData
    




'''Class realize SPCA: Salient Points with Categorization and then k-Averaging, Child class is SPC too avoid categorization redundacy'''
class SPCatAvg(SPCat):

    def __init__(self, C, k,  data: dict[str, int]):
        self.k = k
        self.C = C
        super().__init__(k, data)

    #Data dict is first averaged and then categorized
    def modifications(self, data: dict[str, int]):
        CatData = categorize(self.C, data)
        CatAvgData = averaging(self.k, CatData)
        return CatAvgData
    





#Answer of Average Query, calculates average heart rate over every employee for each time point, Every sequence needs to be of equal lenght!
def calculate_average(data: dict[str, int]):
    n = len(data)
    
    keys = list(data.keys())
    #Check lenght of sequence by checking first id
    m = len(data[keys[0]])
    avg_array = numpy.zeros(m)
    #For every Employee
    for id in keys:
        #For every recorded Time point
        for t in range(m):
            avg_array[t] += data[id][t]/n
    return avg_array


#transform database into k-average database
def averaging(k, data: dict[str, int]):
    keys = list(data.keys())
    #Calculate current sequence Length with first id
    seq_len = len(data[keys[0]])
    #Length of modified sequence
    k_seq_len = seq_len // k
    #Check if sequence Length is divisble by k
    if seq_len % k != 0:
        raise ValueError("Sequence Length is not divisable by k")
    
    #New Dataset with averages
    kAvgData = dict()

    for id in keys:
        #Empty sequence to be filled
        kAvgSeq = numpy.zeros(k_seq_len)
        #for ever average field
        for i in range(k_seq_len):
            #for every values correponding to that average
            for j in range(k):
                #Add proportion to the average field
                kAvgSeq[i] += data[id][i*k + j]/k

        kAvgData[id] = kAvgSeq

    return kAvgData


#Categorize Data in categorize of size C
def categorize(C, data: dict[str, int]):
    keys = list(data.keys())
    #Calculate current sequence Length with first id
    seq_len = len(data[keys[0]])
    #New Dataset with category Data
    CatData = dict()


    for id in keys:
        #Empty sequence to be filled
        CatSeq = numpy.zeros(seq_len)
        #for every time point
        for i in range(seq_len):
            CatSeq[i] = data[id][i] // C

        CatData[id] = CatSeq

    return CatData