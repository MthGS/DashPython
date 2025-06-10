import streamlit as st
import pandas as pd

 #Configuração inicial do Streamlit
st.set_page_config(
    page_title="Leagues",
    page_icon="🏆",
    layout="wide"
)


# Função para carregar os dados do arquivo CSV
# @st.cache_data otimiza o carregamento, lendo o arquivo do disco menos vezes.
@st.cache_data
def load_data_from_csv(file_path="fc25data/all_players.csv"):
    """Carrega dados de um arquivo CSV, tratando possíveis erros."""
    try:
        df = pd.read_csv(file_path, index_col=0)
        if df.empty:
            st.warning(f"Atenção: O arquivo '{file_path}' foi carregado, mas está vazio.")
        return df
    except FileNotFoundError:
        st.error(f"Erro Crítico: O arquivo de dados '{file_path}' não foi encontrado. Verifique o caminho.")
        return None
    except pd.errors.EmptyDataError: # Embora o df.empty acima já pegue, é bom ter para o erro do pandas
        st.error(f"Erro Crítico: O arquivo de dados '{file_path}' está vazio (detectado pelo Pandas).")
        return None
    except Exception as e:
        st.error(f"Erro Crítico ao carregar o arquivo '{file_path}': {e}")
        return None

# Tenta carregar os dados e armazena em st.session_state se ainda não estiverem lá.
# Isso garante que os dados sejam carregados apenas uma vez por sessão do usuário.
if "data" not in st.session_state:
    st.session_state.data = load_data_from_csv() # O caminho do arquivo é o padrão da função

# Prossegue somente se os dados foram carregados com sucesso em st.session_state.data
if st.session_state.data is not None:
    df_leagues_data = st.session_state.data

    # Verifica se a coluna "League" essencial existe no DataFrame
    if "League" not in df_leagues_data.columns:
        st.error("Erro Fatal: A coluna 'League' não foi encontrada no arquivo CSV carregado.")
        st.info("Verifique se o arquivo CSV contém uma coluna chamada 'League' com os nomes das ligas.")
        st.stop()  # Para a execução do script se a coluna chave estiver faltando

    # Processamento da coluna de Ligas para popular o selectbox
    try:
        # 1. Assegura que a coluna 'League' seja tratada como string.
        # 2. Remove espaços em branco no início e no fim dos nomes das ligas.
        # 3. Substitui nomes de liga que se tornaram strings vazias por pd.NA.
        # 4. Remove todas as entradas NA (incluindo NaNs originais e as strings vazias convertidas).
        # 5. Obtém os valores únicos.
        # 6. Converte para uma lista e ordena alfabeticamente.
        league_column = df_leagues_data["League"].astype(str).str.strip()
        unique_leagues_series = league_column.replace('', pd.NA).dropna().unique()
        list_of_leagues = sorted(list(unique_leagues_series))
        
    except Exception as e:
        st.error(f"Erro ao processar a coluna 'League' para criar a lista de seleção: {e}")
        list_of_leagues = [] # Define como lista vazia em caso de erro no processamento

    # Verifica se alguma liga foi encontrada após o processamento
    if not list_of_leagues:
        st.warning("Nenhuma liga válida foi encontrada nos dados para seleção.")
        st.info("Verifique se a coluna 'League' no seu arquivo CSV ('fc25data/all_players.csv') contém dados válidos.")
    else:
        # Cria o selectbox na barra lateral com as ligas encontradas
        selected_league = st.sidebar.selectbox("Selecione a Liga", list_of_leagues)

        if selected_league:
            # Exibe o título da liga selecionada
            st.title(f"🏆 {selected_league}")

            # Filtra o DataFrame original para obter dados apenas da liga selecionada.
            # É importante re-aplicar .astype(str).str.strip() na comparação para consistência,
            # caso haja variações sutis que não foram capturadas ou se a coluna original tiver tipos mistos.
            league_specific_data_df = df_leagues_data[
                df_leagues_data["League"].astype(str).str.strip() == selected_league
            ]

            if not league_specific_data_df.empty:
                st.write(f"Exibindo {len(league_specific_data_df)} registros para a liga: {selected_league}")
                st.dataframe(league_specific_data_df, use_container_width=True)

                # Exemplo de como você poderia usar a informação da primeira linha (como no seu código original):
                # if st.checkbox("Mostrar detalhes da primeira entrada (exemplo)"):
                #     first_entry_stats = league_specific_data_df.iloc[0]
                #     st.write("---")
                #     st.write(first_entry_stats)
            else:
                # Este caso é menos provável se selected_league veio de list_of_leagues, mas é uma salvaguarda.
                st.warning(f"Não foram encontrados dados para a liga '{selected_league}' após a filtragem, o que é inesperado.")
        else:
            # Mensagem inicial se nenhuma liga estiver selecionada (raro, pois o selectbox geralmente tem um padrão)
            st.info("Por favor, selecione uma liga na barra lateral para visualizar os dados.")
else:
    # Esta mensagem é exibida se st.session_state.data continuou None,
    # o que significa que load_data_from_csv() retornou None devido a um erro crítico.
    st.error("Os dados das ligas não puderam ser carregados.")
    st.info("Verifique o console para mensagens de erro detalhadas sobre o arquivo 'fc25data/all_players.csv'.")


##------------------------------
# #Verifica se os dados estão disponíveis no estado da sessão
#if "data" in st.session_state:
#    df_data = pd.read_csv("fc25data/all_players.csv", index_col=0)
#    df_leagues = st.session_state["data"]
#    Liga = df_leagues["League"].value_counts().index
#    selected_league = st.sidebar.selectbox("Liga", Liga)
#
#    # Filtra as informações da liga selecionada
#    league_stats = df_leagues[df_leagues["League"] == selected_league].iloc[0]
#
#    # Exibe o título do país e da liga
#    #selected_country = league_stats["Nation"]  # Supondo que exista uma coluna "Country"
#    #st.title(selected_country)
#    st.write(selected_league)
#else:
#    st.error("Os dados não estão disponíveis no estado da sessão.")