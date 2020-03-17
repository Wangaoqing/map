map_path='allindex1.map'

#读取.map文件
def read_map():
    dict = {}
    with open(map_path) as f:
        str_map =f.readline()
        while str_map!='':
            # 如果在key两边上加上空格
            key =str_map.split('=')[0].strip()
            content =str_map.split('=')[1].strip()
            dict[key]=content
            str_map=f.readline()
    return dict

dict = read_map()

import regex as re

def process_file(dst):     # 读文件到缓冲区
    try:     # 打开文件
        txt=open(dst,encoding='utf8')
    except IOError as s:
        print (s)
        return None
    try:     # 读文件到缓冲区
        bvffer=txt.read()
        print(dst+" Read File okay!")
        # print(bvffer)
    except:
        print (dst+" Read File Error!")
        # print(bvffer)
        return None
    txt.close()
    return bvffer

#没有使用
def process_buffer(bvffer):#处理缓冲区文件，返回词频
    if bvffer:
        word_freq = {}
        # 下面添加处理缓冲区 bvffer代码，统计每个单词的频率，存放在字典word_freq
        bvffer=bvffer.lower()
        for x in '~!@#$%^&*()_+/*+\][':
            bvffer=bvffer.replace(x, " ")
        bvffer = ' '.join(bvffer.split()).join('\r\n')
        words=bvffer.strip().split()
        for word in words:
            word_freq[word]=word_freq.get(word,0)+1
        print("process_buffer:",word_freq)
        return word_freq

#输出top10的单词，没有使用
def output_result(word_freq):
    if word_freq:
        sorted_word_freq = sorted(word_freq.items(), key=lambda v: v[1], reverse=True)
        for item in sorted_word_freq[:10]:  # 输出 Top 10 的单词
            print(item)


# 处理新文件，返回是否存在dict里的key选项
def process_new_file(dict,bvffer,word_freq):
    flag =0
    bvffer = str(bvffer).lower()
    # for x in '~!@#$%^&*()-_+/*+\][':
    #     bvffer = bvffer.replace(x, " ")
    # bvffer =bvffer.replace("  "," ")

    # bvffer = ' '.join(bvffer.split())
    # print(bvffer)
    flag,bvffer,word_freq =replace_count(bvffer,dict,word_freq)
    return flag,bvffer,word_freq

# 将template中属于dictionary中的key替换为dic[key]
# 返回值，如果存在key值，则返回1，替换之后的文本；如果不存在，则返回，原来的文本
def replace_count(template, dictionary,word_freq):
    flag = 0
    tt=re.sub(' +',' ',template)#将多个空格替换为一个
    for key in dictionary:
        # print(key)
        if key in tt:
            flag =1
            # num = num+tt.count("\\s"+key + "\\W")
            # num = num+tt.count("\\s" + key + "\\s")
            # num = num + tt.count("\\W" + key + "\\s")
            # tt=re.sub("\\s"+key + "[,.!?:;()[]{}'\"`]"," " + dictionary[key] + " ",tt)
            # tt=re.sub("\\s"+key+"\\s"," "+dictionary[key]+ " ",tt)
            # tt = re.sub("[,.!?:;()[]{}'\"`]" + key + "\\s"," "+ dictionary[key]+ " ", tt)
            # tt = re.sub("[,.!?:;()[]{}'\"`]" + key + "[,.!?:;()[]{}'\"`]"," "+ dictionary[key]+ " ", tt)
            #我们认为“ brothers　”＝“—brothers—”
            (tt,num) = re.subn("\\b"+key+"\\b",dictionary[key],tt)
            word_freq[key] = word_freq.get(key,0)+num
            # print("1:",word_freq)
            # tt =tt.replace(str(key),str(dictionary[key]))
    return flag,tt,word_freq



# 输入为要处理的文件名，处理之后要存入的文件夹，将要处理的文件处理之后存入新的文件
def read_write_bvffer(path,new_path,word_freq):
    #读取新闻信息,然后找另一个路径存下
    flag=0
    # print("dict",dict)
    bvffer= process_file(path)
    if bvffer ==None:
        return flag, word_freq
    # print("bvffer",bvffer)#有值
    flag,bvffer,word_freq=process_new_file(dict,bvffer,word_freq)
    # print("2:",word_freq)
    #print(bvffer) 空
    if flag == 1:
        print(new_path+' Terminology')
        with open (new_path,encoding='utf8',mode="w") as f:
            f.write(bvffer)
    return flag,word_freq




###复制文件夹中所有文件和文件夹
import os
import shutil


#通过校验MD5 判断B内的文件与A 不同
def get_MD5(file_path):
    files_md5 = os.popen('md5 %s' % file_path).read().strip()
    file_md5 = files_md5.replace('MD5 (%s) = ' % file_path, '')
    return file_md5


# path = r'C:\Users\lenovo\Desktop\word_freq.txt'
def main(path, new_path,B,word_freq):
    count =0
    # word_freq={}
    txt_name= 'Empty'
    txt_dict_path =B
    for files in os.listdir(path):
        txt_new_name =str(files)
        if txt_new_name.endswith('.txt'):
            pass
        else:
            if not os.path.isdir(txt_dict_path+'\\count'):
                os.makedirs(txt_dict_path+'\\count')
            txt_path =txt_dict_path+'\\count\\'+txt_name+'.txt'
            write_dict(txt_path,word_freq,dict)
            txt_name =txt_new_name
            word_freq={}
        # if files.get
        name = os.path.join(path, files)
        new_name = os.path.join(new_path, files)
        if os.path.isfile(name):
            if os.path.isfile(new_name):
                if get_MD5(name) != get_MD5(new_name):
                    flag,word_freq=read_write_bvffer(name,new_name,word_freq)
                    # write_dict(path, word_freq)
                    # count = count + flag
            else:
                flag, word_freq = read_write_bvffer(name, new_name,word_freq)
                # write_dict(path, word_freq)
                # count = count + flag
        else:
            if not os.path.isdir(new_name):
                os.makedirs(new_name)
            main(name, new_name,txt_dict_path,word_freq)
    return word_freq,txt_name



#没有使用
def del_emp_dir(path):#删除所有空的文件夹
    for (root, dirs, files) in os.walk(path):
        for item in dirs:
            dir = os.path.join(root, item)
            try:
                os.rmdir(dir)
                print(dir)
            except Exception as e:
                print('Exception', e)

# 每天每月每年都需要记录
def write_dict(path,dictionary,dict):
    with open(path,"a+") as f:
        for key in dictionary:
            if dictionary[key]!=0:
                f.write(str(key)+" "+dict[key] +"="+str(dictionary[key])+'\n')



if __name__ == '__main__':
    # word_freq={}
    # 原有数据的地址

    A = r'F:\毕业设计\新闻数据2_25'
    # 要存放数据的文件夹，需要先创建
    # 如示例，需要存在F:\\毕业设计\\file2map\\q\\beast的文件夹
    B = 'F:\\毕业设计\\file2map\\cnn'
    word_freq,txt_name=main(A,B,B,{})
    txt_path = B + '\\count\\' + txt_name + '.txt'
    write_dict(txt_path, word_freq, dict)
    os.remove(B + '\\count\\' + 'Empty.txt')
    # path = r'C:\Users\lenovo\Desktop\word_freq.txt'
    # write_dict(path,word_freq)
#拷贝目录A 的内容到目录B如示例



def find_word_freq(file):
    pass