#!/usr/bin/env python
# coding: utf-8

# ## 완료되시면 LC 제출
# ## 그동안 배웠던 문법 복습하는 시간으로 생각하시면 되고, 과제 외에 질문 있으시면 질문하셔도 좋습니다.

# 실제 데이터분석가로서 현업에 투입되면, 데이터를 분석하는 일보다 데이터를 정리하는 일에 더 많은 시간을 할애하게 됩니다. 통상적으로 전체 업무시간에 70% ~ 80%는 데이터를 정리하는 일을 하게 되는데, 이 과정에서 실력있는 데이터 분석가와 그렇지 않은 데이터 분석가의 차이가 눈에 보이게 됩니다. 실력있는 데이터 분석가는 동일한 분량의 데이터를 2~3시간 안에 처리하는데 비해, 실력이 부족하고 아직 툴에 익숙하지 않은 데이터 분석가는 적어도 반나절, 길면 하루 ~ 이틀 정도의 시간을 투입해야 겨우 동일한 분량의 데이터를 처리하곤 합니다.
# 
# 문제를 풀 때 다른 자료를 참고하거나, 구글에 검색하는 것 모두 허용합니다.

# In[1]:


# 관련 모듈 import 하기
import pandas as pd
import numpy as np


# In[2]:


import matplotlib.pyplot as plt #그래프 패키지 모듈 등록
get_ipython().run_line_magic('matplotlib', 'inline')
#그래프는 show()함수를 통해서 독립창에서 실행되는 것이 원칙
#그래프를 콘솔에서 바로 작도되록 하는 설정


# In[3]:


# 한글 문제
# matplotlit의 기본 폰트에서 한글 지원되지 않기 때문에
# matplotlib의 폰트 변경 필요
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


# In[4]:


# 콘솔에서 모든 출력 허용하기
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity="all"


# In[5]:


# 판다스 데이터프레임(DataFrame)을 출력할 때, 최대 출력할 수 있는 컬럼을 100개로 
# 데이터를 분석할 때 출력해서 확인하기 편함
pd.options.display.max_columns = 100


# ### 데이터 로딩하기
# 
# 먼저 데이터를 로딩해오겠습니다. 데이터를 읽어올때는 [판다스(Pandas)](https://pandas.pydata.org/)의 [read_csv](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html) 라는 기능을 사용합니다.
# 
# 여기서 파일의 경로를 지정하는 방법에 주의하셔야 합니다. read_csv를 실행할 때 (**FileNotFoundError**)라는 이름의 에러가 난다면 경로가 제대로 지정이 되지 않은 것입니다. 

# **차주정보.csv**
# 
# 문법 연습을 할때 사용할 데이터는 신용카드 데이터 입니다. 금융데이터 허브(https://www.bigdata-finance.kr/dataset/datasetView.do?datastId=SET1400010)에서 수집한 데이터 입니다.
# 가장 처음 가져올 데이터는  ```차주정보.csv``` 입니다. 여기에는 신용정보원 일반신용정보DB에 등록된 개인(이하 차주)에 대한 인구통계 관련 정보를 제공합니다. 컬럼 정보는 다음과 같습니다.
# 
# - 차주 일련번호 : 차주정보와 대출,연체,카드 개설정보를 결합하기 위한 key
# - 생년 : 차주 출생년도(샘플링 시점 80세 이상은 '80세의 생년'으로 묶음<br>
#                        샘플링 시점 19세 이하는 '19세의 생년'으로 묶음)
# - 성별 : 1.남성, 2: 여성
# 
# 

# In[6]:


raw_data = pd.read_csv("data/차주정보.csv")


# In[7]:


# 0. raw_data의 개요를 확인하시오.

raw_data.info()


# In[8]:


#1. raw_data 변수에 할당된 데이터의 행렬 사이즈를 출력합니다.
# 출력은 (row, column) 으로 표시됩니다.
raw_data.shape


# In[9]:


# 2. raw_data의 처음과 마지막 5행씩을 출력하시오

raw_data.tail()
raw_data.head()


# In[11]:


# 3. raw_data의 컬럼명과 index 명을 확인하시오.

