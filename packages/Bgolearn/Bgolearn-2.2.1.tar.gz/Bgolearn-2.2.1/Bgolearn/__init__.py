
__description__ = 'A Bayesian global optimization package'
__documents__ = 'https://bgolearn.netlify.app/'
__author__ = 'Bin CAO, ZheJiang LAB, Hangzhou, CHINA. (MGI, SHU, Shanghai, CHINA).'
__author_email__ = 'binjacobcao@gmail.com'
__url__ = 'https://github.com/Bin-Cao/Bgolearn'

import datetime
now = datetime.datetime.now()
formatted_date_time = now.strftime('%Y-%m-%d %H:%M:%S')

bgo_ = '''
Thank you for choosing Bgolearn for material design. 
Bgolearn is developed to facilitate the application of machine learning in research.
Bgolearn is designed for optimizing single-target material properties. 
If you need to perform multi-target optimization, here are two important reminders:

1. Multi-tasks can be converted into a single task using domain knowledge. 
For example, you can use a weighted linear combination in the simplest situation. That is, y = w*y1 + y2...

2. Multi-tasks can be optimized using Pareto fronts. 
Bgolearn will return two arrays based on your dataset: 
the first array is a evaluation score for each virtual sample, 
while the second array is the recommended data considering only the current optimized target.

The first array is crucial for multi-task optimization. 
For instance, in a two-task optimization scenario, you can evaluate each candidate twice for the two separate targets. 
Then, plot the score of target 1 for each sample on the x-axis and the score of target 2 on the y-axis. 
The trade-off consideration is to select the data located in the front of the banana curve.

I am delighted to invite you to participate in the development of Bgolearn. 
If you have any issues or suggestions, please feel free to contact me at binjacobcao@gmail.com.
'''

art = '''
██████╗  ██████╗  ██████╗ 
██╔══██╗██╔════╝ ██╔═══██╗
██████╔╝██║  ███╗██║   ██║
██╔══██╗██║   ██║██║   ██║
██████╔╝╚██████╔╝╚██████╔╝
╚═════╝  ╚═════╝  ╚═════╝ 
'''                       

print('A Bayesian global optimization package')
print('Bgolearn, Bin CAO, HKUST(GZ)')
print('Intro : https://bgolearn.netlify.app/')
print('URL : https://github.com/Bin-Cao/Bgolearn')
print('Executed on :',formatted_date_time, ' | Have a great day.')  
print(art)
print('='*80)
print(bgo_)
print('='*80)