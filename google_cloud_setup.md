# Configuração do Google Cloud e BigQuery para Análise de Dados

Este guia detalha os passos necessários para configurar um projeto no Google Cloud Platform (GCP), ativar o serviço BigQuery e gerar as credenciais de autenticação para uso em aplicações Python.

## 1. Criar um Projeto no Google Cloud Platform (GCP)

1.  Acesse o [Console do Google Cloud](https://console.cloud.google.com/).
2.  Se você já tem uma conta Google, faça login. Caso contrário, crie uma.
3.  No topo da página, clique no seletor de projetos (geralmente exibe o nome do projeto atual ou 'My First Project').
4.  Na janela que se abre, clique em 'Novo Projeto'.
5.  Insira um nome para o seu projeto (ex: `analise-ecommerce-bigquery`).
6.  (Opcional) Selecione uma organização e um local.
7.  Clique em 'Criar'.

## 2. Ativar a API do BigQuery

1.  Com o projeto recém-criado selecionado, navegue até o 'Menu de Navegação' (três linhas horizontais no canto superior esquerdo).
2.  Vá para 'APIs e Serviços' > 'Biblioteca de APIs'.
3.  Na barra de pesquisa, digite 'BigQuery API' e pressione Enter.
4.  Clique em 'BigQuery API' nos resultados da pesquisa.
5.  Clique no botão 'Ativar'. Aguarde alguns segundos para que a API seja ativada.

## 3. Gerar Credenciais para Uso em Python (Conta de Serviço)

Para que seu código Python possa acessar o BigQuery de forma segura, você precisará de uma Conta de Serviço e uma chave JSON.

1.  No 'Menu de Navegação', vá para 'APIs e Serviços' > 'Credenciais'.
2.  Clique em 'Criar Credenciais' > 'Conta de Serviço'.
3.  **Detalhes da conta de serviço:**
    -   **Nome da conta de serviço:** `bigquery-analyst` (ou outro nome descritivo).
    -   **ID da conta de serviço:** Será preenchido automaticamente.
    -   **Descrição da conta de serviço:** `Conta de serviço para acesso ao BigQuery para análise de e-commerce`.
4.  Clique em 'Criar e Continuar'.
5.  **Conceder a esta conta de serviço acesso ao projeto:**
    -   No campo 'Selecionar um papel', pesquise por 'BigQuery' e selecione os seguintes papéis:
        -   `BigQuery Data Viewer` (para visualizar dados)
        -   `BigQuery Job User` (para executar consultas)
    -   Para este projeto, esses papéis são suficientes. Em projetos maiores, você pode precisar de `BigQuery User` ou `BigQuery Admin`.
6.  Clique em 'Continuar'.
7.  **Conceder aos usuários acesso a esta conta de serviço:** (Opcional, para outros usuários acessarem esta conta de serviço)
    -   Você pode pular esta etapa por enquanto.
8.  Clique em 'Concluído'.

Agora você tem uma conta de serviço criada. O próximo passo é gerar a chave JSON.

9.  Na página 'Credenciais', localize a conta de serviço que você acabou de criar (`bigquery-analyst`).
10. Clique nos três pontos verticais (ações) ao lado do nome da conta de serviço e selecione 'Gerenciar chaves'.
11. Na página 'Chaves', clique em 'Adicionar Chave' > 'Criar nova chave'.
12. Selecione 'JSON' como o tipo de chave e clique em 'Criar'.
13. Um arquivo JSON será baixado automaticamente para o seu computador. **Este arquivo contém suas credenciais e deve ser mantido em segurança.** Renomeie-o para algo como `bigquery-credentials.json`.

## 4. Configurar Variável de Ambiente em Python

Para usar as credenciais em seu código Python, você pode definir a variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` apontando para o caminho do arquivo JSON baixado.

**Exemplo (Linux/macOS):**

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/caminho/para/seu/arquivo/bigquery-credentials.json"
```

**Exemplo (Windows - Prompt de Comando):**

```cmd
set GOOGLE_APPLICATION_CREDENTIALS="C:\caminho\para\seu\arquivo\bigquery-credentials.json"
```

**Exemplo (Windows - PowerShell):**

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\caminho\para\seu\arquivo\bigquery-credentials.json"
```

Alternativamente, você pode passar o caminho do arquivo JSON diretamente para o cliente BigQuery em seu código Python, mas a variável de ambiente é a forma recomendada para evitar expor o caminho no código.

Com essas configurações, seu ambiente estará pronto para interagir com o Google BigQuery usando Python.

