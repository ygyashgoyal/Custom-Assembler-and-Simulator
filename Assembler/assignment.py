f=open("co.txt","r")
F=open("machinecode.txt","w")
opert={"add":"00000", "sub":"00001","mov":["00010","00011"],"ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
reg={"R0": "000","R1": "001","R2": "010","R3": "011","R4": "100","R5": "101","R6": "110","FLAGS":"111"}
tpA=["add","sub","mul","xor","or","and"]
tpB=["mov","rs","ls"]
tpC=["mov","div","not","cmp"]
tpD=["ld","st",]
tpE=["jmp","jlt","jgt","je"]
tpF=["hlt"]
label={}
lab={}
L1={}
L2=[]
import random
variables = {}
for line in f:
    if line.strip() == "":
        continue
    ans = line.strip().split()
    if ans[0]=="var":
        randomnumber = random.randint(65, 127)
        dictval = str(bin(randomnumber))
        finaldictval = dictval[2:]
        variables[ans[1]] = finaldictval
f.close()

def typeA(op,reg1,reg2,reg3,count):
    if(reg1 not in reg):
        L1[count]=("Invalid Register Name")
    elif(reg2 not in reg):
        L1[count]=("Invalid Register Name")
    elif(reg3 not in reg):
        L1[count]=("Invalid Register Name")
    else:
        if reg[reg1]=="111" or reg[reg2]=="111" or reg[reg3]=="111":
            L1[count]=("Flag error depicted")
        else:
            a=""
            a+=opert[op]
            a+="00"
            a+=reg[reg1]
            a+=reg[reg2]
            a+=reg[reg3]
            L2.append(a)
    
def typeB(op,reg1,value,count):
    if(reg1 not in reg):
            L1[count]=("Invalid Register Name")
    else:
        if reg[reg1]=="111":
            L1[count]=("Flag error depicted")
        else:
            value=value[1:]
            value=bin(int(value))
            sting=str(value)
            sting=sting[2:]
            l=len(sting)
            if l>7:
                L1[count]=("Invalid register depicted")
            else:
                a=""
                a+=(opert[op][0])
                a+=("0")
                a+=(reg[reg1])
                for i in range(7-l):
                    a+=("0")
                a+=(sting)
                L2.append(a)
        
def typeC(op,reg1,reg2,count):
    if(op!="mov"):
        if reg[reg1]=="111" or reg[reg2]=="111":
            L1[count]=("Flag error depicted")
    else:
        if reg[reg1]=="111":
            L1[count]=("Flag error depicted")
    if(reg1 not in reg):
        L1[count]=("Invalid Register Name")
    if(reg1 not in reg):
        L1[count]=("Invalid Register Name")
        
    else:
        a=""
        if(op=="mov"):
            a+=(opert[op][1])
        else:
            a+=(opert[op])
        a+=("00000")
        a+=(reg[reg1])
        a+=(reg[reg2])
        L2.append(a)

def typeD(op,reg1,mem,count):
    if reg[reg1]=="111":
        L1[count]=("Flag error depicted")
    else:
        if(reg1 not in reg):
            L1[count]=("Invalid Register Name")
        else:
            if (mem not in variables):
                L1[count]=("Variable doesn't exist")
            else:
                a=""
                a+=(opert[op])
                a+=("0")
                a+=(reg[reg1])
                a+=(variables[mem])
                L2.append(a)
def typeE(op,mem,count):
    a=""
    a+=(opert[op])
    a+=("0000")
    label[mem]=str(bin(random.randint(65,127)))[2:]
    lab[mem]=count
    a+=label[mem]
    L2.append(a)
    c=f.readline()
    d=0
    cnt=0
    while (True):
        c=c.split()
        if c[0][:-1]==mem:
            c=c[1:]
            if c[0] in tpA:
                typeA(c[0],c[1],c[2],c[3],count)
            elif c[0] in tpB:
                typeB(c[0],c[1],c[2],count)
            elif c[0] in tpC:
                typeC(c[0],c[1],c[2],count)
            elif c[0] in tpD:
                typeD(a[0],a[1],a[2],count)
            elif c[0] in tpF:
                e=""
                e+="11010"
                for i in range(11):
                    e+="0"
                L2.append(e)
                d+=1
            else:
                print("Error")
            return d
            
        else:
            c=f.readline()
            d+=1

    
f1=open("co.txt","r")    
def typeF(op,count):
    l=[i.strip() for i in f1]
    hlt_count = l.count('hlt') + l.count(': hlt') 
    if hlt_count == 0: 
        F.write('-:')
        L1[count]=('hlt instruction missing')
    elif hlt_count > 1 or l[-1] not in ('hlt', ': hlt'): 
        L1[count]=(str(l.index('hlt')+1))
        L1[count]=('hlt not being used as last instruction')
    else:
        a=""
        a+=(opert[op])
        for i in range(11):
            a+=("0")
        L2.append(a)
f=open("co.txt","r")
k=0
count=len(variables)
count2=0
while(True):
    a=f.readline()
    a=a.split()
    if(a!=[]):
        if(a[0]=="add"):
            typeA(a[0],a[1],a[2],a[3],count)
        elif(a[0]=="sub"):
            typeA(a[0],a[1],a[2],a[3],count)
        elif(a[0]=="mov"):
            if(a[2][0]=="$"):
                typeB(a[0],a[1],a[2],count)
            else:
                typeC(a[0],a[1],a[2],count)
        elif(a[0]=="ld"):
            typeD(a[0],a[1],a[2],count)
        elif(a[0]=="st"):
            typeD(a[0],a[1],a[2],count)
        elif(a[0]=="mul"):
            typeA(a[0],a[1],a[2],a[3],count)
        elif(a[0]=="div"):
            typeC(a[0],a[1],a[2],count)
        elif(a[0]=="rs"):
            typeB(a[0],a[1],a[2],count)
        elif(a[0]=="ls"):
            typeB(a[0],a[1],a[2],count)
        elif(a[0]=="xor"):
            typeA(a[0],a[1],a[2],a[3],count)
        elif(a[0]=="or"):
            typeA(a[0],a[1],a[2],a[3],count)
        elif(a[0]=="and"):
            typeA(a[0],a[1],a[2],a[3],count)
        elif(a[0]=="not"):
            typeC(a[0],a[1],a[2],count)
        elif(a[0]=="cmp"):
            typeC(a[0],a[1],a[2],count)
        elif(a[0]=="jmp"):
            d=typeE(a[0],a[1],count)
            count2+=d
        elif(a[0]=="jlt"):
            d=typeE(a[0],a[1],count)
            count2+=d
        elif(a[0]=="jgt"):
            d=typeE(a[0],a[1],count)
            count2+=d
        elif(a[0]=="je"):
            d=typeE(a[0],a[1],count)
            count2+=d
        elif(a[0]=="hlt"):
            count2+=1
            typeF(a[0],count)
        elif(a[0]=="var"):
            if(k==0):
                continue
            else:
                if(b[0]!="var"):
                    L1[count]=("Cant define variable in middle")
        elif(a[0] not in list(variables.keys())):
            if a[0][-1]==":":
                a=a[1:]
                if a[0] in tpA:
                    typeA(a[0],a[1],a[2],a[3],count)
                elif a[0] in tpB:
                    typeB(a[0],a[1],a[2],count)
                elif a[0] in tpC:
                    typeC(a[0],a[1],a[2],count)
                elif a[0] in tpD:
                    typeD(a[0],a[1],a[2],count)
                elif a[0] in tpF:
                    e=""
                    e+="11010"
                    for i in range(11):
                        e+="0"
                    L2.append(e)
        else:
            L1[count]=("Typo error")
        k+=1
        b=a
        count+=1
    else:
        break

if(count>128):
    F.write("Input file exceeded 128 lines")
else:
    if L1=={}:
        if count2==0:
            F.write("hlt is missing")
        else:
            for i in range(len(L2)):
                F.write(L2[i])
                F.write("\n")
    else:
        for key, values in L1.items():
            F.write(f'{key}: {values}\n')
        if count2==0:
            F.write("hlt is missing")
F.close()
