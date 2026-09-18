import pandas as pd
df = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
print(df.to_string(index=False, header=False))
