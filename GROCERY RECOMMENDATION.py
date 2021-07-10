#!/usr/bin/env python
# coding: utf-8

# In[5]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import numpy as np
import pandas as pd
import math
import json
import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
import joblib as jb
import scipy.sparse
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
import warnings; warnings.simplefilter('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Loading the dataset and add headers

# In[6]:


columns=['userId', 'productId', 'ratings','timestamp']
groceries_df=pd.read_csv('ratings_Grocery_and_Gourmet_Food.csv',names=columns)


# In[7]:


groceries_df


# In[8]:


groceries_df.drop('timestamp',axis=1,inplace=True)


# In[9]:


groceries_df.info()


# In[10]:


rows,columns=groceries_df.shape
print('Number of rows: ',rows)
print('Number of columns: ',columns)


# In[11]:


groceries_df.dtypes


# In[13]:


groceries_df1=groceries_df.iloc[:50000,0:]


# In[15]:


## Since the data is very big. Consider groceries_df1 named dataframe with first 50000 rows and all columns from 0 of dataset.


# In[16]:


groceries_df1.info()


# In[17]:


groceries_df1['ratings'].describe().transpose()


# In[18]:


#Finding the minimum and maximum ratings
print('Minimum rating is: %d' %(groceries_df1.ratings.min()))
print('Maximum rating is: %d' %(groceries_df1.ratings.max()))


# In[19]:


## Rating are on the scale 1 to 5.


# In[20]:


## now we handle the data as in check for the missing values as not all the consumers rate a certain product


# In[21]:


print('Number of missing values across columns: \n',groceries_df1.isnull().sum())


# In[22]:


# now lets check the ratings of the products
with sns.axes_style('white'):
    g = sns.factorplot("ratings", data=groceries_df1, aspect=2.0,kind='count')
    g.set_ylabels("Total number of ratings")


# In[24]:


# Number of unique user id  in the data
print('Number of unique users in Raw data = ', groceries_df1['userId'].nunique())
# Number of unique product id  in the data
print('Number of unique product in Raw data = ', groceries_df1['productId'].nunique())


# In[25]:


##  Taking the subset of dataset 
#Check the top 10 users based on ratings
most_rated=groceries_df1.groupby('userId').size().sort_values(ascending=False)[:10]
print('Top 10 users based on ratings: \n',most_rated)


# In[31]:


counts=groceries_df1.userId.value_counts()
groceries_df1_final=groceries_df1[groceries_df1.userId.isin(counts[counts>=15].index)]
print('Number of users who have rated 25 or more items =', len(groceries_df1_final))
print('Number of unique users in the final data = ', groceries_df1_final['userId'].nunique())
print('Number of unique products in the final data = ', groceries_df1_final['userId'].nunique())


# In[32]:


#constructing the pivot table
final_ratings_matrix = groceries_df1_final.pivot(index = 'userId', columns ='productId', values = 'ratings').fillna(0)
final_ratings_matrix.head()


# In[33]:


print('Shape of final_ratings_matrix: ', final_ratings_matrix.shape)


# In[34]:


#splitting the data


# In[35]:


train_data, test_data = train_test_split(groceries_df1_final, test_size = 0.3, random_state=0)
train_data.head()


# In[36]:


print('Shape of training data: ',train_data.shape)
print('Shape of testing data: ',test_data.shape)


# In[37]:


## Building Popularity Recommender model


# In[38]:


train_data_grouped = train_data.groupby('productId').agg({'userId': 'count'}).reset_index()
train_data_grouped.rename(columns = {'userId': 'score'},inplace=True)
train_data_grouped.head(40)


# In[39]:


#Sorting the products on recommendation score 
train_data_sort = train_data_grouped.sort_values(['score', 'productId'], ascending = [0,1]) 
      
#Generate a recommendation rank based upon score 
train_data_sort['rank'] = train_data_sort['score'].rank(ascending=0, method='first') 
          
#Get the top 5 recommendations 
popularity_recommendations = train_data_sort.head(5) 
popularity_recommendations


# In[40]:


# Use popularity based recommender model to make predictions
def recommend(user_id):     
    user_recommendations = popularity_recommendations 
          
    #Adding user_id column  
    user_recommendations['userId'] = user_id 
      
    # user_id column to the front 
    cols = user_recommendations.columns.tolist() 
    cols = cols[-1:] + cols[:-1] 
    user_recommendations = user_recommendations[cols] 
          
    return user_recommendations


# In[41]:


find_recom = [10,100,150]   # This list is user choice.
for i in find_recom:
    print("The list of recommendations for the userId: %d\n" %(i))
    print(recommend(i))    
    print("\n")


# In[42]:


#THE ABOVE MODEL DOESNT RECOMMEND PRODUCTS ON PERSONALIZATION BUT IT SHOWS THE MOST POPULAR


# In[45]:


#Building Collaborative Filtering recommender model.


# In[46]:


groceries_df_CF = pd.concat([train_data, test_data]).reset_index()
groceries_df_CF.head()


# In[47]:


#User Based Collaborative Filtering model


# In[48]:


pivot_df = groceries_df_CF.pivot(index = 'userId', columns ='productId', values = 'ratings').fillna(0)
pivot_df.head()


# In[49]:


print('Shape of the pivot table: ', pivot_df.shape)


# In[50]:


#defining user index from 0 to 10
pivot_df['user_index'] = np.arange(0, pivot_df.shape[0], 1)
pivot_df.head()


# In[51]:


##As this is a sparse matrix we will use SVD.


# In[52]:


U, sigma, Vt = svds(pivot_df, k = 10)


# In[53]:


print('Left singular matrix: \n',U)


# In[ ]:




