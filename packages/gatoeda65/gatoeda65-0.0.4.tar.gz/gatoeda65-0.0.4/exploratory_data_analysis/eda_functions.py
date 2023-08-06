from scipy import stats
from scipy.stats import skew
from scipy.stats import kurtosis
import statsmodels.api as sm
from sklearn.utils import resample

import math
import pandas as pd
import numpy as np

## Graphs
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

################################################################################
##############  READABLE NUMBER ################################################
    
def readableNumbers(x):
    """
    Takes a large number and formats it into K,M to make it more readable
    Args:
        x: a number.
    Returns:
        A string easy to read information.
    Usage:
        # Use the readable_numbers() function to create a new column 
        df['readable'] = df['big_num'].apply(readable_numbers)

    """
    if x >= 1e6:
        s = '{:1.1f}M'.format(x*1e-6)
    else:
        s = '{:1.0f}K'.format(x*1e-3)
    return s

################################################################################
############## FEATURE OBSERVE  ################################################

def feature_observe(dataframe: pd.DataFrame):

    """
    Recieve a dataframe and check for null elements, 
    it returns a dictionary with keys: message, feature
    over 5% and features between 0 and 5%, and its values.
    
    Args:
        df(pd.DataFrame): a pandas DataFrame
    """
    # Running validation on the argument recieved
    assert type(dataframe) == pd.DataFrame, f'{dataframe}, is not a pandas df.'

    df = dataframe.copy()
    feat_look = []
    feat_kill = []
    pct_5 = dataframe.isnull().mean() >= 0.05
    
    for i in df.columns:
        if pct_5[i]:
            feat_kill.append(i)
        elif pct_5[i] < 0.05:
            feat_look.append(i)
    lenghts = [len(feat_look), len(feat_kill)]
    elementos = [feat_look, feat_kill]
    results = {
        "message" : f"{lenghts[0]} features are missing less than 5%. And \
{lenghts[1]} features are missing more than 5%.",
        "features over 5%" : elementos[1], 
        "features less 5%" : elementos[0]
    }
    return results

################################################################################
######################### MISSING INFORMATION  #################################

def miss_df(dataframe: pd.DataFrame):

    """
    Take a pandas df as argument, returns another one
    with  basic information about missing data
    Args:
        df(pd.DataFrame): a pdDataFrame.
    """

    # Running validation on the argument recieved
    assert type(dataframe) == pd.DataFrame, f'{dataframe}, is not a pandas df.'
    df = dataframe.copy()
    total_missing = df.isnull().sum().sort_values(ascending=False)
    percent_missing = (df.isnull().sum() / df.isnull().count()) * 100
    missing_data = pd.concat([total_missing, percent_missing], axis=1, keys=['Total', 'Percent'])
    return missing_data.head(len(df.columns))

################################################################################
#################   INVALID STRINGS   ##########################################

def get_invalid_values(dataframe: pd.DataFrame):
    """
    Take a pandas df as argument, looks for the items 
    in an invalid list. returns a pd df with
    the columns: column, nulls, invalids, 
    and the unique values.
    
    Args:
        df(pd.DataFrame): a pdDataFrame.
    """
    # Running validation on the argument recieved
    assert type(dataframe) == pd.DataFrame, f'{dataframe}, is not a pandas df.'
    df = dataframe
    
    invalid_list =\
    [np.nan, None, [], {}, 'NaN', 'Null','NULL'\
     ,'None','NA','?','-', '--','.','', ' ', '   ']
    
    invalids = []
    uniques = []
    result = pd.DataFrame({
        'nulls': df.isnull().sum(),
    })
    for c in df.columns:
        invalids.append(df[c].isin(invalid_list).sum())
        uniques.append(df[c].unique())
    result['invalids'] = invalids
    result['unique_item'] = uniques
    return(result.head(len(df.columns)))
 
################################################################################
###############  SIFT DATA BY THE PD.TYPES #####################################
    
def sift_data_type(dataframe: pd.DataFrame):

    """
    Takes a pandas df as argument, groups the columns by data type
    and returns a dictionary with the results.

    Args:
      df(pd.DataFrame): a pdDataFrame.
    """

    # Running validation on the argument recieved
    assert type(dataframe) == pd.DataFrame, f'{dataframe}, is not a pandas df.'

    num_features = dataframe.copy().select_dtypes(['int64', 'float64']).columns
    cat_features = dataframe.copy().select_dtypes(['object']).columns

    lenghts = [len(num_features), len(cat_features)]
    elementos = [num_features, cat_features]
    results = {
        "message": f"{lenghts[0]} features are numerical and {lenghts[1]} \
features are categorical.",
        "nums": elementos[0], 
        "objs": elementos[1]
    }

    return results

################################################################################
######################### transformtonan #######################################

