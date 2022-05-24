## DASHBOARD de DADOS METEOROLÓGICOS - PYTHON


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
	- requirements.txt 
		|--Arquivo com dependêcias

### __Executando localmente__

 #### Verificando dependências  
	pip install -r requirements.txt

#### Criando banco de dados e testando funções  
	python setup.py

#### Executando dashboard
	Mudar para diretório dashboard
	python dashborad.py

#### Acessando dashboard  
	Endereço:localhost:8050

