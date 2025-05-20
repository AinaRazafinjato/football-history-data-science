def clean_data(df):
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Fill missing values
    df = df.fillna(method='ffill')
    
    return df

def normalize_data(df):
    # Normalize numerical columns
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    df[df.select_dtypes(include=['float64', 'int']).columns] = scaler.fit_transform(df.select_dtypes(include=['float64', 'int']))
    
    return df

def split_data(df, target_column, test_size=0.2, random_state=42):
    from sklearn.model_selection import train_test_split
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    return X_train, X_test, y_train, y_test