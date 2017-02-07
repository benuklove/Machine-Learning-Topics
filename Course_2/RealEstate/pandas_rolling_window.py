"""

  Created on 2/5/2017 by Ben

  benuklove@gmail.com
  
  

"""

import pandas as pd


d = {'A': pd.Series([1., 2., 3., 4., 5., 6.], index=['1/1/2000', '1/2/2000', '1/3/2000',
                                                     '1/4/2000', '1/5/2000', '1/6/2000']),
     'B': pd.Series([7., 8., 9., 10., 11., 12.], index=['1/1/2000', '1/2/2000', '1/3/2000',
                                                        '1/4/2000', '1/5/2000', '1/6/2000']),
     'C': pd.Series([13., 14., 15., 16., 17., 18.], index=['1/1/2000', '1/2/2000', '1/3/2000',
                                                           '1/4/2000', '1/5/2000', '1/6/2000'])}

df = pd.DataFrame(d)

print df

print df.rolling(window = 2).mean().applymap(round).shift()