raw_data.columns
raw_data.index


# In[31]:


# 2. 1번에서 확인한 컬럼명을 아래와 같이 수정하시오
# strd_yymm : 수집년월
# deto_id : 사용자ID
# bth_yr : 생년
raw_data.rename(columns={'strd_yymm' : '수집년월','deto_id' : '사용자ID','bth_yr' : '생년'},inplace = True)


# In[32]:


raw_data.head()


# In[22]:


# 3. 1번에서 확인한 인덱스를 1부터 50 까지의 정수로 수정하시오
raw_data.set_index(np.arange(1,51))


# In[29]:


# 3. 출생년도를 4개의 카테고리로 분류하여 연령대 필드를 생성하시오. (청년(19~29세); 중년(30~49세); 장년(50~64세); 노년(65세 이상))
# 2020년 나이를 기준으로 경계(bins)는 직접 설정 하시오
raw_data.rename(columns={'bth_yr':'생년'},inplace = True)
lb = ['청년','중년','장년','노년']
bin = [19,30,50,65,100]
data = 2020 - raw_data['생년']
raw_data['연령대'] = pd.cut(data,bins = bin, labels = lb)


# In[33]:


raw_data.head()


# In[36]:


# 4. raw_data의 성별필드를 추가하되 sex_cd 필드의 값이 1이면 M, 2면 F 로 값을 정하시오

raw_data['성별'] = ['남' if i == 1 else '여' for i in raw_data.sex_cd]


# In[44]:


# 5. sex_cd 열을 삭제하시오.
del(raw_data['sex_cd'])


# In[46]:


raw_data.head(3)


# **카드개설정보.csv**
# 
# 문법 연습을 할때 사용할 데이터는 신용카드 데이터 입니다. 금융데이터 허브(https://www.bigdata-finance.kr/dataset/datasetView.do?datastId=SET1400010)에서 수집한 데이터 입니다.
# 이번에 가져올 데이터는  ```카드개설정보.csv``` 입니다. 여기에는 카드개설 관련정보를 카드 개설 기간동안 월말 스냅샷 형태로 제공합니다. 컬럼 정보는 다음과 같습니다.
# 
# - 기준년월 : 해당 데이터 수집 시점
# - 차주 일련번호 : 차주정보와 대출,연체,카드 개설정보를 결합하기 위한 key
# - 기관일련번호 : 카드개설정보와 대출.연체정보를 금융회사 단위로 결합하기 위한 key
# - 개설사유코드 : 0081:신용카드, 0083: 신용체크카드
# - 카드유형코드 : 1.개인카드, 2개인기업카드
# - 개설년월 : 카드 개설정보가 등록된 년월(YYYYMM)
# 
# 

# In[47]:


raw_data_open=pd.read_csv('data/카드개설정보.csv')


# In[48]:


#6. raw_data_open 데이터프레임의 필드수와 컬럼수를 확인하시오.
raw_data_open.shape


# In[49]:


#7. raw_data_open 데이터프레임의 앞부분 레코드 5개 뒷부분 레코드 5개를 확인하시오.
raw_data_open.head(5)
raw_data_open.tail(5)


# In[59]:


# 8.raw_data_open df의 index를 숫자 1~전체행수 로 설정하시오.
raw_data_open.set_index(np.arange(1,len(raw_data_open)+1),inplace = True)


# In[26]:


raw_data_open.tail()


# In[60]:


# 9. raw_data_open df의 컬럼명을 아래와 같이 변경하시오.
# strd_yymm : 수집년월
# card_open_strd_yymm : 1차수집년월
# deto_id : 사용자ID
# inst_id : 금융기관ID  
# card_open_yymm : 개설년월
raw_data_open.rename(columns={'strd_yymm' : '수집년월',
                              'card_open_strd_yymm' : '1차수집년월',
                              'deto_id' : '사용자ID',
                              'inst_id' : '금융기관ID',
                              'card_open_yymm' : '개설년월'},inplace = True)


# In[61]:


raw_data_open


# In[62]:


raw_data_open['개설년월']


# In[66]:


