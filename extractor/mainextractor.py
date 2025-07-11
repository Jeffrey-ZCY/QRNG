import matplotlib.pyplot as plt
import numpy as np
import random

from PyQt5.QtWidgets import QFileDialog

import extractor.ottoeplitz
import extractor.image
import time
import sys
import os
from QRNGdetection.autocorrelation_test import *
from QRNGdetection.binary_derivative_test import *
from QRNGdetection.poker_test import *

sys.path.append(os.path.dirname(os.path.dirname(__file__)) + '\\QRNGdetection')
import QRNGdetection.sp800_22

print("调用了QRNGdetection中的模块")
print(sys.path)

""" 
Main program
======================

This file is the entry to the post-extractor program,
which is responsible for removing noise and extracting truly random numbers using the toeplitz matrix

"""

class Extractor:
    def __init__(self, para):
        self.filename = para["filename"]
        self.fewname = para["fewname"]
        self.fername = para["fername"]
        self.fdwname = para["fdwname"]
        self.fdrname = para["fdrname"]
        self.N = para["N"]
        self.scale = para["scale"]
        self.input = []
        self.length = 0
        self.runtime = 0
        self.testtime = 0
        self.speed = 0
        self.t = None
        self.isplt = para["isplt"]

    """ 
    Toeplitz Hashing Example
    ======================

    In this example, we generate a large Gaussian input data set. We plot the data before
    and after hashing. The data after hashing should be uniform.

    """

    def plot_data(self, flag, isplt, inputdata):
        """ Bins up data and plots. """
        self.t = extractor.ottoeplitz.Toeplitz(inputdata, self.N)  # 生成toeplitz矩阵
        N, data = self.t._calculate_N()
        print(self.N,data)
        binned_data, bins = np.histogram(data, bins=2 ** self.N - 1)
        data_digital = np.digitize(data, bins, right=True)
        fig, ax = plt.subplots()
        ax.hist(data_digital, bins=2 ** self.N - 1, label='Digitized Raw Data')
        plt.xlabel('Random numbers')
        plt.ylabel('Frequency')
        if flag:
            plt.title("Plotting Data After extracting")
            if isplt == 1:
                plt.savefig(f'{self.fewname}/after_extract.png')
            else:
                plt.savefig(f'{self.filename}/after_extract.png')
        else:
            plt.title("Plotting Data Before extracting")
            if isplt == 1:
                plt.savefig(f'{self.fewname}/before_extract.png')
            else:
                plt.savefig(f'{self.filename}/before_extract.png')
        return

    def file_to_array(self, fname, scale):
        input = []
        with open(f'{fname}', mode='r', encoding='utf-8') as fdata:
            for i in range(scale):
                try:
                    input.append(int(fdata.readline()))
                except ValueError as e:
                    pass
        return np.array(input)

    def extract(self):
        inputdata = self.file_to_array(self.fername, self.scale)
        # for i in range(2**19):
        #     temp = random.gauss(5, .05)  #gauss() 是内置的方法random模块。它用于返回具有高斯分布的随机浮点数。
        #     inputdata.append(temp)
        self.t = extractor.ottoeplitz.Toeplitz(inputdata, self.N)  # 生成toeplitz矩阵
        print(inputdata)
        if self.isplt == 1:
            self.plt1 = self.plot_data(0, self.isplt, inputdata)  # 绘制提取前直方图
            start = self.get_time()  # 程序运行时间计时
            dist1, dist2 = self.t.hash(1)  # 利用toeplitz后提取,参数为是否将二进制转换为十进制，0为不转换
            end = self.get_time()
            output1 = open(f'{self.fewname}/{self.filename}-decimal：{self.scale-20000}.txt', 'w')
            for i in range(len(dist2) - 1):
                output1.write(f"{int(dist2[i])}\n")
            # self.plt2 = self.plot_data(self.N, 1, self.isplt, dist2)  # 绘制提取前直方图
        elif self.isplt == 0:
            start = self.get_time()  # 程序运行时间计时
            dist1, dist2 = self.t.hash(0)  # 利用toeplitz后提取,参数为是否将二进制转换为十进制，0为不转换
            end = self.get_time()
        dist = ''
        min_ent = self.t.min_ent
        print(self.t.min_ent)
        for subdist in dist1:
            x = str(int(subdist))
            dist += x
        if self.isplt == 1:
            self.plt2 = self.plot_data(1, self.isplt, dist2)  # 绘制提取后直方图
        # extractor.plotting.plot_data(dist, 14)
        self.runtime = end - start
        print('Running time: %.4f Seconds\n' % self.runtime)
        self.length = len(dist)
        output = open(f'{self.fewname}/{self.filename}-后提取结果-数据：{self.scale-20000}.txt', 'w')
        output.write(dist)
        outpara = open(f'{self.fewname}/{self.filename}-后提取结果-参数：{self.scale-20000}.txt', 'w')
        outpara.write('原始数据最小熵为： %.2f \n' % min_ent)
        outpara.write('提取运行时间: %.4f Seconds\n' % self.runtime)
        self.extractspeed = self.length / (self.runtime * 1000)
        outpara.write('提取速度: %.2f kbps\n' % self.extractspeed)
        return [min_ent, self.runtime, self.extractspeed]

        # 检测

    def detection(self):
        test = ''
        self.testtime = 0
        with open(f"{self.fdrname}") as f:
            for line in f.readlines():
                line = line.strip()
                test += line
        nbits = [v for v in test]
        bits = [int(x) for x in nbits]
        results = list()
        start = self.get_time()
        QRNGdetection.sp800_22.all(results, bits)
        end = self.get_time()
        self.testtime = end - start
        print('**************************************************************************')
        print(len(test))
        fdresult = open(f'{self.fdwname}/{self.filename}-NIST检测结果-数据：{self.scale-20000}.txt', "w")
        for result in results:
            (summary_name, summary_p, summary_result) = result
            print(summary_name.ljust(40), summary_p.ljust(28), summary_result, file=fdresult)
        outpara = open(f'{self.fdwname}/{self.filename}-NIST检测结果-参数：{self.scale-20000}.txt', 'w+')
        outpara.write('检测时间: %.4f Seconds\n' % self.testtime)
        return results, self.testtime

    def guomi_detection(self):
        self.testtime = 0
        start = self.get_time()
        fd = self.fdwname + "/" + self.filename + f"-国密检测结果-数据：{self.scale-20000}.txt"
        print(fd)
        poker(self.fdrname, fd)
        glo.set_value('detectbar2', 1)
        autocorrelation(self.fdrname, fd)
        glo.set_value('detectbar2', 2)
        binary_derivative(self.fdrname, fd)
        glo.set_value('detectbar2', 3)
        end = self.get_time()
        self.testtime = end - start
        outpara = open(f'{fd}-国密检测结果-参数：{self.scale-20000}.txt', 'w+')
        outpara.write('检测时间: %.4f Seconds\n' % self.testtime)
        return fd, self.testtime

    def get_time(self):
        if sys.version_info > (3, 8):  # 兼容Python版本
            return time.perf_counter()
        else:
            return time.clock()
