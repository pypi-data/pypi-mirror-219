import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import math
import scipy.stats 
from scipy.optimize import least_squares
import scipy.stats



######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################## SECTION 1: Functions ########################################
######################################## SECTION 1: Functions ########################################
######################################## SECTION 1: Functions ########################################
######################################## SECTION 1: Functions ########################################
######################################## SECTION 1: Functions ########################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

def make_pretty(ax, title='', xTitle='', yTitle=''):
    '''
    Purpose: This function makes a few basic cosmetic adjustments to an input axes object.
             The objective is to serve as a "quick and dirty" way to make a plot more presentable.

    Input:
        - ax     (matplotlib axes object) : The axes object to which cosmetic adjustments will be made
        - title  (str)                    : Desired plot title
        - xTitle (str)                    : Desired x-axis label
        - yTitle (str)                    : Desired y-axis label

    Output: 
        - There is no output. The orginal copy of ax is altered directly.

    '''
    ax.spines['left'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['right'].set_color('black')

    ax.spines['left'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    
    ax.set_title(title, fontsize = 20)
    ax.set_xlabel(xTitle, fontsize=16)
    ax.yaxis.set_label_coords(-0.15, 0.5)
    ax.set_ylabel(yTitle, rotation = 'horizontal', fontsize = 16)
    
    ax.tick_params(axis='both', labelsize = 16)
    
    ax.grid(True)
    return


def scatter_bygroup(ax, x,y,col,colmap='hot'):
    '''
    Purpose:
        - Plot y against x in a scatterplot, where the points are coloured by a third variable, col.

    Input:
        - ax  (matplotlib axis) : The axis on which to add the scatter plot
        - x   (array/float)     : The data for the x-axis of the scatterplot
        - y   (array/float)     : The data for the y-axis of the scatterplot
        - col (list)            : A list of values of some variable which will correspond to groups. This 
                                  value is used to determine the colour of a point. Points with the same 
                                  'col' value will have the same colour.
        - colmap (str)          : A colormap for determining the group colours. Default to 'hot'.

   Output:
	- Note that there is no output, however, the original input axes object will be altered.
 
    '''
    # Set the color map to match the number of species
    uniq = list(set(col))
    z    = range(1,len(uniq))
   
    cNorm  = colors.Normalize(vmin=0, vmax=len(uniq))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=colmap)

    
    # Plot each group
    for i in range(len(uniq)):
        indx = (col == uniq[i])
        ax.scatter(x[indx], y[indx], s=150, color=scalarMap.to_rgba(i), label=uniq[i])
    return



def moving_average_baseline_subtraction(current, window_size, forward = True):
    '''
    Purpose:
        An iterative function that estimates the baseline of an input signal using a peak-stripping 
        moving average (i.e. a moving average algorithm designed to strip baselines off of peaks.) 
        The function is intended to be used on voltammograms collected via sweep-like voltammetry.

        A simple plot is printed with the baseline estimate overlayed on the input signal.



    Input:
        - current (array/float) : An array of values intended to be a peak-like signal with baseline
        - window_size (int)     : An integer indicating the number of points to be contained in a single window
                                of the moving average
        - forward (boolean)     : This variable is relevant in the context of voltammetric sweep-like data collection.
                                If true, the data in "current" was collected via a sweep-like voltammetric scan where
                                the potential/voltage was swept from a starting value to an increasingly positive
                                potential. If False, the potential/voltage swept from a starting value to increasingly
                                negative values.
                                The objective is essentially to ensure that peak-like structures in the data are "above"
                                the baseline - i.e. more positive than the baseline. If the peaks manifests below the 
                                baseline in your data (i.e. "trench-like" as opposed to peak-like), set this variable to 
                                False, and the algorithm will adjust itself accordingly.
      

  
    Output:
        - baseline (array/float)           : An array of values containing the BASELINE estimate of the algorithm
        - baseline_fig (matplotlib figure) : An overlay plot of the orignal signal and the estimated baseline. Note that
                                             the plot is printed within the function in addition to this output.
    '''
    num_leftover = -1
    
    
    num_samples = len(current)
    num_averages = math.floor(len(current)/window_size)
    
    flag = False # True if the number of samples is a non-integral multiple of window size
    if num_averages*window_size < num_samples:
        flag = True
    
    
    averages = np.zeros(num_averages)
    for i in range(0, num_averages):
        count = i+1
        averages[i] = np.mean((current[(count-1)*window_size:(count*window_size-1)]))
    
    
    # I'm not sure how this is handled in the real Nova algorithm so for now I'm just flagging it.
    if flag:
        num_leftover = len(current) - num_averages*window_size
        
    # If data was obtained on a reverse sweep, we want to read it from right to left for the moving average. We achieve this by flipping the 
    # direction of 'current' below:
    if not forward:
        current = current.iloc[::-1]
   
    temp_averages = averages
    for iteration in range(1000):
        tally = 0
        if forward:
            for i in range(1, num_averages-1):
                # Think about what would happen to an apex in the following: 
                if np.mean((averages[i-1], averages[i+1])) < averages[i]:
                    temp_averages[i] = np.mean((averages[i-1], averages[i+1]))
                    tally += 1
        else:
            for i in range(1, num_averages-1):
                if averages[i] < np.mean((averages[i-1], averages[i+1])):
                    temp_averages[i] = np.mean((averages[i-1], averages[i+1]))
                    tally += 1
            
        
        averages = temp_averages
        if tally == 0:  
            break
        
    # Flip current back, if it is reverse sweep data, since we are done with the moving average portion:
    if not forward:
        current = current.iloc[::-1] 
        
        
    # Interpolate the "betweens":
    baseline = np.zeros(len(current))
    baseline[0] = current[0]
    for i in range(num_averages):
        count = i+1
        baseline[(count*window_size-1)] = averages[i] 
        slope = (averages[i] - averages[i-1])/window_size
        intercept = averages[i-1]
        if i == 0:
            intercept = baseline[0]
            slope = (averages[i] - intercept)/window_size

        start = count*window_size - window_size
        for j in range(1, window_size):            
            baseline[start+j-1] = intercept + slope*j
       
    if flag:
        num_samples = len(current)
        
        start = window_size*num_averages + 1
        
        for i in range(start, num_samples):
            baseline[i] = current[i]
            
            


    
      
        

    return baseline





def get_groupwise_intervals(xdom, yran):
    '''
    Purpose:
        The purpose of this function is to group the input data and then calculate the the means, confidence bands, and prediction bands 
        of each groups. A group is defined by a fixed value of xdom. If many points have the same value of xdom, then they form a group.
        
        The function will output a the interpolated means, confidence interval edges, prediction interval edges, and standard deviations
        of each group. 
        
    Input:
        - xdom (array/float) : an array of points defining the x-coordinates of observations
        - yran (array/float) : an array of points defininf the y-coordinates of observations
        
    Output:
        - outList (list) : list containing 7 arrays
                                1. xUnique    (array/float) : contains the unique xdom values that define the groupings
                                2. means      (array/float) : contains the mean of each group
                                3. sampleSigs (array/float) : the SAMPLE standard deviation of each group (n-1 denominator)
                                4. CILow      (array/float) : lower limits of the CI for the mean of each group
                                5. CIUpp      (array/float) : upper limits of the CI for the mean of each group
                                6. PILow      (array/float) : lower limits of the PI for new observations from each group
                                7. PIUpp      (array/float) : upper limits of the PI for new observations from each group
                                
                        Note that the ith entry in each of the 7 arrays are associated with each other. That is, the ith entry in each array
                        defines a property of the ith group.
                        
                        Note that the limits are calculated at the 95% confidence level and assuming normality of data (i.e. the typical 
                        Student's t multiple of the [group] sample standard deviation. The results may therefore be erroenous for non-normally
                        distributed data.    
    '''

    xUnique = np.unique(xdom) # creates an array of the unique values in xdom
    numGroups = len(xUnique)

    # Create arrays of zeros that will be populated with 
    # the corresponding stats about each group. There is 
    # one entry for each group - i.e. for each unique value
    # of xdom
    means      = np.zeros(numGroups)
    CILow      = np.zeros(numGroups)
    CIUpp      = np.zeros(numGroups)
    PILow      = np.zeros(numGroups)
    PIUpp      = np.zeros(numGroups)
    sampleSigs = np.zeros(numGroups)
    for groupIndex in range(numGroups):
        mask = [val == xUnique[groupIndex] for val in xdom]
        xdat = xdom[mask]
        ydat = yran[mask]


        means[groupIndex] = np.mean(ydat)

        delta = ydat - means[groupIndex]
        sampleSigs[groupIndex] = np.sqrt(np.dot(delta, delta)/(len(delta)-1))

        t = scipy.stats.t.ppf(0.975, len(delta)-1)


        CILow[groupIndex] = means[groupIndex] - t*sampleSigs[groupIndex]/np.sqrt(len(delta))
        CIUpp[groupIndex] = means[groupIndex] + t*sampleSigs[groupIndex]/np.sqrt(len(delta))

        PILow[groupIndex] = means[groupIndex] - t*sampleSigs[groupIndex]*np.sqrt(1+1/len(delta))
        PIUpp[groupIndex] = means[groupIndex] + t*sampleSigs[groupIndex]*np.sqrt(1+1/len(delta))
    
    outList = [xUnique, means, sampleSigs, CILow, CIUpp, PILow, PIUpp]
    return outList


######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
########################################## SECTION 2: CLASSES ########################################
########################################## SECTION 2: CLASSES ########################################
########################################## SECTION 2: CLASSES ########################################
########################################## SECTION 2: CLASSES ########################################
########################################## SECTION 2: CLASSES ########################################
########################################## SECTION 2: CLASSES ########################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################


class linear_std_curve:
    '''
    Purpose:
        - To define a linear standard curve complete with prediction intervals, an error propagation formula for use with the delta method, 
          limits of estimation, and details about the creation of the curve, including smoothing parameters, baseline subtraction parameters,
          and calibration procedures.
    
    Attributes:
        - fit_params   (1D array/float) : An array containing the values of the fit coefficients of the linear model. form: [p0, p1], where linear(x) = p0 + p1*x
        - covar        (2D array/float) : the covariance matrix of the fit coefficients
        - s            (float)          : the MSE of the fit to the standard points
        - df           (int)            : the number of degrees of freedom in the standard curve, where the value is equal to the number of standard points minus the number of fit parameters 
        - Elow         (float)          : The lower edge of the peak window for the peak with which the curve was created. The curve is considered inaccurate below this value.
        - Eupp         (float)          : The upper edge of the peak window for the peak with which the curve was created. The curve is considered inaccurate above this value.
        - imin_est     (float)          : minimum current for use in inverse regression. Below this value, the standard curve must be extrapolated, which is poor practice.  
                                          It is the "y" value corresponding to conc_est_min as the "x" value.
        - imax_est     (float)          : maximum current for use in inverse regression. Above this value the standard curve must be extrapolated, which is poor practice.
                                          It is the "y" value corresponding to conc_est_max as the "x" value.
        - imin_std     (float)          : minimum current for obtaining a valid MLE for concentration. It is the "y" value corresponding to conc_std_min as the "x" value
        - imax_std     (float)          : maximum current for obtaining a valid MLE for concentration. It is the "y" value corresponding to conc_std_max as the "x" value
        - conc_est_min (float)          : the lowest possible value of concentration that can be estimated with a valid confidence interval (i.e. the estimate and its 95% limits fall within the non-extrapolated region)
        - conc_est_max (float)          : the largest value of concentratio nthat can be estimated with a valid confidence interval (i.e. the estimate and its 95% limits fall within the non-extrapolated region)
        - conc_std_min (float)          : the lowest concentration of all the std pts. Any MLE above this value and below conc_std_max is a valid MLE. However, the lower limit on the estimate will not be valid
                                          if the MLE is between conc_std_min and conc_est_min (i.e. the lower limit will require extrapolation of the prediction band's upper edge to be calculated... this is risky and is not recommended)
        - conc_std_max (float)          : the largest concentration of all the std pts. Any MLE below this value and above conc_std_min is a valid MLE. However, the upper limit on the estimate will not be valid
                                          if the MLE is between conc_std_ax and conc_est_max (i.e. the upper limit will require extrapolation of the prediction band's lower edge to be calculated... this is risky and is not recommended)
      
        - smoothing    (str)            : details regarding the smoothing procedure used when building the curve
        - baseline     (str)            : details regarding the baseline procedure used when building the curve  
        - calibration  (str)            : details regarding the calibration procedure used when building the curve
        - fit_data     (list)           : a list containing the x,y data for fitting a linear model
        - full_data    (list)           : if fit_data is a result of processing an original dataset, this attribute can be used to house the original, unprocessed data
   
    Methods/Functions:
        - fit             : performs least-squares regression using scipy.optimize.curve_fit. The function returns estimated fit coefficients, their covariance matrix,
                            and also populate various attributes of the linear_std_curve object including s, standard range, estimation range.
        - predict         : returns the value, y, of the standard curve at a particular input, x. This is essentially the MLE for the system response to the input, x.
        - details         : prints out a summary of the details of the standard curve
        - errprop         : the error propagation formula for a parabola. This method returns the value of the variance of the response variable, y, at a given input, x.
        - upper_pred_edge : returns the value of the upper edge of the prediction interval, with confidence alpha specified by the user, at a particular input, x.
                            This calculation makes use of the 'Delta Method' and uses the errprop method above within its calculation.
        - lower_pred_edge : analogous to upper_pred_edge but for the lower edge of the prediction interval
        - conc_est_min_loss : This function returns zero when the horizontal minimum current line intersects the best fit line. The concentration at the point of intersection is the 
                              minimum concentration estimate that can be reported with a valid lower limit. We solve for the point of intersection via least-squares minimization
                              and use the result to instantiate the conc_est_min parameter of the curve object
        - conc_est_max_loss : This function returns zero when the horizontal maximum current line intersects the best fit line. The concentration at the point of intersection is the 
                              maximum concentration estimate that can be reported with a valid upper limit. We solve for the point of intersecgtions via least-squares minimization
                              and use the result to instatiate the conc_est_max parameter of the curve object.
        - set_params        : This function can be used to manually adjust the values of the curve's parameters. The user will be queried with a simple i/o question & answer algorithm
                              where the user is prompeted to enter each parameter, one after the other.
    '''
               
    # How an instance of the class is initiated:
    def __init__(self, fit_params = np.array([0.,0.]), covar=np.zeros((2,2)), s=0., df=0, 
                 Elow=-2., Eupp=2., imin_est=0., imax_est=100., imin_std=0., imax_std=100,
                 conc_est_min=0.1, conc_est_max=5., conc_std_min=0.1, conc_std_max=100., 
                 smoothing='None', baseline='None', calibration='None', fit_data = [np.zeros(3), np.zeros(3)], 
                full_data = []):

        self.fit_params     = fit_params
        self.covar          = covar
        self.s              = s
        self.df             = df
        self.Elow           = Elow
        self.Eupp           = Eupp
        self.imin_std       = imin_std
        self.imax_std       = imax_std
        self.imin_est       = imin_est
        self.imax_est       = imax_est
        self.conc_est_min   = conc_est_min
        self.conc_est_max   = conc_est_max
        self.conc_std_min   = conc_std_min
        self.conc_std_max   = conc_std_max

        
        
        self.smoothing   = smoothing
        self.baseline    = baseline
        self.calibration = calibration
        
        self.fit_data    = fit_data
        

        return
    

    
    
    def fit(self, x_data, y_data):
        def linear_map(x, p0=0, p1=1):
            '''
            Purpose: 
                Map an argument, x, to a response, y, with a linear relationship given by:   f(x) = y = p0 + p1*x

            Input:
                - x         (float - array) : The argument for the linear mapping
                - p1        (float)         : the slope in the linear model
                - p0        (float)         : the intercept in the linear model

            Output:
                - y         (float)         : The response of the argument, x, under the linear model
            '''

            y = p0 + p1*x
            return y

        
        
        
        from scipy.optimize import curve_fit
        model          = linear_map
        bestest, covar = curve_fit(model, x_data, y_data)
        ddof           = len(bestest)
        
        self.fit_params = bestest
        self.covar      = covar
        self.df         = len(x_data) - ddof

        
        predictions = self.predict(x_data)
        sse = np.dot(predictions - y_data,predictions - y_data)
            

        mse  = sse/(len(y_data)-ddof)
        rmse = np.sqrt(mse)
        
        self.s            = rmse        
        self.conc_std_min = min(x_data)
        self.conc_std_max = max(x_data)
        self.fit_data[0]  = x_data
        self.fit_data[1]  = y_data
        
        
        # Below, we check if the linear fit slopes positively or negatively. The "standard scenario"
        # is where the slope is positive. If the slope is positive, then the lowest concentration
        # produces the lowest prediction. 
        a                 = self.predict(self.conc_std_min)
        b                 = self.predict(self.conc_std_max)
        standard_scenario = self.fit_params[1] >= 0
        if standard_scenario:
            self.imin_std = a
            self.imax_std = b
        else:
            self.imax_std = a
            self.imin_std = b
         
        
        if standard_scenario:
            self.imin_est     = self.upper_pred_edge(self.conc_std_min, 0.05)
            self.imax_est     = self.lower_pred_edge(self.conc_std_max, 0.05)

        else:
            self.imin_est     = self.upper_pred_edge(self.conc_std_max, 0.05)
            self.imax_est     = self.lower_pred_edge(self.conc_std_min, 0.05)
 
        if standard_scenario:
            self.conc_est_min = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
            self.conc_est_max = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        else:
            self.conc_est_max = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
            self.conc_est_min = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        
        
        return bestest, covar, sse
        
        
        
        
        return params, loss
    # Function for printing out the attributes of the object
    def details(self):
        print('Model : linear         --- y = p0 + p1*x')                                                                           
        print('[p0, p1] = {}'.format(self.fit_params))        
        print('--------------------------------------------------')                            
        print('covar :')
        print(self.covar)
        print('--------------------------------------------------')
        print('s                              = {}'.format(self.s))
        print('degrees of freedom             : {}'.format(self.df))
        print('Elow                           = {}'.format(self.Elow))
        print('Eupp                           = {}'.format(self.Eupp))
        print('imin_est                       = {}'.format(self.imin_est))
        print('imax_est                       = {}'.format(self.imax_est))
        print('imin_std                       = {}'.format(self.imin_std))
        print('imax_std                       = {}'.format(self.imax_std))
        print('conc_est_min                   = {}'.format(self.conc_est_min))
        print('conc_est_max                   = {}'.format(self.conc_est_max))
        print('conc_std_min                   = {}'.format(self.conc_std_min))
        print('conc_std_max                   = {}'.format(self.conc_std_max))
        
        print('Smoothing Procedure            : {}'.format(self.smoothing))
        print('Baseline Procedure             : {}'.format(self.baseline))
        print('Internal Calibration Procedure : {}'.format(self.calibration))
        return
    
    
    def set_params(self):
        # set the fit params:
        print('Model : linear         --- y = p0 + p1*x') # notifies the user of the function definition, implying the parameter notation
        for i in range(len(self.fit_params)):
            print('Enter p{} : '.format(i))
            self.fit_params[i] = float(input())
               
        covarShape = self.covar.shape
        for i in range(covarShape[0]):
            #start from i because the matrix is symmetrical:
            for j in range(i, covarShape[1]):
                self.covar[i][j] = float(input('Enter V{}{}'.format(i, j)))
                
        self.s = float(input('Enter model error, s: '))
        self.df = int(input('Enter the number of degrees of freedom of the model : '))

        self.Elow = float(input('Enter Elow : '))
        self.Eupp = float(input('Enter Eupp : '))
        self.conc_std_min = float(input('Enter conc_std_min : '))
        self.conc_std_max = float(input('Enter conc_std_max : '))

        self.smoothing    = str(input('Enter smoothing procedure abbreviation : '))
        self.baseline     = str(input('Enter baseline procedure abbreviation : '))
        self.calibration  = str(input('Enter calibration procedure abbreviation : '))
        
        a = self.predict(self.conc_std_min)
        b = self.predict(self.conc_std_max)
        if a<b:
            self.imin_std = a
            self.imax_std = b
        else:
            self.imax_std = a
            self.imin_std = b
         
        
        if a<b:
            self.imin_est     = self.upper_pred_edge(self.conc_std_min, 0.05)
            self.imax_est     = self.lower_pred_edge(self.conc_std_max, 0.05)
        else:
            self.imin_est     = self.upper_pred_edge(self.conc_std_max, 0.05)
            self.imax_est     = self.lower_pred_edge(self.conc_std_min, 0.05)
 
        if a<b:
            self.conc_est_min = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
            self.conc_est_max = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        else:
            self.conc_est_max = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
            self.conc_est_min = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
            

        return
        
    # This function IS the standard curve. It takes a concentration argument, x,  and maps it to the corresponding most likely current value, y
    def predict(self, x):
        '''
        Function : linear

        Purpose  : Apply a linear function to the input argument, x, where linear(x) = p0 + p1*x

        Input: 
            - x (float/array) : an array of floats to be used as an argument for the linear model
            - p1 (float)      : the coefficient for the first order (linear) term of the linear model
            - p0 (float)      : the zeroth order (constant) term of the linear model

        Output:
            - y (float/array) : The mapping of the argument, x, under the linear model
        '''
        t1 = self.fit_params[1]*x

        y = self.fit_params[0] + t1 

        #y = self.linear_map(x, self.fit_params[0], self.fit_params[1])
        return y
    
    
    # This function is the error propagation formula or the parabolic standard curve It requires the covariance of the fit parameters and will map a cocnentration, x, to the variance of the current at that concentration:
    def errprop(self, x, cov):
        '''
        Purpose:
            To compute the error propagation of a line whose coefficients have been estimated with some uncertainty. The terms use the typical error propagation formula, where each term is a product of 
            partial derivatives multiplied by the corresponding covariance term. The method is often called the "Delta Method"

            The parabola function takes the form:   y = p0 + p1*X

        Input:
            x   (array/float)    : argument to the linear model
            cov (2D array/float) : the covariance matrix of the three input parameters p0, p1, p2

        Output:
            varprop (array/float) : propagated error evaluated at the input argument
        '''  
        import numpy as np
    
        # Diagonal terms of the error prop:
        term_1 = np.power(x, 2)*cov[0][0]
        term_2 = cov[1][1]

        # Mixed terms of the error prop:
        term_3 = 2*x*cov[0][1]

        varprop = term_1 + term_2 + term_3 
        return varprop
    
    
    
    
    # The next two functions compute the prediction band edges about the best fit line, which is defined by the predict function 
    # (user chooses confidence level via alpha parameter)
    def upper_pred_edge(self, x, alpha):
        tail_perc = alpha/2.
        return self.predict(x) + scipy.stats.t.ppf(1.-tail_perc, self.df)*np.sqrt(self.errprop(x, self.covar) + self.s**2)
    
    def lower_pred_edge(self, x, alpha):    
        tail_perc = alpha/2.
        return self.predict(x) - scipy.stats.t.ppf(1.-tail_perc, self.df)*np.sqrt(self.errprop(x, self.covar) + self.s**2)
    
    
    def conc_est_min_loss(self, x):
        return self.predict(x) - self.imin_est
        
    def conc_est_max_loss(self, x):
        return self.predict(x) - self.imax_est
        



class parabola_std_curve:
    '''
    Purpose:
        - To define a parabolic standard curve complete with prediction intervals, an error propagation formula for use with the delta method, 
          limits of estimation, and details about the creation of the curve, including smoothing parameters, baseline subtraction parameters,
          and calibration procedures.
    
    Attributes:
        - fit_params   (1D array/float) : An array containing the values of the fit coefficients of the parabola. form: [p0, p1, p2], where parabola(x) = p2*x^2 + p1*x + p0
        - covar        (2D array/float) : the covariance matrix of the fit coefficients
        - s            (float)          : the MSE of the fit to the standard points
        - df           (int)            : the number of degrees of freedom in the standard curve, where the value is equal to the number of standard points minus the number of fit parameters 
        - Elow         (float)          : The lower edge of the peak window for the peak with which the curve was created. The curve is considered inaccurate below this value.
        - Eupp         (float)          : The upper edge of the peak window for the peak with which the curve was created. The curve is considered inaccurate above this value.
        - imin_est     (float)          : minimum current for use in inverse regression. Below this value, the standard curve must be extrapolated, which is poor practice.  
                                          It is the "y" value corresponding to conc_est_min as the "x" value.
        - imax_est     (float)          : maximum current for use in inverse regression. Above this value the standard curve must be extrapolated, which is poor practice.
                                          It is the "y" value corresponding to conc_est_max as the "x" value.
        - imin_std     (float)          : minimum current for obtaining a valid MLE for concentration. It is the "y" value corresponding to conc_std_min as the "x" value
        - imax_std     (float)          : maximum current for obtaining a valid MLE for concentration. It is the "y" value corresponding to conc_std_max as the "x" value
        - conc_est_min (float)          : the lowest possible value of concentration that can be estimated with a valid confidence interval (i.e. the estimate and its 95% limits fall within the non-extrapolated region)
        - conc_est_max (float)          : the largest value of concentratio nthat can be estimated with a valid confidence interval (i.e. the estimate and its 95% limits fall within the non-extrapolated region)
        - conc_std_min (float)          : the lowest concentration of all the std pts. Any MLE above this value and below conc_std_max is a valid MLE. However, the lower limit on the estimate will not be valid
                                          if the MLE is between conc_std_min and conc_est_min (i.e. the lower limit will require extrapolation of the prediction band's upper edge to be calculated... this is risky and is not recommended)
        - conc_std_max (float)          : the largest concentration of all the std pts. Any MLE below this value and above conc_std_min is a valid MLE. However, the upper limit on the estimate will not be valid
                                          if the MLE is between conc_std_ax and conc_est_max (i.e. the upper limit will require extrapolation of the prediction band's lower edge to be calculated... this is risky and is not recommended)
      
        - smoothing    (str)            : details regarding the smoothing procedure used when building the curve
        - baseline     (str)            : details regarding the baseline procedure used when building the curve  
        - calibration  (str)            : details regarding the calibration procedure used when building the curve

        - fit_data     (list)           : a list containing the x,y data for the data used to fit the parabolic model
        - full_data    (list)           : if fit_data is a result of processing an original dataset, this attribute can be used to house the original, unprocessed data. It is not necessary to fit.
    Methods/Functions:
        - fit               : performs least-squares regression using scipy.optimize.curve_fit. The function returns estimated fit coefficients, their covariance matrix,
                              and populates various attributes of the linear_std_curve object including s, standard range, estimation range.
        - predict           : returns the value, y, of the standard curve at a particular input, x. This is essentially the MLE for the system response to the input, x.
        - details           : prints out a summary of the details of the standard curve
        - errprop           : the error propagation formula for a parabola. This method returns the value of the variance of the response variable, y, at a given input, x.
        - upper_pred_edge   : returns the value of the upper edge of the prediction interval, with confidence alpha specified by the user, at a particular input, x.
                              This calculation makes use of the 'Delta Method' and uses the errprop method above within its calculation.
        - lower_pred_edge   : analogous to upper_pred_edge but for the lower edge of the prediction interval
        - conc_est_min_loss : This function returns zero when the horizontal minimum current line intersects the best fit line. The concentration at the point of intersection is the 
                              minimum concentration estimate that can be reported with a valid lower limit. We solve for the point of intersection via least-squares minimization
                              and use the result to instantiate the conc_est_min parameter of the curve object
        - conc_est_max_loss : This function returns zero when the horizontal maximum current line intersects the best fit line. The concentration at the point of intersection is the 
                              maximum concentration estimate that can be reported with a valid upper limit. We solve for the point of intersecgtions via least-squares minimization
                              and use the result to instatiate the conc_est_max parameter of the curve object.
        - set_params        : This function can be used to manually adjust the values of the curve's parameters. The user will be queried with a simple i/o question & answer algorithm
                              where the user is prompeted to enter each parameter, one after the other.
    '''
               
    # How an instance of the class is initiated:
    def __init__(self, fit_params = np.array([0.,0.,0.]), covar= np.zeros((3,3)),  s=0., df=0, 
                 Elow=-2, Eupp=2, imin_est=0., imax_est=100., imin_std=0., imax_std=100.,
                 conc_est_min=0., conc_est_max=5., conc_std_min=0., conc_std_max=100., 
                 smoothing='None', baseline='None', calibration='None', fit_data = [np.zeros(4), np.zeros(4)]):
        
        self.fit_params     = fit_params
        self.covar          = covar
        self.s              = s
        self.df             = df
        self.Elow           = Elow
        self.Eupp           = Eupp
        self.imin_std       = imin_std
        self.imax_std       = imax_std
        self.conc_est_min   = conc_est_min
        self.conc_est_max   = conc_est_max
        self.conc_std_min   = conc_std_min
        self.conc_std_max   = conc_std_max

        self.smoothing   = smoothing
        self.baseline    = baseline
        self.calibration = calibration
        
        self.fit_data    = fit_data
                                         
        return
    
    # Function for printing the attributes of the object:
    def details(self):
        print('Model : parabolic --- y = p0 + p1*x + p2*x^2')                                                                           
        print('[p0, p1, p2] = {}'.format(self.fit_params))        
        print('--------------------------------------------------')                            
        print('covar :')
        print(self.covar)
        print('--------------------------------------------------')
        print('s                              = {}'.format(self.s))
        print('degrees of freedom             : {}'.format(self.df))
        print('Elow                           = {}'.format(self.Elow))
        print('Eupp                           = {}'.format(self.Eupp))
        print('imin_est                       = {}'.format(self.imin_est))
        print('imax_est                       = {}'.format(self.imax_est))
        print('imin_std                       = {}'.format(self.imin_std))
        print('imax_std                       = {}'.format(self.imax_std))
        print('conc_est_min                   = {}'.format(self.conc_est_min))
        print('conc_est_max                   = {}'.format(self.conc_est_max))
        print('conc_std_min                   = {}'.format(self.conc_std_min))
        print('conc_std_max                   = {}'.format(self.conc_std_max))
        
        print('Smoothing Procedure            : {}'.format(self.smoothing))
        print('Baseline Procedure             : {}'.format(self.baseline))
        print('Internal Calibration Procedure : {}'.format(self.calibration))
        return
    
    
    def set_params(self):
        # set the fit params:
        print('Model : parabolic --- y = p2*x^2 + p1*x + p0') # notifies the user of the function definition, implying the parameter notation
        for i in range(len(self.fit_params)):
            print('Enter p{} : '.format(i))
            self.fit_params[i] = float(input())
               
        covarShape = self.covar.shape
        for i in range(covarShape[0]):
            #start from i because the matrix is symmetrical:
            for j in range(i, covarShape[1]):
                self.covar[i][j] = float(input('Enter V{}{}'.format(i, j)))
                
        self.s = float(input('Enter model error, s: '))
        self.df = int(input('Enter the number of degrees of freedom of the model : '))

        self.Elow = float(input('Enter Elow : '))
        self.Eupp = float(input('Enter Eupp : '))
        self.conc_std_min = float(input('Enter conc_std_min : '))
        self.conc_std_max = float(input('Enter conc_std_max : '))

        self.smoothing    = str(input('Enter smoothing procedure abbreviation : '))
        self.baseline     = str(input('Enter baseline procedure abbreviation : '))
        self.calibration  = str(input('Enter calibration procedure abbreviation : '))
        
        
        
        
        self.imin_std = self.predict(self.conc_std_min)
        self.imax_std = self.predict(self.conc_std_max)
        self.imin_est = self.upper_pred_edge(self.conc_std_min, 0.05)
        self.imax_est = self.lower_pred_edge(self.conc_std_max, 0.05)   

        self.conc_est_min = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        self.conc_est_max = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]

        return
        
    # This functio
                                         
                                        
        
    # This function IS the standard curve. It takes a concentration argument, x,  and maps it to the corresponding most likely current value, y
    def predict(self, x):
        '''
        Function : parabola

        Purpose  : Apply a parabolic function to the input argument, x, where parabola(x) = p2*x^2 + p1*x + p0

        Input: 
            - x (float/array) : an array of floats to be used as an argument for the parabolic function 
            - p2 (float)      : the coefficient for the second order term of the parabola 
            - p1 (float)      : the coefficient for the first order (linear) term of the parabola
            - p0 (float)      : the zeroth order (constant) term of the parabola

        Output:
            - y (float/array) : The mapping of the argument, x, under the parabolic function
        '''
    
        t2 = self.fit_params[2]*x**2.
        t1 = self.fit_params[1]*x

        y = self.fit_params[0] + t1 + t2


        return y
    
    
    # This function is the error propagation formula or the parabolic standard curve It requires the covariance of the fit parameters and will map a cocnentration, x, to the variance of the current at that concentration:
    def errprop(self, x, cov):
        '''
        Purpose:
            To compute the error propagation of a parabola whose coefficients have been estimated with some uncertainty. The terms use the typical error propagation formula, where each term is a product of partial derivatives
            multiplied by the corresponding covariance term.

            The parabola function takes the form:   y = p2*x^2 + p1*x + p0

        Input:
            x   (array/float)    : argument to the power law function
            cov (2D array/float) : the covariance matrix of the three input parameters p0, p1, p2

        Output:
            varprop (array/float) : propagated error evaluated at the input argument
        '''
        import numpy as np    

        # diagonal terms:
        t1 = np.power(x, 4.)*cov[2,2]
        t2 = np.power(x, 2.)*cov[1,1]
        t3 = cov[0,0]

        # mixing terms:
        t4 = 2*np.power(x, 3.)*cov[1,2]
        t5 = 2*np.power(x, 2.)*cov[0,2]
        t6 = 2*x*cov[0,1]

        # Combine for total variance:
        varprop = t1 + t2 + t3 + t4 + t5 + t6

        return varprop
    # The next two functions compute the prediction band edges about the best fit line, which is defined by the predict function 
    # (user chooses confidence level via alpha parameter)
    def upper_pred_edge(self, x, alpha):
        tail_perc = alpha/2.
        return self.predict(x) + scipy.stats.t.ppf(1.-tail_perc, self.df)*np.sqrt(self.errprop(x, self.covar) + self.s**2)
    
    def lower_pred_edge(self, x, alpha):    
        tail_perc = alpha/2.
        return self.predict(x) - scipy.stats.t.ppf(1.-tail_perc, self.df)*np.sqrt(self.errprop(x, self.covar) + self.s**2)
    
    def conc_est_min_loss(self, x):
        return self.predict(x) - self.imin_est
    def conc_est_max_loss(self, x):
        return self.predict(x) - self.imax_est
    
    
    
    
    def fit(self, x_data, y_data):
        def quadratic_map(x, p0=0, p1=0, p2 = 1):
            '''
            Purpose: 
                Map an argument, x, to a response, y, with a lquadratic relationship given by:   f(x) = y = p0 + p1*x + p2*x^2

            Input:
                - x         (float - array) : The argument for the linear mapping
                - p2        (float)         : the coefficient of the second order polynomial term
                - p1        (float)         : the coefficient of the 1st order polynomial term
                - p0        (float)         : the intercept/coefficient of the zeroth order poynomial term

            Output:
                - y         (float)         : The response of the argument, x, under the quadratic model
            '''

            y = p0 + p1*x + p2*x**2
            return y




        from scipy.optimize import curve_fit
        model          = quadratic_map
        bestest, covar = curve_fit(model, x_data, y_data)
        ddof           = len(bestest)

        self.fit_params = bestest
        self.covar      = covar
        self.df         = len(x_data) - ddof


        predictions = self.predict(x_data)
        sse = np.dot(predictions - y_data,predictions - y_data)


        mse  = sse/(len(y_data)-ddof)
        rmse = np.sqrt(mse)

        self.s            = rmse        
        self.conc_std_min = min(x_data)
        self.conc_std_max = max(x_data)
        self.fit_data[0]  = x_data
        self.fit_data[1]  = y_data

        self.imin_std = self.predict(self.conc_std_min)
        self.imax_std = self.predict(self.conc_std_max)
        self.imin_est = self.upper_pred_edge(self.conc_std_min, 0.05)
        self.imax_est = self.lower_pred_edge(self.conc_std_max, 0.05)   

        self.conc_est_min = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        self.conc_est_max = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        return bestest, covar, sse
    


