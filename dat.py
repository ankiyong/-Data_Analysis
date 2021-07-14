
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform

from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Darwin':  # 맥OS
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # 윈도우
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system...  sorry~~~')

#cctv = 서울시 cctv현황
cctv = pd.read_csv('../data_science/data/01. CCTV_in_Seoul.csv')

print(cctv.columns)
cctv.rename(columns={'기관명':'지역명'},inplace=True)
print(cctv.head(1))

#pop = 서울시 인구 현황
# pop = pd.read_excel('../data_science/data/01.population_in_Seoul.xls')
# print(pop.columns)
#원본 데이터의 인덱스가 다중 인덱스로 구성되어있어 행 조정이 필요하다
#컬럼 또한 필요한 내용만 추출이 필요하다

pop = pd.read_excel('../data_science/data/01.population_in_Seoul.xls',
                    usecols='B,D,G,J,N',
                    header=2)
# print(pop.head(1))

#pop의 컬럼명 또 한 변경해준다
pop.rename(columns ={pop.columns[0]:'지역명',
                     pop.columns[1]:'인구수',
                     pop.columns[2]:'한국인',
                     pop.columns[3]:'외국인',
                     pop.columns[4]:'고령자'},inplace = True)
print(pop.head(2))

#cctv와 pop의 개요를 info함수를 통해 확인한다
# print(cctv.info())
# print(pop.info())
# 1개의 행 차이가 있는것으로 보아 두 df중 중복값 혹은 결측치가 포함되어있을 가능성이 있다

# print(cctv['지역명'].unique())
# print(pop['지역명'].unique())
# print(len(cctv['지역명'].unique()))
# print(len(pop['지역명'].unique()))
#확인결과 pop df에 1행과 마지막 행에서 합계,결측치 행이 발견되어 두 행의 삭제가 필요함

pop.drop([0],inplace=True)
pop.drop([26],inplace=True)

# print(pop)

#외국인과 고령자의 인구비율을 새로운 컬럼으로 추가한다
pop['외국인비율'] = (pop['외국인'] / pop['인구수'])*100
pop['고령자비율'] = (pop['고령자'] / pop['인구수'])*100


data_result = pd.merge(cctv,pop,on='지역명')


# del data_result['2013년도 이전']
# del data_result['2014년']
# del data_result['2015년']
# del data_result['2016년']

data_result.set_index('지역명',inplace=True)
print(data_result.head(5))

data_result['소계'].plot(kind = 'bars',grid = True) #정렬 필요
data_result['소계'].sort_values().plot(kind = 'bars',grid = True)