def transform_to_nan(elemento, dataframe, column_name):
    """
    arguments
    returns new df.
    """
    df = dataframe.copy()
    df[column_name] = df[column_name].astype(str).apply(str.strip).replace(elemento, np.nan)
    df[column_name] = df[column_name].astype(str).apply(str.strip).replace('nan', np.nan)
     
    return df


################################################################################
#######################   FILL IN MISSINGA VALUES      #########################

def filler_of_the_nans(technique, df, list_to_fill):
    """
    Fill in nans of a fill_list from a pandas df,
    the fill list should be defined by the technique to use. 
    The options are mean, median, mode or interpolation.
    Returns a copy of the original dataframe, but filled.
    It uses : mean(), median(), interpolate(), mode() and 'None'

    Args:
        technique (list): a technique to use, from the list
        df(pd.DataFrame): a pdDataFrame.
        fill_list (pd.Series): pd.Series or list of Series with
        missing values. 
        
    """
    #Running validation on the argument recieved
    tecnicas = ('mean', 'median', 'interpolate', 'mode', 'None')
    assert type(df) == pd.DataFrame, f'{df} is not a pandas df.'
    assert technique in tecnicas, f'{technique} not in options:\
        [mean|median|interpolate|mode|None]'
    technique = technique
    # Deffining and populating a dataframe
    dff = pd.DataFrame()
    dff = df.copy()

    if technique == 'None':
        for i in list_to_fill:
            dff.loc[:, i] =  dff.loc[:, i].fillna('None')
        return dff
    
    elif technique == 'mode':
        for i in list_to_fill:
            dff.loc[:, i] =  dff.loc[:, i].fillna\
            (getattr(dff.loc[:, i], technique)()[0])
        return dff
   
    else: 
        for i in list_to_fill:
            dff.loc[:, i] = dff.loc[:, i].fillna\
            (getattr(dff.loc[:, i], technique)())

    return dff

################################################################################
######################  HISTOGRAM OF DESIRED  FEATURES #########################

def histogramas(df, features):
    """
    Show histograma.
    Take a pandas dataframe and a list
    of columns

    Args:
        df: a pdDataFrame.
        features: pd.Series or list of Series with
        desire values. 
    """
    plt.figure(figsize = (10, 35))
    for i, feature in enumerate(features):
        ax = plt.subplot(10, 3, i + 1)
        ax.hist(df[feature], bins=25, color='Orange', edgecolor='black',\
               label=feature, alpha=0.2)
        ax.set_title(feature + ' histograma')
        plt.xticks(rotation=45)
        plt.tight_layout(pad=5.0)
        

################################################################################
####################  KURTOSIS AND SKEWNESS ####################################

def kurt_skew(df, features):
    """
    Kurtosis and Skewness report.
    Take a pandas dataframe and a list
    of columns
    Args:
        df: a pdDataFrame.
        features: pd.Series or list of Series with
            desire values. 
    Returns a package with 3 objects to unpack.
    (info, list of columns, 
    """
    kurt = stats.describe(df[features]).kurtosis
    skew = stats.describe(df[features]).skewness
    # if the column is gretter than 0.5 is skew
    info = pd.DataFrame({'column': df[features].columns, 'kurtosis': abs(kurt), \
                         'skewness': abs(skew)})
    info['need_transformation'] = info['kurtosis'].\
    apply(lambda x: True if x >= 0.5 else False)
    
    # numerical columns that are skew and need attention.
    skewColumns = info.query('need_transformation == True')['column'].values
    
    return(histogramas(df, skewColumns), skewColumns, info)
    

################################################################################
#######################  ESTADISTICAS  #########################################

def estadisticas(df: pd.core.frame.DataFrame, col: pd.core.series.Series ):
    
    """
    Recieve a dataframe and a column.
    returns a dataframe with num of observations, 
    min, max, mean, variance, skewness, kurtosis.
    
    Args:
        df(pd.DataFrame): a pandas DataFrame
        column: a pandas series
    """
    nobs, minMax, mean, variance, skewness, kurtosis = stats.describe(df[col])
    descriptive_stats = {}
    descriptive_stats['observations'] = nobs
    descriptive_stats['minimun'] = minMax[0]
    descriptive_stats['maximun'] = minMax[1]
    descriptive_stats['mean'] = mean
    descriptive_stats['variance'] = variance
    descriptive_stats['skewness'] = skewness
    descriptive_stats['kurtosis'] = kurtosis
    return pd.DataFrame.from_dict(descriptive_stats, orient='index', \
                                  columns=[col])

################################################################################
####################### Empirical Rule  ########################################