class power_std_curve:
    '''
    Purpose:
        - To define a power-law standard curve via the quantile regression approach. Upper and lower quantile curves serve as the prediction interval for the best fit, which itself is defined by the 50% quantile,
          Details about the creation of the curve, including smoothing parameters baseline subtraction parameters,and calibration procedures are iuncluded, as well as the range and domain of 
          applicability of the curve for estimation purposes.
 
    
    Attributes:
        - fit_params   (1D array/float)    : An array containing the values of the fit coefficients of the power model. form: [p0, p1, p2], where power(x) = p0+p1*x^p2
        - low_edge_params (1D array/float) : An array containing the values of the fit coefficients of the power model for the lower quantile (or lower prediction edge). form: [p0_l, p1_l, p2_l], where y_l = p0_l + p1_l*x^p2_l
        - upp_edge_params (1D array/float) : An array containing the values of the fit coefficients of the power model for the upper quantile (or upper prediction edge). form: [p0_u, p1_u, p2_u], where y_u = p0_u + p1_u*x^p2_u
        - Elow         (float)             : The lower edge of the peak window for the peak with which the curve was created. The curve is considered inaccurate below this value.
        - Eupp         (float)             : The upper edge of the peak window for the peak with which the curve was created. The curve is considered inaccurate above this value.
        - imin_est     (float)             : minimum current for use in inverse regression. Below this value, the standard curve must be extrapolated, which is poor practice.  
                                             It is the "y" value corresponding to conc_est_min as the "x" value.
        - imax_est     (float)             : maximum current for use in inverse regression. Above this value the standard curve must be extrapolated, which is poor practice.
                                             It is the "y" value corresponding to conc_est_max as the "x" value.
        - imin_std     (float)             : minimum current for obtaining a valid MLE for concentration. It is the "y" value corresponding to conc_std_min as the "x" value
        - imax_std     (float)             : maximum current for obtaining a valid MLE for concentration. It is the "y" value corresponding to conc_std_max as the "x" value
        - conc_est_min (float)             : the lowest possible value of concentration that can be estimated with a valid confidence interval (i.e. the estimate and its 95% limits fall within the non-extrapolated region)
        - conc_est_max (float)             : the largest value of concentration that can be estimated with a valid confidence interval (i.e. the estimate and its 95% limits fall within the non-extrapolated region)
        - conc_std_min (float)             : the lowest concentration of all the std pts. Any MLE above this value and below conc_std_max is a valid MLE. However, the lower limit on the estimate will not be valid
                                             if the MLE is between conc_std_min and conc_est_min (i.e. the lower limit will require extrapolation of the prediction band's upper edge to be calculated... this is risky and is not recommended)
        - conc_std_max (float)             : the largest concentration of all the std pts. Any MLE below this value and above conc_std_min is a valid MLE. However, the upper limit on the estimate will not be valid
                                             if the MLE is between conc_std_ax and conc_est_max (i.e. the upper limit will require extrapolation of the prediction band's lower edge to be calculated... this is risky and is not recommended)
      
        - smoothing    (str)               : details regarding the smoothing procedure used when building the curve
        - baseline     (str)               : details regarding the baseline procedure used when building the curve  
        - calibration  (str)               : details regarding the calibration procedure used when building the curve
        - fit_data     (list)              : a list containing the x,y data of the linear fit
        - full_data    (list)              : if fit_data is a result of processing an original dataset, this attribute can be used to house the original, unprocessed data. This is not
                                             necessary for fitting
        
    Methods:
        - fit             : performs quantile regression on x,y data
                            The function returns estimated fit coefficients for three specified quantiles (default 0.025, 0.5, 0.975)
                            and populates various attributes of the power_std_curve object including fit_params, low_edge_params,
                            upp_edge_params, models, imin_std, imax_Std, imin_est, imax_est, conc_est_min, conc_est_max.

                            Output: 3-entry list (one for each quantile). Each entry is of the form,
                                                                    [
                                                                    quantile (float), 
                                                                    np.array([est of p0, est of p1, est of p2])
                                                                    ]
        - predict         : returns the median quantile for the prediction, y, of the standard curve at a particular input, x.
        - details         : prints out a summary of the details of the standard curve
        - set_params      : This function can be used to manually adjust the values of the curve's parameters. The user will be queried with a simple i/o question & answer algorithm
                            where the user is prompeted to enter each parameter, one after the other.
        - upper_pred_edge : returns the value of the upper edge of the prediction interval, with confidence alpha specified by the user, at a particular input, x.
                            This calculation makes use of the 'Delta Method' and uses the errprop method above within its calculation.
        - lower_pred_edge : analogous to upper_pred_edge but for the lower edge of the prediction interval
        - inv_pred        : Invert the predict function to obtain an estimate for x given a measured y
        - inv_low         : Invert the upper quantile function (upper_pred_edge) to obtain the lower limit for the estimate of x given a measured y
        - inv_upp         : Invert the lower quantile function (lower_pred_edge) to obtain the upper limit for the estimate of x given a measured y
   '''
    
    
    # How an instance of the class is initiated:
    def __init__(self, fit_params = np.array([0.,0.,0.]), low_edge_params = np.array([0.,0.,0.]), upp_edge_params = np.array([0.,0.,0.]), 
                 Elow=-2., Eupp=2., imin_est=0., imax_est=100., imin_std=0., imax_std=100.,
                 conc_est_min=0., conc_est_max=5., conc_std_min=0., conc_std_max=100., 
                 smoothing='None', baseline='None', calibration='None', fit_data = [np.zeros(4), np.zeros(4)],
                full_data=[]):

        self.fit_params      = fit_params
        self.low_edge_params = low_edge_params
        self.upp_edge_params = upp_edge_params
        self.Elow            = Elow
        self.Eupp            = Eupp
        self.imin_est        = imin_est
        self.imax_est        = imax_est
        self.imin_std        = imin_std
        self.imax_std        = imax_std
        self.conc_est_min    = conc_est_min
        self.conc_est_max    = conc_est_max
        self.conc_std_min    = conc_std_min
        self.conc_std_max    = conc_std_max

        self.smoothing       = smoothing
        self.baseline        = baseline
        self.calibration     = calibration
        
        self.fit_data = fit_data
        self.full_data = full_data
        
                                         
        return

    def fit(self, x_data, y_data, quantiles=[0.025, 0.5, 0.975], show_summary=True):     
        def power_model(x, p0=0, p1=1, p2=1):
            '''
            Purpose: 
                Map an argument, x, to a response, y, with a power law relationship given by:   f(x) = y = alpha*x^beta + gamma

            Input:
                - x  (float - array) : The argument for the power law function
                - p2 (float)         : the coefficient in the power law function
                - p1 (float)         : the exponent of the power law function
                - p0 (float)         : the intercept of the power law function
            Output:
                - y  (float)         : The response of the argument, x, under the power law function/mapping
            '''

            y = p1*(x**p2) + p0
            return y

        def quantile_loss(q, y, f):
            # q: Quantile to be evaluated, e.g., 0.5 for median.
            # y: True value.
            # f: Fitted (predicted) value.
            e = y - f
            return np.maximum(q * e, (q - 1) * e)


        from scipy.optimize import curve_fit
        bestest, covar = curve_fit(power_model, x_data, y_data, maxfev=2000) # the output of this is used as an intial guess in our quantile loss algorithm
        from scipy.optimize import minimize as minimize
        fit_results = []
        for q in quantiles:
            def power_quantileLoss(p):
                obs  = y_data
                nobs = len(obs)
                loss = 0
                for i in range(nobs):
                    f = power_model(x_data[i], *p)
                    loss+=quantile_loss(q, y_data[i], f)
                return loss
            fit_results.append([q, minimize(power_quantileLoss, x0=bestest,method='Nelder-Mead').x])

        


        p0_low = fit_results[0][1][0]
        p0_mid = fit_results[1][1][0]
        p0_upp = fit_results[2][1][0]
        
        p1_low = fit_results[0][1][1]
        p1_mid = fit_results[1][1][1]
        p1_upp = fit_results[2][1][1]
        
        p2_low = fit_results[0][1][2]
        p2_mid = fit_results[1][1][2]
        p2_upp = fit_results[2][1][2]
        
        
       
        
        
        self.fit_params[0]      = p0_mid
        self.fit_params[1]      = p1_mid
        self.fit_params[2]      = p2_mid
        
        self.low_edge_params[0]      = p0_low
        self.low_edge_params[1]      = p1_low
        self.low_edge_params[2]      = p2_low
        
        self.upp_edge_params[0]      = p0_upp
        self.upp_edge_params[1]      = p1_upp
        self.upp_edge_params[2]      = p2_upp
       
    
        self.conc_std_min = min(x_data)
        self.conc_std_max = max(x_data)
        self.fit_data[0]  = x_data
        self.fit_data[1]  = y_data

        self.imin_std = self.predict(self.conc_std_min)
        self.imax_std = self.predict(self.conc_std_max)
        self.imin_est = self.upper_pred_edge(self.conc_std_min)
        self.imax_est = self.lower_pred_edge(self.conc_std_max) 
        
        self.conc_est_min = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        self.conc_est_max = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]

        
    
        
    
        return fit_results
    
    
    # Function for printing out the attributes of the object
    def details(self):
        print('Model : power --- y = p0 + p1*x^p2')                                                                           
        print('[p0, p1, p2]       = {}'.format(self.fit_params))   
        print('[p0_l, p1_l, p2_l] = {}'.format(self.low_edge_params))   
        print('[p0_u, p1_u, p2_u] = {}'.format(self.upp_edge_params))   
        print('')
        print('Elow                           = {}'.format(self.Elow))
        print('Eupp                           = {}'.format(self.Eupp))
        print('imin_est                       = {}'.format(self.imin_est))
        print('imax_est                       = {}'.format(self.imax_est))
        print('imin_std                       = {}'.format(self.imin_std))
        print('imax_std                       = {}'.format(self.imax_std))
        print('conc_est_min                   = {}'.format(self.conc_est_min))
        print('conc_est_max                   = {}'.format(self.conc_est_max))
        print('conc_std_min                   = {}'.format(self.conc_std_min))
        print('conc_std_max                   = {}'.format(self.conc_std_max))
        
        print('Smoothing Procedure            : {}'.format(self.smoothing))
        print('Baseline Procedure             : {}'.format(self.baseline))
        print('Internal Calibration Procedure : {}'.format(self.calibration))
        return
    
    def set_params(self):
        # set the fit params:
        print('Enter the model fit parameters')
        print('Model : parabolic         --- y = p0 + p1*x^p2')  # Notifies the user of the functional form, implying the parameter definitions of the fit
        for i in range(len(self.fit_params)):
            print('Enter p{} : '.format(i))
            self.fit_params[i] = float(input())
            
            
        print('Enter lower quantile fit parameters  --- y_l = p0_l + p1_l*x^p2_l')
        for i in range(len(self.low_edge_params)):
            print('Enter p{}_l : '.format(i))
            self.low_edge_params[i] = float(input())
            
        print('Enter upper quantile fit parameters  --- y_u = p0_u + p1_u*x^p2_u')
        for i in range(len(self.upp_edge_params)):
            print('Enter p{}_u : '.format(i))
            self.upp_edge_params[i] = float(input())
            
                


        self.Elow         = float(input('Enter Elow : '))
        self.Eupp         = float(input('Enter Eupp : '))
        self.conc_std_min = float(input('Enter conc_std_min : '))
        self.conc_std_max = float(input('Enter conc_std_max : '))

        self.smoothing    = str(input('Enter smoothing procedure abbreviation : '))
        self.baseline     = str(input('Enter baseline procedure abbreviation : '))
        self.calibration  = str(input('Enter calibration procedure abbreviation : '))
        
                
        self.imin_std = self.predict(self.conc_std_min)
        self.imax_std = self.predict(self.conc_std_max)
        self.imin_est = self.upper_pred_edge(self.conc_std_min)
        self.imax_est = self.lower_pred_edge(self.conc_std_max)   

        self.conc_est_min = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        self.conc_est_max = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]

        
       
        return
        
    # This function IS the standard curve. It takes a concentration argument, x,  and maps it to the corresponding most likely current value, y
    def predict(self, x):
        '''
        Function : Power-law with intercept
        Purpose  : Apply a power function to the input argument, x, where power(x) = p0 + p1*x^p2

        Input: 
            - x (float/array) : an array of floats to be used as an argument for the power model

        Output:
            - y (float/array) : The mapping of the argument, x, under the power model
        '''
    
        # Terms:
        t0 = self.fit_params[0]
        t1 = self.fit_params[1]*(x**self.fit_params[2])

        # sum of terms:
        y = t0 + t1

        return y
    
    

    # The next two functions compute the prediction band edges about the best fit line, which is defined by the predict function 
    # (user chooses confidence level via alpha parameter)
    def upper_pred_edge(self, x):    
        t0 = self.upp_edge_params[0]
        t1 = self.upp_edge_params[1]*(x**self.upp_edge_params[2])
        y  =  t0 + t1
        return y
    
    def lower_pred_edge(self, x):   
        t0 = self.low_edge_params[0]
        t1 = self.low_edge_params[1]*(x**self.low_edge_params[2])
        y  = t0 + t1
        return y
    
    
        
    def conc_est_min_loss(self, x):
        return self.predict(x) - self.imin_est
    def conc_est_max_loss(self, x):
        return self.predict(x) - self.imax_est
    

