import numpy as np
class Styler:
    def __init__(self, styled_data_frame, style):
        self.styled_data_frame = styled_data_frame
        self.data = styled_data_frame.data
        self.columns = styled_data_frame.columns
        self.index = styled_data_frame.index
        self.shape = styled_data_frame.data.shape
    def __getitem__(self, key):
        return self.styled_data_frame.__getitem__(key)
    def __getattr__(self, attr):
        return getattr(self.styled_data_frame, attr)
    def head(self, n=5):
        return self.styled_data_frame.data.head(n).style.use(style)
    def __repr__(self):
        return self.styled_data_frame.__repr__()
    def __str__(self):
        return self.styled_data_frame.__str__()
    def to_html(self, *args, **kwargs):
        return self.styled_data_frame.to_html(*args, **kwargs)
    def to_excel(self, *args, **kwargs):
        return self.styled_data_frame.to_excel(*args, **kwargs)
    def to_latex(self, *args, **kwargs):
        return self.styled_data_frame.to_latex(*args, **kwargs)
    def to_csv(self, *args, **kwargs):
        return self.styled_data_frame.to_csv(*args, **kwargs)
    def to_json(self, *args, **kwargs):
        return self.styled_data_frame.to_json(*args, **kwargs)
    def to_markdown(self, *args, **kwargs):
        return self.styled_data_frame.to_markdown(*args, **kwargs)
    
    # define a method for when a method or attribute is called but not available to
    # return styled_data_frame.data.{atttribute} or styled_data_frame.data.{method}
    def __getattr__(self, attr):
        if attr in dir(self.styled_data_frame):
            return getattr(self.styled_data_frame, attr)
        elif attr in dir(self.styled_data_frame.data):
            return getattr(self.styled_data_frame.data, attr)
        else:
            raise AttributeError(f'No attribute or method named {attr} in {self.__class__.__name__}')


def get_naive_diff(df1, df2):
    '''
    write a function to highlight the differences between two dataframes (df1 and df2)
    goes throug each row of the two dataframes, compares them and if any of the values are different, highlight the different value
    if there are additional rows, highlight the entire row
    '''
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)
    df = df1.copy()
    for i in range(max(df1.shape[0], df2.shape[0])):
        for j in range(max(df1.shape[1], df2.shape[1])):
            if i < df1.shape[0] and i < df2.shape[0] and j < df1.shape[1] and j < df2.shape[1]:
                if df1.iloc[i,j] != df2.iloc[i,j]:
                    df.iloc[i,j] = f'{df1.iloc[i,j]} -> {df2.iloc[i,j]}'
            else:
                if i < df1.shape[0] and j < df1.shape[1]:
                    df.iloc[i,j] = f'{df1.iloc[i,j]} -> (missing in df2)'
                elif i < df2.shape[0] and j < df2.shape[1]:
                    df.iloc[i,j] = f'(missing in df1) -> {df2.iloc[i,j]}'
                else:
                    df.iloc[i,j] = np.nan
    return df


def color_fill(val):
    styling = ''
    if isinstance(val, str):
        if "->" in val:
            styling = 'background-color: red; color:black'
    return styling 


MLEN = 50

def get_df_flags(df, column):
    df[f"{column}"] = np.where(df['_merge'] == 'both', 
                                           np.where(df[column + '_df1'] != df[column + '_df2'], 
                                                    True, False), True)
    return df

def get_df_diff(df, column):
    is_equal = df[column + '_df1'] != df[column + '_df2']
    is_long = df[column + '_df1'].str.len() > MLEN
    lng_df = df[column + '_df1'] + " -> " + df[column + '_df2']
    shortened_df = np.where(
        is_long, 
        df[column + '_df1'].str[:MLEN] + '...' + " -> " + df[column + '_df2'].str[:MLEN] + '...', 
        df[column + '_df1'])
    df[f"{column}"] = np.where(is_long, 
                                np.where(is_equal, 
                                        shortened_df, df[column+"_df1"]), lng_df)
    return df


def get_merge_diff(df1, df2, mer_column, mode='flags'):
    columns = df1.columns
    df = df1.merge(df2, on=mer_column, how='outer', indicator=True, suffixes=('_df1', '_df2'))
    for column in columns:
        if column not in [mer_column, '_merge']:
            
            if mode == 'flags':
                df = get_df_flags(df, column)
            elif mode == 'flags_only':
                df = get_df_flags(df, column)
                df = df[df[f"{column}"] == True]
                
            elif mode == 'diff':
                df = get_df_diff(df, column)
            elif mode == 'diff_only':
                df = get_df_diff(df, column)
                df = df[df[f"{column}"] != df[column+"_df1"]]
    df = df.replace({'_merge': {'left_only': '(missing in df2)', 'right_only': '(missing in df1)'}})
    df = df.drop(columns=[col for col in df.columns if col.endswith('_df1') or col.endswith('_df2')], axis=1)
    return df


def highlight_dff(df1, df2, mer_column=False, mode='flags', color='yellow'):
    if not mer_column: ddf = get_naive_diff(df1, df2)
    else: ddf = get_merge_diff(df1, df2, mer_column, mode=mode)
    ddf = ddf.style.applymap(color_fill)
    style = ddf.export()
    sdf = Styler(ddf, style)
    return sdf

highlight_dff(df1, df2, mer_column='POnr',mode='diff_only')


'''
#             elif mode == 'flags_long':
#                 is_true = df[column + '_df1'] != df[column + '_df2']
#                 if_false = df[column + '_df1'].str[:MLEN*2]
#                 df[f"{column}"] = np.where(df['_merge'] == 'both', 
#                                            np.where(is_true, 
#                                                     True, False), True)

'''