def empirical(df, col):
    """
    Recieve a dataframe and a column.
    Return a data frame with information related
    to the empirical rule compared to a column
    distribution.
    
    Args:
        df(pd.DataFrame): a pandas DataFrame
        column: a pandas series
    """
    mean = df[col].mean()
    SD   = df[col].std()
    
    lowerLim = mean - 1 * SD
    upperLim = mean + 1 * SD

    pct1 = round(((df[col] >= lowerLim) & (df[col] <= upperLim)).mean(), 2)

    ## 2SD from the mean

    lowerLim2 = mean - 2 * SD
    upperLim2 = mean + 2 * SD

    pct2 = round(((df[col] >= lowerLim2) & (df[col] <= upperLim2)).mean(), 2)

    ## 3SD from the mean
    
    lowerLim3 = mean - 3 * SD
    upperLim3 = mean + 3 * SD

    pct3 = round(((df[col] >= lowerLim3) & (df[col] <= upperLim3)).mean(), 2)
    
    lims = [pct1, pct2, pct3]
    suggestion = [0.68, 0.95, 0.997]
    
    rules = [[ pct1, suggestion[0], abs(pct1 - suggestion[0]) ], 
             [ pct2, suggestion[1], abs(pct2 - suggestion[1]) ], 
             [ pct3, suggestion[2], abs(pct3 - suggestion[2]) ]]
    index = ["Frac of the values within +/- 1 SD from the mean", 
             "Frac of the values within +/- 2 SD from the mean", 
             "Frac of the values within +/- 3 SD from the mean"]
    df = pd.DataFrame(rules, columns = [col, 'empirical_rule_suggest', \
                                        'difference'], index = index)
    
    return(df)

################################################################################
######################  Distribution Report ####################################

def distribution(df, col):
    
    """
    Recieve a dataframe and a column.
    Return a data frame with information related
    to the empirical rule compared to a column
    distribution, an hisogram and a qq plot.
    
    Args:
        df(pd.DataFrame): a pandas DataFrame
        column: a pandas series
    """

    
    mean = df[col].mean()
    SD   = df[col].std()
    
    lowerLim = mean - 1 * SD
    upperLim = mean + 1 * SD

    pct1 = round(((df[col] >= lowerLim) & (df[col] <= upperLim)).mean(), 2)

    ## 2SD from the mean

    lowerLim2 = mean - 2 * SD
    upperLim2 = mean + 2 * SD

    pct2 = round(((df[col] >= lowerLim2) & (df[col] <= upperLim2)).mean(), 2)

    ## 3SD from the mean
    
    lowerLim3 = mean - 3 * SD
    upperLim3 = mean + 3 * SD

    pct3 = round(((df[col] >= lowerLim3) & (df[col] <= upperLim3)).mean(), 2)
    11.7,8.27
    plt.figure(figsize=( 11.7,8.27))
    ax = plt.subplot()
    p = sns.histplot(data=df[col], kde=col, hue=None, legend=False)
    plt.legend(title='Values within 1, 2, 3 SD from the mean', loc='upper left',\
               labels=[pct1, pct2, pct3])
    ax.set_title(col)
    
    ax.axvline(x=lowerLim, color='r', linestyle='dotted')
    ax.axvline(x=upperLim, color='r', linestyle='dotted')
    
    ax.axvline(x=lowerLim2, color='b', linestyle='dashed')
    ax.axvline(x=upperLim2, color='b',linestyle='dashed')
    
    ax.axvline(x=lowerLim3, color='g', linestyle='dashdot')
    ax.axvline(x=upperLim3, color='g', linestyle='dashdot')
    ## qqplot from stats
    sm.qqplot(df[col], fit=True, line='45')
    
    plt.show()
    

################################################################################
####################UpSampleMinorityClass#######################################

def upsample_minority_class(data, feature):
    
    '''
    Take a pandas df and one binary feature.
    identify the minority class,
    upsamples the minority in a binary class in a DataFrame 
    to match the size of the majority class.

      Args:
        data: The DataFrame to be upsampled, pandas Data Frame.
        feature: the columns name, string.
        
      Returns:
        A DataFrame with the minority class upsampled.
    '''
    
    ## Identify data points from majority and minority classes
    
    class_1 = data[feature].value_counts().index[0]
    class_2 = data[feature].value_counts().index[1]
    
    majority_class = None
    minority_class = None

    if class_1 > class_2:
        majority_class = class_1
        minority_class = class_2
    else: 
        majority_class = class_2
        minority_class = class_1

    
    data_majority = data[data[feature] == majority_class]
    data_minority = data[data[feature] == minority_class]
    
    n_samples = len(data_majority)
                              
    data_minority_upsampled = resample(
          data_minority,
          replace=True,
          n_samples=n_samples,
          random_state=None)

    data_upsampled = pd.concat([data_majority, \
                                data_minority_upsampled]).reset_index(drop=True)

    return data_upsampled

################################################################################
################################################################################
