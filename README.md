# Olist Prescriptive Analytics Platform

Projeto de Engenharia de Dados e Analytics utilizando dados públicos da Olist.

## Objetivo

Construir uma plataforma analítica com pipeline de dados em camadas, modelagem dimensional, PostgreSQL, Docker, Data Quality, KPIs executivos e recomendações prescritivas.

## Arquitetura

Kaggle Dataset  
→ Bronze CSV  
→ Silver Parquet  
→ Gold Star Schema  
→ PostgreSQL Data Warehouse  
→ Analytics Layer  
→ Power BI

## Tecnologias

- Python
- Pandas
- PostgreSQL
- Docker
- SQLAlchemy
- PyArrow
- Power BI
- VS Code
- WSL Ubuntu

## Estrutura

- `src/ingestion`: inventário dos dados
- `src/transformations`: criação da camada Silver
- `src/warehouse`: criação da camada Gold
- `src/load`: carga no PostgreSQL
- `src/quality`: validação de qualidade
- `src/analytics`: KPIs, insights e recomendações

## Principais resultados

- Receita total: R$ 16.008.872,12
- Ticket médio: R$ 154,10
- Avaliação média: 4,09
- Pedidos atrasados: 6,45%
- Modelo dimensional em Star Schema
- Relatório de qualidade com 0 inconsistências críticas

## Próximos passos

- Construção do dashboard Power BI
- Publicação do relatório online
- Criação de vídeo explicativo do projeto