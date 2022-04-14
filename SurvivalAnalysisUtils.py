from lifelines import KaplanMeierFitter

class ReusableUtils():
    
    
    """
    Module of reusable function and utilities that 
    can be reused across notebooks.
    
    """
    
    def __init__(self):
        pass
    
    def PlotKaplanMeierEstimatesForCategoricalVariables(data = None, categorical_columns=[]):
    
        '''
        Purpose: 
            Plots the Kaplan Meier Estimates For Categorical Variables in the data.

            **NOTE: The Kaplan-Meier estimator is used to estimate the survival function. 
            The visual representation of this function is usually called the Kaplan-Meier 
            curve, and it shows what the probability of an event (for example, survival) 
            is at a certain time interval. If the sample size is large enough, the curve 
            should approach the true survival function for the population under 
            investigation.

        Parameters:
            1. data: the dataset.
            2. categorical_columns: all the categorical data features as a list.

        Return Value: 
            NONE.

        Reference:       https://lifelines.readthedocs.io/en/latest/fitters/univariate/KaplanMeierFitter.html#lifelines.fitters.kaplan_meier_fitter.KaplanMeierFitter
        '''

        categoricalData = data.loc(axis=1)[categorical_columns]

        fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(18,10))
        plt.tight_layout(pad=5.0)

        def km_fits(data, curr_Feature = None):

            '''
            Purpose: 
                Generates the Kaplan Meier fits for fitting the Kaplan-Meier 
                estimate for the survival function.

            Parameters:
                1. data: the dataset.
                2. curr_Feature: the current feature under consideration.

            Return Value: 
                kmfits: the Kaplan-Meier estimates.
            '''

            range_hue = np.unique(data[curr_Feature])

            X = [data[data[curr_Feature]==x]['time'] for x in range_hue]
            Y = [data[data[curr_Feature]==y]['DEATH_EVENT'] for y in range_hue]
            fit_label = [str(curr_Feature + ': ' + str(range_hue_i)) for range_hue_i in range_hue]

            kmfits = [KaplanMeierFitter().fit(durations = x_i, 
                                              event_observed = y_i, 
                                              label = fit_label[i]) for i,(x_i, y_i) in enumerate(zip(X,Y))]

            return kmfits

        for idx, feature in enumerate(categorical_columns):
            cat_fits = km_fits(data = data, 
                               curr_Feature = feature)

            [x.plot(title=feature, ylabel="Survival Probability", xlabel="Days",
                    ylim=(0,1.1), xlim=(0,290),
                    ci_alpha=0.1, ax=ax.flatten()[idx]) for x in cat_fits]

        ax.flatten()[-1].set_visible(False)
        fig.suptitle("Kaplan Meier Estimates for Categorical Variables ", fontsize=16.0)
        plt.show()
        
        return None
    
    def PlotKaplanMeierEstimatesForContinuousVariables(data = None, contituous_columns=[]):
    
        '''
        Purpose: 
            Plots the Kaplan Meier Estimates For Continuous Variables in the data.

            **NOTE: The Kaplan-Meier estimator is used to estimate the survival function. 
            The visual representation of this function is usually called the Kaplan-Meier 
            curve, and it shows what the probability of an event (for example, survival) 
            is at a certain time interval. If the sample size is large enough, the curve 
            should approach the true survival function for the population under 
            investigation.

        Parameters:
            1. data: the dataset.
            2. contituous_columns: all the continuous data features as a list.

        Return Value: 
            NONE.

        Reference:
            https://lifelines.readthedocs.io/en/latest/fitters/univariate/KaplanMeierFitter.html#lifelines.fitters.kaplan_meier_fitter.KaplanMeierFitter
        '''

        continuousData = data.loc(axis=1)[contituous_columns]

        fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(18,15))
        plt.tight_layout(pad=5.0)

        def km_fits(data, curr_Feature = None, split_points = None):

            '''
            Purpose: 
                Generates the Kaplan Meier fits for fitting the Kaplan-Meier 
                estimate for the survival function.

            Parameters:
                1. data: the dataset.
                2. curr_Feature: the current feature under consideration.
                3. split_points: the data split points to cut the data.

            Return Value: 
                kmfits: the Kaplan-Meier estimates.
            '''

            bins = pd.cut(x=data[curr_Feature],bins=split_points)
            range_hue = np.unique(bins)
            hue_group = str(curr_Feature) + "_group"
            data[hue_group] = pd.cut(x=data[curr_Feature], bins=split_points)

            X = [data[data[hue_group] == bin_range]['time'] for bin_range in range_hue]      
            Y = [data[data[hue_group] == bin_range]['DEATH_EVENT'] for bin_range in range_hue]        
            fit_label = [str(str(range_hue_i).replace(',',' -').replace(']',')')) for range_hue_i in range_hue]        
            data.drop(hue_group, axis=1, inplace=True)

            kmfits = [KaplanMeierFitter().fit(durations = x_i, 
                                              event_observed = y_i, 
                                              label=fit_label[i]) for i,(x_i, y_i) in enumerate(zip(X,Y))]

            return kmfits

        data_split_points = [[30.0,60.0,80.0,100.0],3,[0,30.0,45.0,100.0],3,3,3,3]

        for idx, feature in enumerate(contituous_columns):

            cont_fits = km_fits(data = data, 
                                curr_Feature = feature,
                                split_points = data_split_points[idx])

            [x.plot(title=feature, ylabel="Survival Probability", xlabel="Days",
                    ylim=(0,1.1), xlim=(0,290), ci_alpha=0.1, 
                    ax=ax.flatten()[idx]) for x in cont_fits]

        ax.flatten()[-1].set_visible(False)
        ax.flatten()[-2].set_visible(False)

        fig.suptitle("Kaplan Meier Estimates for Continuous Variables ", fontsize=16.0, y=1.0)

        plt.show()