class linear_QR:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    '''
    Purpose:
        - To define a linear standard curve via the quantile regression approach. Upper and lower quantile curves serve as the prediction interval for the best fit (defined by the 50% quantile))
          Details about the creation of the curve, including smoothing parameters baseline subtraction parameters,and calibration procedures are iuncluded, as well as the range and domain of 
          applicability of the curve for estimation purposes.
 
    
    Attributes:
        - fit_params   (1D array/float) : An array containing the values of the fit coefficients of the linear model. form: [p0, p1], where linear(x) = p0 + p1*x
        - low_edge_params (1D array/float) : An array containing the values of the fit coefficients of the linear model for the lower quantile (or lower prediction edge). form: [p0_l, p1_l], where y_l = p0_l + p1_l*x
        - upp_edge_params (1D array/float) : An array containing the values of the fit coefficients of the linear model for the upper quantile (or upper prediction edge). form: [p0_u, p1_u], where y_u = p0_u + p1_u*x
        - Elow         (float)          : The lower edge of the peak window for the peak with which the curve was created. The curve is considered inaccurate below this value.
        - Eupp         (float)          : The upper edge of the peak window for the peak with which the curve was created. The curve is considered inaccurate above this value.
        - imin_est     (float)          : minimum current for use in inverse regression. Below this value, the standard curve must be extrapolated, which is poor practice.  
                                          It is the "y" value corresponding to conc_est_min as the "x" value.
        - imax_est     (float)          : maximum current for use in inverse regression. Above this value the standard curve must be extrapolated, which is poor practice.
                                          It is the "y" value corresponding to conc_est_max as the "x" value.
        - imin_std     (float)          : minimum current for obtaining a valid MLE for concentration. It is the "y" value corresponding to conc_std_min as the "x" value
        - imax_std     (float)          : maximum current for obtaining a valid MLE for concentration. It is the "y" value corresponding to conc_std_max as the "x" value
        - conc_est_min (float)          : the lowest possible value of concentration that can be estimated with a valid confidence interval (i.e. the estimate and its 95% limits fall within the non-extrapolated region)
        - conc_est_max (float)          : the largest value of concentratio nthat can be estimated with a valid confidence interval (i.e. the estimate and its 95% limits fall within the non-extrapolated region)
        - conc_std_min (float)          : the lowest concentration of all the std pts. Any MLE above this value and below conc_std_max is a valid MLE. However, the lower limit on the estimate will not be valid
                                          if the MLE is between conc_std_min and conc_est_min (i.e. the lower limit will require extrapolation of the prediction band's upper edge to be calculated... this is risky and is not recommended)
        - conc_std_max (float)          : the largest concentration of all the std pts. Any MLE below this value and above conc_std_min is a valid MLE. However, the upper limit on the estimate will not be valid
                                          if the MLE is between conc_std_ax and conc_est_max (i.e. the upper limit will require extrapolation of the prediction band's lower edge to be calculated... this is risky and is not recommended)
      
        - smoothing    (str)            : details regarding the smoothing procedure used when building the curve
        - baseline     (str)            : details regarding the baseline procedure used when building the curve  
        - calibration  (str)            : details regarding the calibration procedure used when building the curve
        - fit_data     (list)           : a list containing the x,y data of the linear fit
        - full_data    (list)           : if fit_data is a result of processing an original dataset, this attribute can be used to house the original, unprocessed data. This is not
                                          necessary for fitting
        - models       (list)           : a list of the fitted linear models for each quantile - models are of statsmodels.formula.api.quantreg
   
    Methods:
        - fit             : performs quantile regression using statsmodels.formula.api.quantreg.
                            The function returns estimated fit coefficients for three specified quantiles (default 0.025, 0.5, 0.975)
                            and populates various attributes of the linear_QR object including fit_params, low_edge_params,
                            upp_edge_params, models, imin_std, imax_Std, imin_est, imax_est, conc_est_min, conc_est_max.

                            Output: 3-entry list (one for each quantile). Each entry is of the form
                                                                    [quantile (float), 
                                                                    np.array([lower lim of intercept , est of intercept, upper lim of intercept]), 
                                                                    np.array([lower lim of slope, est of slope, upper lim of slope]),
                                                                    a linear quantile regression model from statsmodels.formula.api.quantreg]

                                                                    where the intercept and slope limits are at alpha level 0.05

        - predict         : returns the median quantile for the prediction, y, of the standard curve at a particular input, x.
        - details         : prints out a summary of the details of the standard curve
        - set_params      : This function can be used to manually adjust the values of the curve's parameters. The user will be queried with a simple i/o question & answer algorithm
                            where the user is prompeted to enter each parameter, one after the other.
        - upper_pred_edge : returns the value of the upper edge of the prediction interval, with confidence alpha specified by the user, at a particular input, x.
                            This calculation makes use of the 'Delta Method' and uses the errprop method above within its calculation.
        - lower_pred_edge : analogous to upper_pred_edge but for the lower edge of the prediction interval
        - inv_pred        : Invert the predict function to obtain an estimate for x given a measured y
        - inv_low         : Invert the upper quantile function (upper_pred_edge) to obtain the lower limit for the estimate of x given a measured y
        - inv_upp         : Invert the lower quantile function (lower_pred_edge) to obtain the upper limit for the estimate of x given a measured y
    '''
    
 


    # How an instance of the class is instatiated:
    def __init__(self, fit_params = np.array([0.,0.]), low_edge_params = np.array([0.,0.]), upp_edge_params = np.array([0.,0.]), 
                 Elow=-2., Eupp=2., imin_est=0., imax_est=100., imin_std=0., imax_std=100.,
                 conc_est_min=0., conc_est_max=5., conc_std_min=0., conc_std_max=100., 
                 smoothing='None', baseline='None', calibration='None', fit_data = [np.zeros(3), np.zeros(3)],
                full_data=[], models = []):

        self.fit_params      = fit_params
        self.low_edge_params = low_edge_params
        self.upp_edge_params = upp_edge_params
        self.Elow            = Elow
        self.Eupp            = Eupp
        self.imin_est        = imin_est
        self.imax_est        = imax_est
        self.imin_std        = imin_std
        self.imax_std        = imax_std
        self.conc_est_min    = conc_est_min
        self.conc_est_max    = conc_est_max
        self.conc_std_min    = conc_std_min
        self.conc_std_max    = conc_std_max

        self.smoothing       = smoothing
        self.baseline        = baseline
        self.calibration     = calibration
        
        self.fit_data  = fit_data
        self.full_data = full_data
        self.models    = models
        
                                         
        return

    def fit(self, x_data, y_data, quantiles=[0.025, 0.5, 0.975], show_summary=True):     
        import statsmodels.formula.api as smf
        import pandas as pd
        import math
        data = pd.DataFrame(data={'X': x_data, 'Y':y_data})


        mod = smf.quantreg('Y ~ X', data)
        def fit_model(q):
            modfit = mod.fit(q=q)
            if show_summary:
                print('---------------------------------------------')
                print('---------------------------------------------')
                print('---------------------------------------------')
                print('---------------------------------------------')
                print('Quantile: {}'.format(q))
                print(modfit.summary())
            return [q, 
                    np.array([modfit.conf_int().loc['Intercept'][0], modfit.params['Intercept'], modfit.conf_int().loc['Intercept'][1]]), 
                    np.array([modfit.conf_int().loc['X'][0], modfit.params['X'], modfit.conf_int().loc['X'][1]]),
                    modfit] 
        
        fit_results = [fit_model(q) for q in quantiles]


        slope_low = fit_results[0][2][1]
        slope_mid = fit_results[1][2][1]
        slope_upp = fit_results[2][2][1]
        
        int_low   = fit_results[0][1][1]
        int_mid   = fit_results[1][1][1]
        int_upp   = fit_results[2][1][1]
        
        mod_low   = fit_results[0][3]
        mod_mid   = fit_results[1][3]
        mod_upp   = fit_results[2][3]
        
        
        
        self.fit_params[0]      = int_mid
        self.fit_params[1]      = slope_mid
        
        self.low_edge_params[0] = int_low
        self.low_edge_params[1] = slope_low
        
        self.upp_edge_params[0] = int_upp
        self.upp_edge_params[1] = slope_upp
        self.models = [x[3] for x in fit_results]
        
        checklist = [int_low, slope_low, int_upp, slope_upp]
        
        checks = [math.isnan(x) for x in checklist]
        
        if any(checks):
            print('Unable to compute some estimates. You may have insufficient data for chosen quantiles.\nTry raising lower quantile and/or lowering upper quantile.')
            print('Recommend checking model summaries of output.')
            return fit_results
        self.conc_std_min = min(x_data)
        self.conc_std_max = max(x_data)
        self.fit_data[0]  = x_data
        self.fit_data[1]  = y_data

        self.imin_std = self.predict(self.conc_std_min)
        self.imax_std = self.predict(self.conc_std_max)
        self.imin_est = self.upper_pred_edge(self.conc_std_min)
        self.imax_est = self.lower_pred_edge(self.conc_std_max) 
        
        self.conc_est_min = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        self.conc_est_max = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]

        
       
        return fit_results
    
    
    # Function for printing out the attributes of the object
    def details(self):
        print('Model : linear         --- y = p0 + p1*x')                                                                           
        print('[p0, p1]     = {}'.format(self.fit_params))   
        print('[p0_l, p1_l] = {}'.format(self.low_edge_params))   
        print('[p0_u, p1_u] = {}'.format(self.upp_edge_params))   
        print('')
        print('Elow                           = {}'.format(self.Elow))
        print('Eupp                           = {}'.format(self.Eupp))
        print('imin_est                       = {}'.format(self.imin_est))
        print('imax_est                       = {}'.format(self.imax_est))
        print('imin_std                       = {}'.format(self.imin_std))
        print('imax_std                       = {}'.format(self.imax_std))
        print('conc_est_min                   = {}'.format(self.conc_est_min))
        print('conc_est_max                   = {}'.format(self.conc_est_max))
        print('conc_std_min                   = {}'.format(self.conc_std_min))
        print('conc_std_max                   = {}'.format(self.conc_std_max))
        
        print('Smoothing Procedure            : {}'.format(self.smoothing))
        print('Baseline Procedure             : {}'.format(self.baseline))
        print('Internal Calibration Procedure : {}'.format(self.calibration))
        return
    
    
    def set_params(self):
        # set the fit params:
        print('Enter the model fit parameters')
        print('Model : linear         --- y = p0 + p1*x')  # Notifies the user of the functional form, implying the parameter definitions of the fit
        for i in range(len(self.fit_params)):
            print('Enter p{} : '.format(i))
            self.fit_params[i] = float(input())
            
            
        print('Enter lower quantile fit parameters  --- y_l = p0_l + p1_l*x')
        for i in range(len(self.low_edge_params)):
            print('Enter p{}_l : '.format(i))
            self.low_edge_params[i] = float(input())
            
        print('Enter upper quantile fit parameters  --- y_u = p0_u + p1_u*x')
        for i in range(len(self.upp_edge_params)):
            print('Enter p{}_u : '.format(i))
            self.upp_edge_params[i] = float(input())
            
                


        self.Elow         = float(input('Enter Elow : '))
        self.Eupp         = float(input('Enter Eupp : '))
        self.conc_std_min = float(input('Enter conc_std_min : '))
        self.conc_std_max = float(input('Enter conc_std_max : '))

        self.smoothing    = str(input('Enter smoothing procedure abbreviation : '))
        self.baseline     = str(input('Enter baseline procedure abbreviation : '))
        self.calibration  = str(input('Enter calibration procedure abbreviation : '))
        
       
        self.imin_std = self.predict(self.conc_std_min)
        self.imax_std = self.predict(self.conc_std_max)
        self.imin_est = self.upper_pred_edge(self.conc_std_min)
        self.imax_est = self.lower_pred_edge(self.conc_std_max)   

        self.conc_est_min = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        self.conc_est_max = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]

        return
        
    # This function IS the standard curve. It takes a concentration argument, x,  and maps it to the corresponding most likely current value, y
    def predict(self, x):
        '''
        Function : linear

        Purpose  : Apply a linear function to the input argument, x, where linear(x) = p0 + p1*x, and p0 & p1 are intercept and slope parameters, already defined

        Input: 
            - x (float/array) : an array of floats to be used as an argument for the linear model

        Output:
            - y (float/array) : The mapping of the argument, x, under the linear model
        '''
    
        t1 = self.fit_params[1]*x

        y = self.fit_params[0] + t1 
        return y
    
    
    # This function is the error propagation formula or the parabolic standard curve It requires the covariance of the fit parameters and will map a cocnentration, x, to the variance of the current at that concentration:
    
    # The next two functions compute the prediction band edges about the best fit line, which is defined by the predict function 
    # (user chooses confidence level via alpha parameter)
    def upper_pred_edge(self, x):       
        t1 = self.upp_edge_params[1]*x
        t0 = self.upp_edge_params[0]
        y  =  t0 + t1
        return y
    
    def lower_pred_edge(self, x):    
        t0 = self.low_edge_params[0]
        t1 = self.low_edge_params[1]*x
        
        y = t0 + t1
        return y
    
    
    def inv_pred(self, y_meas):
        x_est = (y_meas - self.fit_params[0])/self.fit_params[1]    
        
        return x_est
    
    def inv_lower(self, y_meas):
        x_low = (y_meas - self.upp_edge_params[0])/self.upp_edge_params[1]
        return x_low
    
    def inv_upper(self, y_meas):
        x_upp = (y_meas - self.low_edge_params[0])/self.upp_edge_params[1]
        return x_upp
        
        
    def conc_est_min_loss(self, x):
        return self.predict(x) - self.imin_est
    def conc_est_max_loss(self, x):
        return self.predict(x) - self.imax_est


