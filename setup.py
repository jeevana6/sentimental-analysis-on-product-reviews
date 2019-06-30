
from amazon_reviews import Amazon
obj=Amazon()
from tb import textb
t1=textb()
pol=t1.polar_list()
from senti_analysis import senti_analysis
s=senti_analysis()
s.cal_avg_pol(pol)
review,rating=s.tot_review_rating()
print(review,rating)


