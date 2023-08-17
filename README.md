# Bot Quant - Estratégia de Pairs Trading com Análise de Cointegração

![Bot Quant](https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDF8fHRyYWRpbmd8ZW58MHx8fHwxNjkwMzA3ODU4fDA&ixlib=rb-4.0.3&q=80&w=200)

Este projeto visa desenvolver um bot quantitativo para automatizar estratégias de negociação nos mercados financeiros, com foco na Estratégia de Pairs Trading. O bot utiliza análise de cointegração para identificar pares de ativos que apresentam comportamento co-movimentado e, a partir desses pares, calcula e monitora as razões de preços (ratios) para explorar oportunidades de negociação quando essas razões se desviam da média histórica.

## Funcionalidades

-   [x] Conexão com APIs de dados de mercado.
-   [x] Identificação de pares cointegrados de ativos.
-   [x] Cálculo das razões de preços (ratios) para cada par cointegrado.
-   [ ] Seleção de pares com distribuição mais normal das razões.
-   [ ] Avaliação da reversão à média das razões.
-   [ ] Execução automatizada de operações de compra e venda.
-   [ ] Gerenciamento de risco e controle de posição.
-   [ ] Monitoramento e análise contínua de resultados.

## Instalação

Certifique-se de ter o Python instalado no sistema. Para configurar o ambiente de desenvolvimento, siga os passos abaixo:

1. Clone este repositório para o seu ambiente local:

```bash
git clone https://github.com/Lucasch1/Itau-Quantamental.git
```

2. Acesse o diretório do projeto:

```bash
cd Itau-Quantamental
```

3. Crie um ambiente virtual (recomendado) e ative-o:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate.bat
```

Em sistemas baseados em Unix (Linux/Mac):

```bash
source venv/bin/activate
```

4. Instale as dependências do projeto a partir do arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Utilização

1. **Coleta de Dados:**

    - Obtenha dados históricos de preços de ativos financeiros utilizando uma API ou fontes de dados como o Yahoo Finance.

2. **Pré-processamento dos Dados:**

    - Limpe e normalize os dados para prepará-los para análise.

3. **Identificação de Pares Cointegrados:**

    - Utilize técnicas de cointegração para identificar pares de ativos cointegrados.

4. **Cálculo do Ratio:**

    - Calcule o ratio para cada par cointegrado.

5. **Seleção de Pares e Verificação de Normalidade:**

    - Escolha pares cointegrados com razões que apresentam uma distribuição mais próxima da normal.

6. **Avaliação de Reversão à Média:**

    - Analise a reversão à média das razões mais normalmente distribuidas.

7. **Execução de Operações:**

    - Com base nos pares restantes apos o filtro, execute operações de compra e venda dos ativos com razões fora da média.

8. **Gerenciamento de Risco:**

    - Implemente um sistema de gerenciamento de risco para controlar a alocação de capital em cada operação.

9. **Monitoramento Contínuo:**

    - Monitore o desempenho da estratégia em tempo real e faça ajustes conforme necessário.

## Considerações Finais

A estratégia de Pairs Trading com Análise de Cointegração é complexa e requer conhecimentos em finanças quantitativas, análise de dados e programação. Antes de aplicá-la em um ambiente de negociação real, conduza uma extensa pesquisa, teste a estratégia em dados históricos e implemente um gerenciamento rigoroso de riscos.

Consultar especialistas em finanças quantitativas e realizar testes exaustivos é fundamental para aumentar a probabilidade de sucesso. Opere com cautela e responsabilidade, pois todas as estratégias de negociação envolvem riscos e podem levar a perdas significativas.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, propor melhorias ou enviar pull requests para o projeto.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

Criado por [Lucas Hashimoto](https://www.linkedin.com/in/lucas-hashimoto/) - [Aron Burgos](https://www.linkedin.com/in/aron-miranda-burgos-57a99a169/) - [Isabela Sigaki](https://www.linkedin.com/in/isabela-sigaki/) - [Fernanda Diniz](https://www.linkedin.com/in/fernandadinizmarinho/) - 2023.
