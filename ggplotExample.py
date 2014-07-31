
# coding: utf-8

# In[1]:

from ggplot import *


# In[3]:

q =ggplot(mtcars, aes('mpg', 'qsec'))


# In[4]:

q += geom_point(colour='steelblue')


# In[5]:

q += scale_x_continuous(breaks=[10,20,30],
                        labels=['horrible','ok','awesome'])


# In[6]:

print q


# In[ ]:



