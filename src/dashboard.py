from bdconfig import carrega_csv

path = '../dados/JoaoPessoa_clima.csv'

df = carrega_csv(path)
print(df.head())