# 🧬 FunExpression 🧬

### FunExpression: Um pipeline para análise de expressão diferencial de fungos utilizando dados brutos de Bulk RNA-Seq.

Essa é uma ferramenta para realizar análise de expressão diferencial de genes utilizando dados brutos de RNA-Seq Bulk.
No seu backend existe um endpoint que é utilizado para calcular a expressão diferencial.


## Como Executar
Esta ferramenta está utilizando Docker, para rodar na sua máquina é necessário possuir o Docker[https://docs.docker.com/engine/install/] instalado e seguir os passos abaixo:

- Realize o clone do projeto 
- Copie o .env.example para o arquivo .env e preencha com as variáveis de ambiente
- Na raiz do projeto execute o comando `docker-compose  up --build`


## Acessando a interface
Você pode acessar a interface com o usuário a partir da url: `localhost`

## Para acessar a Api copie o cURL abaixo no seu programa de client que pode ser insomnia ou o postman, por exemplo.

```
curl --request POST \
  --url http://localhost/expression/calculate/ \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/9.2.0' \
  --data '{
	"name": "Adeonita",
	"email": "adeonita.sousa@gmail.com",
	"control_organism": {
		 "srr_acession_number_1": "SRR10042980",
		 "srr_acession_number_2": "SRR10042981",
		 "srr_acession_number_3": "SRR10042982"
	},
	"experiment_organism": {
		 "srr_acession_number_1": "SRR10042986",
		 "srr_acession_number_2": "SRR10042987",
		 "srr_acession_number_3": "SRR10042988"
	},
	"reference_genome_acession_number": "GCA_000346795.1",
	"p_adj": 0.05,
  "log_2_fold_change_threshold": 2
}'
```