import math


class senti_analysis(object):

    def cal_avg_pol(self,pol):
        self.tot_pol=sum(pol)
        self.avg_pol=round((self.tot_pol/len(pol)),1)
        #print(self.avg_pol)

    def tot_review_rating(self):
        if self.avg_pol>=-1 and  self.avg_pol<-0.5:
            self.overall_review="NEGETIVE REVIEW, FAIR PRODUCT, DON'T AGREE TO BUY THIS PRODUCT"
            self.overall_rating=" 1"
        elif self.avg_pol>=-0.5 and self.avg_pol<0.0:
            self.overall_review = "NEGETIVE REVIEW, GOOD PRODUCT, YOU MAY FIND SOMEOTHER BETTER PRODUCT THAN THIS"
            self.overall_rating = " 2"
        elif self.avg_pol>=0.0 and self.avg_pol<0.5:
            self.overall_review = "POSITIVE REVIEW,  VERY GOOD PRODUCT, YOU MAY BUY THIS PRODUCT"
            self.overall_rating = " 4"
        elif self.avg_pol>=0.5 and self.avg_pol<1.0:
            self.overall_review = "POSITIVE REVIEW, EXCELLENT  PRODUCT, BUY THIS PRODUCT"
            self.overall_rating = " 5"
        else:
            self.overall_review="NEUTRAL REVIEW,PROCEED TO BUY OR CHECK FEW MORE PRODUCTS"
            self.overall_rating = " 3"
        return self.overall_review,self.overall_rating




