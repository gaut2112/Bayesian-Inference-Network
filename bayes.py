from random import randint
from collections import OrderedDict
import sys, getopt



def create_max_min(helper_dict):
    if (bool(helper_dict)):
        key_list=helper_dict.keys()
        max_val=helper_dict[key_list[0]][0]
        min_val=max_val
        #print max_val,min_val
        max_index=[0,0]
        min_index=[0,0]
        length = len(helper_dict.keys())
        i=0
        while i<length:
            j=0
            while j<2:
                if (max_val < helper_dict[key_list[i]][j]):
                    max_val = helper_dict[key_list[i]][j]
                    max_index=[i,j]
                if (min_val > helper_dict[key_list[i]][j]):
                    min_val = helper_dict[key_list[i]][j]
                    min_index=[i,j]
                j=j+1
            i=i+1
        max_res='T' if max_index[1]==0 else 'F'
        min_res='T' if min_index[1]==0 else 'F'
        result=[key_list[max_index[0]],max_res,key_list[min_index[0]],min_res]
        #print "result", result
    else:
        result=['none','N','none','N']
    return result
        
    

def prob_calc_helper(val1,val2,mul1,mul2):
    prob1=mul1*val1
    prob2=val2*mul2
    con_prob=float(prob1/(prob1+prob2))
    return con_prob

def max_increase_helper(nos,sym,val1,val2,test_res,mul1,mul2):
    max_dict={}
    i=0
    while i<nos:
        if test_res[i]== 'U':
            new_prob1=prob_calc_helper(val1[i],val2[i],mul1,mul2)
            new_prob2=prob_calc_helper(1-val1[i],1-val2[i],mul1,mul2)
            max_dict[sym[i]]=[new_prob1,new_prob2]
        i=i+1
    #print "Max Dict", max_dict
    return max_dict
       
def prob_helper_min_1(nos,sym,val1,val2,test_res,mul):
    i=0
    while i<nos:
        if test_res[i] == 'U':
            if (val1[i] >= val2[i]):
                mul *= (1-val1[i])
            else:
                mul *= val1[i]
        i=i+1   
    return mul

def prob_helper_min_2(nos,sym,val1,val2,test_res,mul):
    i=0
    while i<nos:
        if test_res[i] == 'U':
            if (val1[i] >= val2[i]):
                mul *= (1-val2[i])
            else:
                mul *= val2[i]
        i=i+1
    return mul

def prob_helper_max_2(nos,sym,val1,val2,test_res,mul):
    i=0
    while i<nos:
        if test_res[i] == 'U':
            if (val1[i] >= val2[i]):
                mul *= val2[i]
            else:
                mul *= (1-val2[i])
        i=i+1
    return mul

def prob_helper_max_1(nos,sym,val1,val2,test_res,mul):
    i=0
    while i<nos:
        if test_res[i] == 'U':
            if (val1[i] >= val2[i]):
                mul *= val1[i]
            else:
                mul *= (1-val1[i])
        i=i+1
    return mul
            

def prob_helper_1(nos,sym,val,test_res,dp):
    mul=1
    i=0
    while i<nos:
        if test_res[i] == 'T':
            mul *= float(val[i])
        if test_res[i] == 'F':
            mul *= float(1.0-val[i])
        i=i+1
    mul*=dp
    return mul
        

def prob_helper_2(nos,sym,val,test_res,dp):
    mul=1
    i=0
    while i<nos:
        if test_res[i] == 'T':
            mul *= float(val[i])
        if test_res[i] == 'F':
            mul *= float(1.0-val[i])
        i=i+1
    mul*=float(1.0-dp)
    return mul

def calculate_prob(filename,disease,patient,nop,nod):
    f1=open(filename,"w+")
    i=0
    while i<nop:
        f1.write("Patient-"+str(i+1)+":")
        f1.write("\n")
        dis_dict={}
        max_min_dict={}
        inc_dec_dict={}
        j=0
        while j<nod:
            max_min=[]
            inc_dec_list=[]
            id_dict={}
            prob1= prob_helper_1(disease[j]['n_sym'],disease[j]['sym'],disease[j]['b'],patient[i][j+1],disease[j]['p'])
            prob2= prob_helper_2(disease[j]['n_sym'],disease[j]['sym'],disease[j]['n'],patient[i][j+1],disease[j]['p'])
            con_prob=round(float( prob1/(prob1+prob2)),4)
            con_prob_str = str(con_prob)
            if (len(con_prob_str) < 6 ):
              	k = 6-len(con_prob_str)
                while k is not 0:
                  	con_prob_str += '0'
                        k=k-1
            dis_dict[disease[j]['name']] = con_prob_str
            max1=prob_helper_max_1(disease[j]['n_sym'],disease[j]['sym'],disease[j]['b'],disease[j]['n'],patient[i][j+1],prob1)
            max2=prob_helper_max_2(disease[j]['n_sym'],disease[j]['sym'],disease[j]['b'],disease[j]['n'],patient[i][j+1],prob2)
            max_prob=round(float(max1/(max1+max2)),4)
            min1=prob_helper_min_1(disease[j]['n_sym'],disease[j]['sym'],disease[j]['b'],disease[j]['n'],patient[i][j+1],prob1)
            min2=prob_helper_min_2(disease[j]['n_sym'],disease[j]['sym'],disease[j]['b'],disease[j]['n'],patient[i][j+1],prob2)
            min_prob=round(float(min1/(min1+min2)),4)
            max_prob_str = str(max_prob)
            if (len(max_prob_str) < 6):
              	m = 6-len(max_prob_str)
                while m is not 0:
                  	max_prob_str += '0'
                        m=m-1
            min_prob_str = str (min_prob)
            if (len(min_prob_str) < 6):
              	n = 6-len(min_prob_str)
                while n is not 0:
                  	min_prob_str += '0'
                        n=n-1
            max_min.append(min_prob_str)
            max_min.append(max_prob_str)
            max_min_dict[disease[j]['name']]=max_min
            id_dict=max_increase_helper(disease[j]['n_sym'],disease[j]['sym'],disease[j]['b'],disease[j]['n'],patient[i][j+1],prob1,prob2)
            inc_dec_list=create_max_min(id_dict)
            inc_dec_dict[disease[j]['name']]=inc_dec_list
            j=j+1
        f1.write(str(dis_dict))
        f1.write("\n")
        f1.write(str(max_min_dict))
        f1.write("\n")
        f1.write(str(inc_dec_dict))
        f1.write("\n")
        i=i+1
        


def main(argv):#main function to read and output files
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print "error in reading commandlin arguments"
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            inputfile=arg
    res={}
    fileN = inputfile.split("\\")[0]
    filename=fileN.split(".")[0]
    filename += "_inference.txt"
    print filename
    f = open(inputfile)
    st = f.readline()
    no_d  = int(st.split()[0])
    no_p = int(st.split()[1])
    i = no_d
    disease=[]
    patient=[]
    while i is not 0:
        temp={}
        data = f.readline().split()
        temp['name']=data[0]
        temp['n_sym']=int(data[1])
        temp['p']=float(data[2])
        temp['sym']=eval(f.readline())
        temp['b']=eval(f.readline())
        temp['n']=eval(f.readline())
        disease.append(temp)
        i=i-1
    i=0
    while i < no_p:
        temp={}
        j=1
        while j <= no_d:
            temp[j]=eval(f.readline())
            j=j+1
        i=i+1
        patient.append(temp)                 
    calculate_prob(filename,disease,patient,no_p,no_d)
        

if __name__=="__main__":
    
     main(sys.argv[1:])
