#!/usr/bin/env python
# coding: utf-8 
#usage: python scrpit inputfile outfilename
from selenium import webdriver
from Bio import SeqIO
import re,time,json,sys
st = time.time()
input_file = sys.argv[1]
out_file = sys.argv[2]

#import os
#os.chdir(r"C:\Users\Acer\Desktop\codee\python\expasy")

expasy = webdriver.Chrome()
expasy.get("https://web.expasy.org/protparam/")


class expasy_cal():
    '''get physical and chemical parameters for a given protein sequence file 
        based on web https://web.expasy.org/protparam/'''
    
    def inputseq(seq):
        """input the protein sequence"""
        time.sleep(0.3)
        while True:
            if expasy.find_element_by_xpath('//*[@id="sib_body"]/form/textarea').is_displayed():
                expasy.find_element_by_xpath('//*[@id="sib_body"]/form/p[1]/input[1]').click() #获取新网页
                expasy.find_element_by_xpath('//*[@id="sib_body"]/form/textarea').send_keys(seq)
                expasy.find_element_by_xpath('//*[@id="sib_body"]/form/p[1]/input[2]').click()
                break
            else:
                print("input box is not displayed")
             
    def compute():
        """get the parameters showed below"""
         #inbox.send_keys(seq)
        time.sleep(0.3) #等待页面加载的时间
        while True:
            if expasy.find_element_by_xpath('//*[@id="sib_body"]/h2').is_displayed():
                pd={}
                parameters = expasy.find_element_by_xpath('//*[@id="sib_body"]/pre[2]').text.split("\n\n") #分割不同参数
                aaa='\n'.join(parameters)
                bbb=re.split("[:\n]",aaa)  #将参数值 与 值分割
                pd["number_of_amine_acid"] = bbb[1].strip()
                pd["molecular_weight"] = bbb[3].strip()
                pd["theoretical_pi"] = bbb[5].strip() 
                pd["instability_index"] = re.findall("[\d.]+",bbb[66])[0]  #filter 结果怎么是个对象
                pd["aliphatic_index"] = bbb[70].strip()
                pd["gravy"] = bbb[72].strip()
                return pd
                break
            else:
                print("loading")
                

with open(out_file,"w",encoding='utf-8') as f:
    f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
        'seq_id',
        'number_of_amine_acid',
        'molecular_weight',
        'theoretical_pi',
        'instability_index',
        'aliphatic_index',
        'gravy'))
    pros = SeqIO.parse(input_file,"fasta")
    i=0
    for pro in pros:
        print("="*10,"seq",i+1,"->",pro.id,"on the way","="*10)
        expasy_cal.inputseq(seq = pro.seq)
        cccc = expasy_cal.compute()
        number_of_amine_acid = cccc['number_of_amine_acid']
        molecular_weight = cccc['molecular_weight']
        theoretical_pi = cccc['theoretical_pi']
        instability_index = cccc['instability_index']
        aliphatic_index = cccc['aliphatic_index']
        gravy = cccc['gravy']
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            pro.id,
            number_of_amine_acid,
            molecular_weight,
            theoretical_pi,
            instability_index,
            aliphatic_index,
            gravy))
        i+=1
        
        #single_id_pd = {pro.id:cccc}  #单条序列计算结果封装到字典 好像这种不是json格式
        #print(single_id_pd)
        #json.dump(single_id_pd,f,indent = 4,ensure_ascii=False)  #是否要等到全部完成才写入？
        #f.write(json.dumps(single_id_pd,indent = 4,ensure_ascii=False)+"\n")
        #expasy.get("https://web.expasy.org/protparam/")
        expasy.back() #好像back也需要重新加载页面 也是慢
expasy.close()
et = time.time()
print("process finished")
print("taking time",et-st,"s")
