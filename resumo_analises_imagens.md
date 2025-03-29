# Resumo das Análises das Imagens

## Imagem: 1_baixar_relatorio.png
![1_baixar_relatorio.png](/processed_images/1_baixar_relatorio.png)

### Navegação para a seção de Relatórios
Navegação da página inicial para a seção de "Relatórios" e "Estatísticas".


## Imagem: 2_baixar_relatorio.png
![2_baixar_relatorio.png](/processed_images/2_baixar_relatorio.png)

### Navegação para a última página de estatísticas
Clique na última página de estatísticas (exemplo: página 3) para acessar os dados mais recentes.

## Imagem: 3_baixar_relatorio_executar.png
![3_baixar_relatorio_executar.png](/processed_images/3_baixar_relatorio_executar.png)

### Executar Relatório SAP Ariba
Clique no ícone de play para executar o relatório SAP Ariba.

## Imagem: 4_baixar_relatorio_executar.png
![4_baixar_relatorio_executar.png](/processed_images/4_baixar_relatorio_executar.png)

### Executar Estatísticas
Clique em "Executar agora" para gerar a estatística com as configurações atuais.

## Imagem: 5_salvar_relatorio_pasta_correta.png
![5_salvar_relatorio_pasta_correta.png](/processed_images/5_salvar_relatorio_pasta_correta.png)

### Movendo Arquivo para Pasta Específica

O arquivo está sendo movido da pasta "Downloads" para a pasta "dashboard_csc", localizada em "Documentos" dentro da pasta do usuário "Joel Ferreira Heanna Dos Reis".

## Imagem: 6_deletar_relatorios_sap_relatorio_novo.png
![6_deletar_relatorios_sap_relatorio_novo.png](/processed_images/6_deletar_relatorios_sap_relatorio_novo.png)

### Selecionar e deletar arquivos

*   Os arquivos "relatorio\_novo.xlsx" e "sap.xlsx" estão destacados em vermelho, indicando que devem ser selecionados e excluídos.

## Imagem: 7_abrir_vs_code.png
![7_abrir_vs_code.png](/processed_images/7_abrir_vs_code.png)

### Abertura do VS Code via Terminal

1.  **Comando `pwd`**: Exibe o caminho absoluto do diretório atual.
2.  **Comando `code .`**: Abre o VS Code no diretório exibido pelo comando `pwd`.

## Imagem: 8_executar_script_merge_csc_report.png
![8_executar_script_merge_csc_report.png](/processed_images/8_executar_script_merge_csc_report.png)

### Executando Script Python no VS Code
O arquivo `merge_csc_report.py` está aberto no VS Code. Clique no botão "Run Python File in Terminal" (seta vermelha) para executar o script.


## Imagem: 9_relatorio_final_gerado.png
![9_relatorio_final_gerado.png](/processed_images/9_relatorio_final_gerado.png)

### Arquivo de saída e execução do script
O script Python "merge_csc_report.py" foi executado com sucesso. O arquivo "relatorio_final.xlsx" foi gerado na pasta do projeto.

## Imagem: 11_filtrar_planilha_por_Estado.png
![11_filtrar_planilha_por_Estado.png](/processed_images/11_filtrar_planilha_por_Estado.png)

### Filtrando status "Solucionado" na coluna "Estad"
Filtrar a coluna "Estad" da planilha para exibir apenas os registros com o status "Solucionado".

- Desmarcar todas as opções de status.
- Marcar a opção "Solucionado".
- Clicar em "OK" para aplicar o filtro.


## Imagem: 10_abrir_relatorio_final.png
![10_abrir_relatorio_final.png](/processed_images/10_abrir_relatorio_final.png)

### Abrir Arquivo "relatorio_final"
Abrir arquivo selecionado.

## Imagem: 12_filtrar_planilha_por_Servico.png
![12_filtrar_planilha_por_Servico.png](/processed_images/12_filtrar_planilha_por_Servico.png)

### Filtro da coluna "Serviço" no LibreOffice Calc

*   Na coluna "Serviço", um filtro está sendo aplicado.

*   Os itens marcados indicam os dados que serão exibidos após a aplicação do filtro.
    *   "Dados da Classificação Anterior": SAP - Dúvidas Gerais, SAP - SLP Fornecedores, SAP - Usuários, SAP - Workflow, SI - Tabela RH.
    *   "Dados novos para Classificação": Tecnologia da Informação::SAP Ariba, Tecnologia da Informação::SAP Ariba::Dados: Alteração de Workflow de Aprovação, Tecnologia da Informação::SAP Ariba::Dados: Solicitação de Perfil de Usuário, Tecnologia da Informação::SAP Ariba::P2O: PO.

