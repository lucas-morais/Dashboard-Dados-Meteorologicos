## DASHBOARD de DADOS METEREOLÓGICOS - PYTHON


### __Fonte de dados__
- INMET  

  
### __Tecnologias utilizadas__
- python
	- dash
	- plotly
	- pandas
- SQLite
- CSS

### __Estrutura de diretórios__
	- dados
		|--Dados em csv e banco de dados
	- notebooks
		|--Notebooks com os passos para implementação das funções de apoio
	- dashboard
		|--Arquivos principal do dashboard
		|--Arquivos de apoio
	- setup.py
		|--Arquivo para configurações
	- requirements.txt 
		|--Arquivo com dependêcias

### __Executando localmente__

 #### Verificando dependências  
	pip install requirements.txt

#### Criando banco de dados e testando funções  
	python setup.py

#### Executando dashboard
	python dashboard/dashborad.py

#### Acessando dashboard  
	Endereço:localhost:8050

