import sys
sys.path.append('../dashboard')

try:
    import bdconfig as bd
except:
    print("Arquivo bdconfig.py não encontrado")
try:
    import graficos
except: 
    print("Arquivo graficos.py não encontado")

if __name__ == "__main__":    
    
    bd.bd_clima()
        
