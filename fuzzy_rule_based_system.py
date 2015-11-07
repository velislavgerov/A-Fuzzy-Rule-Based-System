#-------------------------------------------------------------------------------
# Name:        A Fuzzy Rule-Based System
# Author:      velislav.gerov.12@aberdeen.ac.uk
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import os.path
import re

class KnowledgeBase():
    def __init__(self,inputmap,names, variables, measurements):
        self.rules = inputmap[names[0]] 
        self.names = names
        self.variables = variables
        self.measurements = measurements



class FourTuple():
    # Initializatioin function
    def __init__(self, a, b, alpha, beta):
        self.a = float(a)
        self.b = float(b)
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.tuple = [float(a), float(b), float(alpha), float(beta)]
    # Find the area
    def area(self, x):
        base = abs((self.a - self.alpha) - (self.b + self.beta))
        if self.a == self.b:
            #triangle
            area_full = 0.5*base
            area_missing = 0.5*base*(1-x)*(1-x)
            return area_full - area_missing
        else:
            #trapozoid
            area_full = 0.5*(base + (self.b - self.a))*1
            area_missing = 0.5*((base*(1-x)) + (self.b - self.a))*(1-x)
            return area
    # Find the centre point
    def centre(self):
        return ((self.a - self.alpha) + (self.b + self.beta))*0.5
    def membership_function(self,x):
        if x < (self.a - self.alpha): return 0
        if x >= (self.a - self.alpha) and x <= self.a:
            return self.alpha**-1*(x-self.a+self.alpha)
        if x >= self.a and x<= self.b: return 1
        if x >= self.b and x<= (self.b+self.beta):
            return self.beta**-1*(self.b+self.beta-x)
        if x > self.b + self.beta: return 0



class InputHandler():
    
    # Handling input and populating KnowledgeBase
    # Knowledge Base
    def input(self):
        names = []
        inputmap = {}
        input_values = {}
        variables = {}
        content = []
        pointer = 0
        counter = -1
        print "Please specify the file name:"
        
        filename = raw_input()
        #filename = "example2.txt"
        if not os.path.isfile(filename):
            print("File does not exist")
            return False
        file = open(filename, "rU")
        for line in file:

            if line == "\n": pointer += 1
            elif pointer%2 == 0:
                names.append(line.strip())
                counter += 1
                content = []
            else:
                content.append(line.strip())
                inputmap[names[counter]] = content
                #content = []
        print inputmap

        # Global input values is begin populated
        for item in reversed(names):
            current = item.split()
            if len(current) > 1:
                input_values[current[0]] = current[2]
                names.remove(item)
            else: break

        print names

        # Populating     
        for item in inputmap:
            temp = {}
            if item!=names[0]:
                
                four_tuples = []
                for i in inputmap[item]:
                    i = i.split()
                    name = i[0]
                    i = [float(x) for x in i if x!=name]
                    temp[name] = FourTuple(i[0],i[1],i[2],i[3])
                variables[item] = temp

        #print inputmap
        
        return KnowledgeBase(inputmap,names,variables,input_values)

class System():

    def __init__(self, KnowledgeBase):
        self.base = KnowledgeBase

    '''def fuzzifier(self,x):
        if x < (self.a - self.alpha): return 0
        if x >= (self.a - self.alpha) and x <= self.a:
            return self.alpha**-1*(x-self.a+self.alpha)
        if x >= self.a and x<= self.b: return 1
        if x >= self.b and x<= (self.b+self.beta):
            return self.beta**-1*(self.b+self.beta-x)
        if x > self.b + self.beta: return 0
'''
    def defuzzifier(self,inference_result):
        name = inference_result.keys()[0]
        values = inference_result[name]
        sum = 0
        sum1 = 0
        for item in values:
            if values[item] == 0.0: continue
            k = self.base.variables[name][item]
            print "Area: ",name, " is ", item, " - ", k.area(values[item])
            print "Centre: ",name, " is ", item, " - ", k.centre()
            sum += (k.centre()*k.area(values[item]))
            sum1 += k.area(values[item])
        if sum1!= 0: return sum//sum1
        else: return 0.0

    def inference_engine(self):
        #r Represent the rules into an appropriate format
        rules_dict = {}
        for item in self.base.rules:
            item = item.split()
            item = [x for x in item if x not in ["Rule","the","If","will","be","is"]]
            key = item[0]
            item.pop(0)
            rules_dict[key] = item
        print item
        
        mfsMap = {}
        last_name = ''
        for item in rules_dict:
            is_last = False
            is_name = True
            mfs = []
            connective = ''
            for x in range(0,len(rules_dict[item])):
                
                curx = rules_dict[item][x]
                if is_last:
                    last_name = curx
                    #print "Rule ", item, " resulted in: ",mfs[0]
                    nextx = rules_dict[item][x+1]
                    #inputz = mfs[0]
                    if nextx in mfsMap:
                        if mfsMap[nextx] < mfs[0]:
                            mfsMap[nextx] = mfs[0]
                    else:
                        mfsMap[nextx] = mfs[0]
                    is_last = False

                if len(mfs) == 3:
                    if mfs[1] == 'and':
                        mfs = [min(mfs[0],mfs[2])]
                    elif mfs[1] == 'or':
                        mfs = [max(mfs[0],mfs[2])]
                if curx.lower() == 'and' or curx.lower() == 'or': 
                    connective = curx.lower()
                    mfs.append(connective)
                    is_name = True
                    continue
                if curx.lower() == 'then':
                    is_last = True
                    continue
                if not is_last and is_name: 
                    nextx = rules_dict[item][x+1]
                    #print variables[curx][nextx].tuple
                    mf = self.base.variables[curx][nextx].membership_function(float(self.base.measurements[curx]))
                    print "Membership Function of ", curx, " is ", nextx, " - ", mf
                    mfs.append(mf)
                    is_name = False
                elif not is_name:
                    continue
            #print "Result for Rule ", item, ": " ," is ", mfs[0]
        result = {}
        result[last_name] = mfsMap

        return result
    


     

    
    




def main():
    #if (input()):
        #print inputmap
        #print names
        print ""
        print "Starting Inference Engine.."
        

        #inference_result = InferenceEngine(inputmap[names[0]])
        
        #print "Output of Inference Engine:", inference_result
        print ""
        print "Starting Defuzzifier.."
        
       
        # Populating global inputmap{}, a dictionary contarining    and names[]a  cointaining rule base, variables and crisp measurements
        #file = open(os.path.join(root,filename), "rU")
        #print kb.names
        base = InputHandler().input()
        system = System(base)
        #base =
        print base.measurements
        print system.base.measurements
        #print system.base.input
        print system.base.names
        print system.base.variables
        chrisp_values = system.inference_engine()
        print system.defuzzifier(chrisp_values)
        #output = Defuzzifier(inference_result)
        #print "Defuzzified value for ", names[-1], " is ", output
    

if __name__ == '__main__':
    main()