*   Após selecionar os dados desejados, clica-se em "OK" para aplicar o filtro.

## Imagem: 13_clasificando_planilha_por_Servico.png
![13_clasificando_planilha_por_Servico.png](/processed_images/13_clasificando_planilha_por_Servico.png)

### Filtragem de Dados no LibreOffice Calc

- **Serviço:** Filtrando dados na coluna "Serviço" para mostrar apenas linhas que contêm "Tecnologia da Informação::SAP Ariba::P2O: PO".
- **Título:** Observando a coluna "Título" para identificar chamados com "portal comercial".


## Imagem: 14_exemplo_apos_classificacao.png
![14_exemplo_apos_classificacao.png](/processed_images/14_exemplo_apos_classificacao.png)

### Dados em planilha
Os serviços ERP: ALMOX de linhas 5 e 10, possuem os números de tickets 2025032885003574 e 2025032885002521, respectivamente. O serviço Tecnologia da Informação::SAP Ariba::P2O: PO, na linha 17, possui o ticket 2025032885001361.

## Imagem: 15_apos_classificar_salvar.png
![15_apos_classificar_salvar.png](/processed_images/15_apos_classificar_salvar.png)

### Filtrando dados na coluna "Serviço"
Filtrando os dados da coluna "Serviço" na planilha.

*   Desmarcando a opção "Todos" e selecionando itens específicos para filtrar os dados exibidos na coluna.
*   Clicando em "OK" para aplicar o filtro selecionado.

## Imagem: 16_executar_dasboard_streamlit.png
![16_executar_dasboard_streamlit.png](/processed_images/16_executar_dasboard_streamlit.png)

### Verificando o diretório atual e executando o script Streamlit
- **`pwd`**: Mostra o diretório atual, que é `/c/Users/jfreis/Documents/dashboard_csc`.
- **`streamlit run analitics_incidents.py`**: Executa o script Python `analitics_incidents.py` usando o Streamlit.


## Imagem: 17_executando_dashboard.png
![17_executando_dashboard.png](/processed_images/17_executando_dashboard.png)

### Executando o Streamlit
Executa o comando `streamlit run analitics_incidents.py` para iniciar a aplicação Streamlit.

- A aplicação Streamlit estará acessível através dos seguintes URLs:
  - Local URL: `http://localhost:8502`
  - Network URL: `http://192.168.0.106:8502`


## Imagem: 18_interface_dashboard.png
![18_interface_dashboard.png](/processed_images/18_interface_dashboard.png)

### Análise de Incidentes
O painel exibe estatísticas de incidentes para o mês de março de 2025, incluindo:

- Total de incidentes abertos no mês: 928
- Total de incidentes encerrados: 1071
- Total de incidentes sem atendente: 5
- Total de incidentes em backlog: 2
- Total de incidentes abertos: 186
- Incidentes em atendimento: 17
- Incidentes aguardando terceiros: 128
- Incidentes aguardando cliente: 31
- Incidentes agendados: 0
- Gráfico de incidentes encerrados por analista com total de 1247.

## Imagem: 19_opcao_download_imagem.png
![19_opcao_download_imagem.png](/processed_images/19_opcao_download_imagem.png)

### Gráfico de chamados abertos por serviço
Gráfico de chamados abertos por serviço, mostrando o total de chamados e o chamado mais antigo por serviço.
- No canto superior direito, há um botão para baixar o plot como um arquivo PNG.

## Imagem: 20_opcao_download_tabela_csv.png
![20_opcao_download_tabela_csv.png](/processed_images/20_opcao_download_tabela_csv.png)

### Download do relatório
Clique no botão "Download as CSV" para baixar o relatório exibido na tela em formato CSV.

## Imagem: 21_opcao_grafico_tela_cheia.png
![21_opcao_grafico_tela_cheia.png](/processed_images/21_opcao_grafico_tela_cheia.png)

### Gráfico de Chamados Criados por Mês
Acesso à opção de visualização em tela cheia do gráfico, clicando no botão "Fullscreen" destacado em vermelho.

## Imagem: 22_resultado_grafico_tela_cheia.png
![22_resultado_grafico_tela_cheia.png](/processed_images/22_resultado_grafico_tela_cheia.png)

### Gráfico de Chamados Criados por Mês
O gráfico apresenta o total de chamados criados por mês, variando de Março de 2024 a Março de 2025.

- **Março de 2024:** 11 chamados
- **Abril de 2024:** 2 chamados
- **Maio de 2024:** 1 chamado
- **Julho de 2024:** 79 chamados
- **Setembro de 2024:** 133 chamados
- **Novembro de 2024:** 1730 chamados
- **Janeiro de 2025:** 1869 chamados
- **Março de 2025:** 928 chamados