# 10. 카드개설년월필드에 대해서 카드개설연도 카드개설월로 필드를 분리하시오
raw_data_open['개설연도'] = [int(str(i)[:4]) for i in raw_data_open['개설년월']]
raw_data_open['개설월'] = [int(str(i)[4:]) for i in raw_data_open['개설년월']]


# In[31]:





# In[67]:


raw_data_open


# In[69]:


# 11. card_open_rson_nm 필드는 81이면 신용카드 83이면 신용체크카드를 의미한다 
# 개설유형 필드를 새로 생성하고 해당 코드에 맞는 유형으로 데이터를 변환하시오
raw_data_open['개설유형'] = ['신용카드' if i == 81 else '신용체크카드' for i in raw_data_open.card_open_rson_nm]


# In[70]:


raw_data_open


# In[72]:


# 12. card_typ_nm 필드는 개인카드(1)인지 개인기업카드(2)인지를 나타낸다
# 카드유형 필드를 새로 추가하고 card_typ_nm 값에 따라 개인/기업으로 나타내시오
raw_data_open['카드유형'] =['개인카드' if i == 1 else '개인기업카드' for i in raw_data_open.card_typ_nm] 

raw_data_open


# In[81]:


# 13. card_typ_nm 필드와 card_open_rson_nm 필드는 제거하시오

del raw_data_open['card_typ_nm']
del raw_data_open['card_open_rson_nm']


# In[82]:


raw_data_open.head()


# In[84]:


# 14. 카드개설연도 필드에 대해서 각 연대별로 카테고리를 구분하여 개설연대 필드를 생성하시오..
# 1990년대, 2000년대, 2010년대
lb = ['1990년대','2000년대','2010년대']
bin = [1990,1999,2009,2020]
raw_data_open['개설연대'] = pd.cut(raw_data_open.개설연도,bins = bin, labels = lb)


raw_data_open.head()


# In[85]:


# 15. 카드 개설 df와 차주정보 df를 memberID를 기준으로 병합하여 새로운 df로 저장하시오.
# inner_join 
fin_data = pd.merge(raw_data,raw_data_open,on = '사용자ID')

fin_data.head()


# In[120]:


# 16. 카드 개설 인원을 청년, 중년, 장년, 노년으로 비교할 수 있도록 그래프로 표현하시오

plt.figure(figsize = (10,6))
# pd.pivot_table(fin_data,index = '연령대',values = '성별', aggfunc = 'count').plot(kind='barh')
y = pd.value_counts(fin_data.연령대)
y.plot(kind='barh',color = ['r','y','b','g'])


# In[138]:


# 17 시간의 흐름에 따른 카드 개설 인원의 추이를 확인할 수 있는 그래프를 표현하시오.
a = pd.value_counts(fin_data['개설연도']).sort_index()

plt.plot(a)

# plt.hist(open_count)


# In[150]:


# 18 fin_data df를 이용하여 각 연대별 발급건수를 표현하는 피봇테이블을 생성하고 해당 테이블을 
# 사용하여 각 연대별 신용카드 발급 추이를 나타내는 그래프를 그리시오
p_year = pd.pivot_table(fin_data,index=['개설연도'],values=['성별'],aggfunc='count')
plt.plot(p_year)


# In[152]:


# 19 신용카드의 각 연도별 발급건수를 계산하고 연도별 오름차순으로 정렬하시오.
# 결과를 변수에 저장하시오
y_count=fin_data['개설연도'].value_counts().sort_index()


# In[44]:


# 20 19번에서 저장한 변수의 데이터를 활용하여 연도별 
# 개설건수에 대하여 시계열 그래프로 표현하시오.
plt.figure(figsize=(10,6))
plt.plot(y_count)


# In[153]:


# 21. 성별,연령대로 그룹화하여 카드 발급 건수를 표현하는 피봇테이블을 작성하고 변수에 저장하시오

c_count = pd.pivot_table(fin_data,index = ['성별','연령대'],values = ['생년'],aggfunc = 'count')


# ![](문제21_피봇.png)

# In[155]:


# 21. 21번에서 저장한 변수를 이용하여 아래와 같은 그래프를 작성하시오.
s=c_count.unstack(1)
s.plot(kind = 'bar')