class parabolic_QR:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    '''
    Purpose:
        - To define a parabolic standard curve via the quantile regression approach. Upper and lower quantile curves serve as the prediction interval for the best fit (defined by the 50% quantile))
          Details about the creation of the curve, including smoothing parameters baseline subtraction parameters,and calibration procedures are iuncluded, as well as the range and domain of 
          applicability of the curve for estimation purposes.
 
    
    Attributes:
        - fit_params   (1D array/float)    : An array containing the values of the fit coefficients of the parabolic model. form: [p0, p1, p2], where parabola(x) = p0 + p1*x + p2*x^2
        - low_edge_params (1D array/float) : An array containing the values of the fit coefficients of the parabolic model for the lower quantile (or lower prediction edge). form: [p0_l, p1_l], where y_l = p0_l + p1_l*x + p2_l*x^2
        - upp_edge_params (1D array/float) : An array containing the values of the fit coefficients of the parabolic model for the upper quantile (or upper prediction edge). form: [p0_u, p1_u], where y_u = p0_u + p1_u*x + p2_u*x^2
        - Elow         (float)             : The lower edge of the peak window for the peak with which the curve was created. The curve is considered inaccurate below this value.
        - Eupp         (float)             : The upper edge of the peak window for the peak with which the curve was created. The curve is considered inaccurate above this value.
        - imin_est     (float)             : minimum current for use in inverse regression. Below this value, the standard curve must be extrapolated, which is poor practice.  
                                             It is the "y" value corresponding to conc_est_min as the "x" value.
        - imax_est     (float)             : maximum current for use in inverse regression. Above this value the standard curve must be extrapolated, which is poor practice.
                                             It is the "y" value corresponding to conc_est_max as the "x" value.
        - imin_std     (float)             : minimum current for obtaining a valid MLE for concentration. It is the "y" value corresponding to conc_std_min as the "x" value
        - imax_std     (float)             : maximum current for obtaining a valid MLE for concentration. It is the "y" value corresponding to conc_std_max as the "x" value
        - conc_est_min (float)             : the lowest possible value of concentration that can be estimated with a valid confidence interval (i.e. the estimate and its 95% limits fall within the non-extrapolated region)
        - conc_est_max (float)             : the largest value of concentratio nthat can be estimated with a valid confidence interval (i.e. the estimate and its 95% limits fall within the non-extrapolated region)
        - conc_std_min (float)             : the lowest concentration of all the std pts. Any MLE above this value and below conc_std_max is a valid MLE. However, the lower limit on the estimate will not be valid
                                             if the MLE is between conc_std_min and conc_est_min (i.e. the lower limit will require extrapolation of the prediction band's upper edge to be calculated... this is risky and is not recommended)
        - conc_std_max (float)             : the largest concentration of all the std pts. Any MLE below this value and above conc_std_min is a valid MLE. However, the upper limit on the estimate will not be valid
                                             if the MLE is between conc_std_ax and conc_est_max (i.e. the upper limit will require extrapolation of the prediction band's lower edge to be calculated... this is risky and is not recommended)
      
        - smoothing    (str)               : details regarding the smoothing procedure used when building the curve
        - baseline     (str)               : details regarding the baseline procedure used when building the curve  
        - calibration  (str)               : details regarding the calibration procedure used when building the curve
        - fit_data     (list)              : a list containing the x,y data of the lparabolic fit
        - full_data    (list)              : if fit_data is a result of processing an original dataset, this attribute can be used to house the original, unprocessed data. This is not
                                             necessary for fitting
        - models       (list)              : a list of the fitted parabolic models for each quantile - models are of statsmodels.formula.api.quantreg
   
    Methods:
        - fit             : performs quantile regression using statsmodels.formula.api.quantreg.
                            The function returns estimated fit coefficients for three specified quantiles (default 0.025, 0.5, 0.975)
                            and populates various attributes of the parabolic_QR object including fit_params, low_edge_params,
                            upp_edge_params, models, imin_std, imax_Std, imin_est, imax_est, conc_est_min, conc_est_max.

                        Output: 3-entry list (one for each quantile). Each entry is of the form
                                                                    [quantile (float), 
                                                                    np.array([lower lim of p0 , est of p0, upper lim of p0]), 
                                                                    np.array([lower lim of p1 , est of p1, upper lim of p1]),
                                                                    np.array([lower lim of p2 , est of p2, upper lim of p2])
                                                                    a linear quantile regression model from statsmodels.formula.api.quantreg]

                                                                where the p0, p1, p2 limits are at alpha level 0.05
                                                                
        - predict         : returns the median quantile for the prediction, y, of the standard curve at a particular input, x.
        - details         : prints out a summary of the details of the standard curve
        - set_params      : This function can be used to manually adjust the values of the curve's parameters. The user will be queried with a simple i/o question & answer algorithm
                            where the user is prompeted to enter each parameter, one after the other.
        - upper_pred_edge : returns the value of the upper edge of the prediction interval, with confidence alpha specified by the user, at a particular input, x.
                            This calculation makes use of the 'Delta Method' and uses the errprop method above within its calculation.
        - lower_pred_edge : analogous to upper_pred_edge but for the lower edge of the prediction interval
        - inv_pred        : Invert the predict function to obtain an estimate for x given a measured y
        - inv_low         : Invert the upper quantile function (upper_pred_edge) to obtain the lower limit for the estimate of x given a measured y
        - inv_upp         : Invert the lower quantile function (lower_pred_edge) to obtain the upper limit for the estimate of x given a measured y
    '''
    

    # How an instance of the class is initiated:
    def __init__(self, fit_params = np.array([0.,0.,0.]), low_edge_params = np.array([0.,0.,0.]), upp_edge_params = np.array([0.,0.,0.]), 
                 Elow=-2., Eupp=2., imin_est=0., imax_est=100., imin_std=0., imax_std=100.,
                 conc_est_min=0., conc_est_max=5., conc_std_min=0., conc_std_max=100., 
                 smoothing='None', baseline='None', calibration='None', fit_data = [np.zeros(4), np.zeros(4)],
                full_data = [], models = []):

        self.fit_params      = fit_params
        self.low_edge_params = low_edge_params
        self.upp_edge_params = upp_edge_params
        self.Elow            = Elow
        self.Eupp            = Eupp
        self.imin_est        = imin_est
        self.imax_est        = imax_est
        self.imin_std        = imin_std
        self.imax_std        = imax_std
        self.conc_est_min    = conc_est_min
        self.conc_est_max    = conc_est_max
        self.conc_std_min    = conc_std_min
        self.conc_std_max    = conc_std_max

        self.smoothing       = smoothing
        self.baseline        = baseline
        self.calibration     = calibration
        
        self.fit_data  = fit_data
        self.full_data = full_data
        self.models    = models
        
                                         
        return

    def fit(self, x_data, y_data, quantiles=[0.025, 0.5, 0.975], show_summary=True):     
        import statsmodels.formula.api as smf
        import pandas as pd
        import math
        data = pd.DataFrame(data={'X': x_data, 'X2' : x_data**2, 'Y':y_data})
        mod  = smf.quantreg('Y ~ X2 + X', data)
        
        def fit_model(q):
            modfit = mod.fit(q=q)
            if show_summary:
                print('---------------------------------------------')
                print('---------------------------------------------')
                print('---------------------------------------------')
                print('---------------------------------------------')
                print('Quantile: {}'.format(q))
                print(modfit.summary())
            return [q,
                    np.array([modfit.conf_int().loc['Intercept'][0], modfit.params['Intercept'], modfit.conf_int().loc['Intercept'][1]]), 
                    np.array([modfit.conf_int().loc['X'][0]        , modfit.params['X']        , modfit.conf_int().loc['X'][1]]), 
                    np.array([modfit.conf_int().loc['X2'][0]       , modfit.params['X2']       , modfit.conf_int().loc['X2'][1]]),
                    modfit
                   ] 
        models = [fit_model(x) for x in quantiles]
        
        fit_results = [fit_model(q) for q in quantiles]


        p0_low = fit_results[0][1][1]
        p0_mid = fit_results[1][1][1]
        p0_upp = fit_results[2][1][1]
        
        p1_low = fit_results[0][2][1]
        p1_mid = fit_results[1][2][1]
        p1_upp = fit_results[2][2][1]
        
        p2_low = fit_results[0][3][1]
        p2_mid = fit_results[1][3][1]
        p2_upp = fit_results[2][3][1]
        
        
       
        
        
        self.fit_params[0]      = p0_mid
        self.fit_params[1]      = p1_mid
        self.fit_params[2]      = p2_mid
        
        self.low_edge_params[0]      = p0_low
        self.low_edge_params[1]      = p1_low
        self.low_edge_params[2]      = p2_low
        
        self.upp_edge_params[0]      = p0_upp
        self.upp_edge_params[1]      = p1_upp
        self.upp_edge_params[2]      = p2_upp
        
        self.models = [x[4] for x in fit_results]
        
        checklist = [p0_low, p1_low, p2_low, p0_upp, p1_upp, p2_upp]
        
        checks = [math.isnan(x) for x in checklist]
        
        if any(checks):
            print('Unable to compute some estimates. You may have insufficient data for chosen quantiles.\nTry raising lower quantile and/or lowering upper quantile.')
            print('Recommend checking model summaries of output.')
            return fit_results
        
        self.conc_std_min = min(x_data)
        self.conc_std_max = max(x_data)
        self.fit_data[0]  = x_data
        self.fit_data[1]  = y_data

        self.imin_std = self.predict(self.conc_std_min)
        self.imax_std = self.predict(self.conc_std_max)
        self.imin_est = self.upper_pred_edge(self.conc_std_min)
        self.imax_est = self.lower_pred_edge(self.conc_std_max) 
        
        self.conc_est_min = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        self.conc_est_max = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]

        
       
        return fit_results
    
    
    # Function for printing out the attributes of the object
    def details(self):
        print('Model : parabolic        --- y = p0 + p1*x + p2*x^2')                                                                           
        print('[p0, p1, p2]     = {}'.format(self.fit_params))   
        print('[p0_l, p1_l, p2_l] = {}'.format(self.low_edge_params))   
        print('[p0_u, p1_u, p2_u] = {}'.format(self.upp_edge_params))   
        print('')
        print('Elow                           = {}'.format(self.Elow))
        print('Eupp                           = {}'.format(self.Eupp))
        print('imin_est                       = {}'.format(self.imin_est))
        print('imax_est                       = {}'.format(self.imax_est))
        print('imin_std                       = {}'.format(self.imin_std))
        print('imax_std                       = {}'.format(self.imax_std))
        print('conc_est_min                   = {}'.format(self.conc_est_min))
        print('conc_est_max                   = {}'.format(self.conc_est_max))
        print('conc_std_min                   = {}'.format(self.conc_std_min))
        print('conc_std_max                   = {}'.format(self.conc_std_max))
        
        print('Smoothing Procedure            : {}'.format(self.smoothing))
        print('Baseline Procedure             : {}'.format(self.baseline))
        print('Internal Calibration Procedure : {}'.format(self.calibration))
        return
    
    

    
    def set_params(self):
        # set the fit params:
        print('Enter the model fit parameters')
        print('Model : parabolic         --- y = p0 + p1*x + p2*x^2')  # Notifies the user of the functional form, implying the parameter definitions of the fit
        for i in range(len(self.fit_params)):
            print('Enter p{} : '.format(i))
            self.fit_params[i] = float(input())
            
            
        print('Enter lower quantile fit parameters  --- y_l = p0_l + p1_l*x + p2_l*x^2')
        for i in range(len(self.low_edge_params)):
            print('Enter p{}_l : '.format(i))
            self.low_edge_params[i] = float(input())
            
        print('Enter upper quantile fit parameters  --- y_u = p0_u + p1_u*x + p2_u*x^2')
        for i in range(len(self.upp_edge_params)):
            print('Enter p{}_u : '.format(i))
            self.upp_edge_params[i] = float(input())
            
                


        self.Elow         = float(input('Enter Elow : '))
        self.Eupp         = float(input('Enter Eupp : '))
        self.conc_std_min = float(input('Enter conc_std_min : '))
        self.conc_std_max = float(input('Enter conc_std_max : '))

        self.smoothing    = str(input('Enter smoothing procedure abbreviation : '))
        self.baseline     = str(input('Enter baseline procedure abbreviation : '))
        self.calibration  = str(input('Enter calibration procedure abbreviation : '))
        
                
        self.imin_std = self.predict(self.conc_std_min)
        self.imax_std = self.predict(self.conc_std_max)
        self.imin_est = self.upper_pred_edge(self.conc_std_min)
        self.imax_est = self.lower_pred_edge(self.conc_std_max)   

        self.conc_est_min = least_squares(self.conc_est_min_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]
        self.conc_est_max = least_squares(self.conc_est_max_loss, bounds = (self.conc_std_min, self.conc_std_max), x0 = (self.conc_std_min+self.conc_std_max)/2).x[0]

        
       
        return
        
    # This function IS the standard curve. It takes a concentration argument, x,  and maps it to the corresponding most likely current value, y
    def predict(self, x):
        '''
        Function : Parabola

        Purpose  : Apply a parabolic function to the input argument, x, where parabola(x) = p0 + p1*x + p2*x^2

        Input: 
            - x (float/array) : an array of floats to be used as an argument for the parabolic model

        Output:
            - y (float/array) : The mapping of the argument, x, under the parabolic model
        '''
    
        # Terms:
        t0 = self.fit_params[0]
        t1 = self.fit_params[1]*x
        t2 = self.fit_params[2]*x**2.

        # sum of terms:
        y = t0 + t1 + t2

        return y
    
    
    # This function is the error propagation formula or the parabolic standard curve It requires the covariance of the fit parameters and will map a cocnentration, x, to the variance of the current at that concentration:
    
    # The next two functions compute the prediction band edges about the best fit line, which is defined by the predict function 
    # (user chooses confidence level via alpha parameter)
    def upper_pred_edge(self, x):    
        t2 = self.upp_edge_params[2]*x**2.
        t1 = self.upp_edge_params[1]*x
        t0 = self.upp_edge_params[0]
        y  =  t0 + t1 + t2
        return y
    
    def lower_pred_edge(self, x):   
        t0 = self.low_edge_params[0]
        t1 = self.low_edge_params[1]*x
        t2 = self.low_edge_params[2]*x**2.
        
        y = t0 + t1 + t2
        return y
    
    
        
    def conc_est_min_loss(self, x):
        return self.predict(x) - self.imin_est
    def conc_est_max_loss(self, x):
        return self.predict(x) - self.imax_est
    