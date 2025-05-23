import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Neymar: Evolução do Valor de Mercado",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Dados Históricos de Valor de Mercado (Simulados/Manual) ---
neymar_market_value_data = [
    # Santos (2009-2013) - 1ª Passagem
    {"Date": "2009-07-23", "Market_Value_EUR_M": 1.0, "Club": "Santos - 1ª Passagem"},
    {"Date": "2010-06-10", "Market_Value_EUR_M": 15.0, "Club": "Santos - 1ª Passagem"},
    {"Date": "2011-06-29", "Market_Value_EUR_M": 30.0, "Club": "Santos - 1ª Passagem"},
    {"Date": "2012-08-01", "Market_Value_EUR_M": 50.0, "Club": "Santos - 1ª Passagem"},
    {"Date": "2013-03-20", "Market_Value_EUR_M": 50.0, "Club": "Santos - 1ª Passagem"},
    # Barcelona (2013-2017)
    {"Date": "2013-09-02", "Market_Value_EUR_M": 50.0, "Club": "Barcelona"},
    {"Date": "2014-06-10", "Market_Value_EUR_M": 70.0, "Club": "Barcelona"},
    {"Date": "2015-02-09", "Market_Value_EUR_M": 80.0, "Club": "Barcelona"},
    {"Date": "2015-07-01", "Market_Value_EUR_M": 100.0, "Club": "Barcelona"},
    {"Date": "2016-03-17", "Market_Value_EUR_M": 100.0, "Club": "Barcelona"},
    {"Date": "2017-01-20", "Market_Value_EUR_M": 100.0, "Club": "Barcelona"},
    {"Date": "2017-06-26", "Market_Value_EUR_M": 100.0, "Club": "Barcelona"},
    # Paris SG (2017-2023)
    {"Date": "2017-08-03", "Market_Value_EUR_M": 150.0, "Club": "Paris SG"},
    {"Date": "2018-01-24", "Market_Value_EUR_M": 180.0, "Club": "Paris SG"},
    {"Date": "2018-05-29", "Market_Value_EUR_M": 180.0, "Club": "Paris SG"},
    {"Date": "2018-12-17", "Market_Value_EUR_M": 180.0, "Club": "Paris SG"},
    {"Date": "2019-06-12", "Market_Value_EUR_M": 180.0, "Club": "Paris SG"},
    {"Date": "2019-12-18", "Market_Value_EUR_M": 160.0, "Club": "Paris SG"},
    {"Date": "2020-04-08", "Market_Value_EUR_M": 128.0, "Club": "Paris SG"},
    {"Date": "2020-10-12", "Market_Value_EUR_M": 128.0, "Club": "Paris SG"},
    {"Date": "2021-06-25", "Market_Value_EUR_M": 100.0, "Club": "Paris SG"},
    {"Date": "2022-03-24", "Market_Value_EUR_M": 90.0, "Club": "Paris SG"},
    {"Date": "2022-11-07", "Market_Value_EUR_M": 75.0, "Club": "Paris SG"},
    {"Date": "2023-03-27", "Market_Value_EUR_M": 70.0, "Club": "Paris SG"},
    {"Date": "2023-06-20", "Market_Value_EUR_M": 60.0, "Club": "Paris SG"},
    # Al-Hilal (2023-presente)
    {"Date": "2023-08-15", "Market_Value_EUR_M": 60.0, "Club": "Al-Hilal"},
    {"Date": "2023-12-14", "Market_Value_EUR_M": 45.0, "Club": "Al-Hilal"},
    {"Date": "2024-03-25", "Market_Value_EUR_M": 30.0, "Club": "Al-Hilal"},
    {"Date": "2024-06-15", "Market_Value_EUR_M": 25.0, "Club": "Al-Hilal"},
    {"Date": "2024-09-20", "Market_Value_EUR_M": 20.0, "Club": "Al-Hilal"},
    # Santos (Retorno) - 2ª Passagem
    {"Date": "2024-12-13", "Market_Value_EUR_M": 15.0, "Club": "Santos - 2ª Passagem"}
]

df_market_value = pd.DataFrame(neymar_market_value_data)
df_market_value['Date'] = pd.to_datetime(df_market_value['Date'])

# Cores para as linhas do gráfico
club_colors_altair = alt.Scale(
    domain=["Santos - 1ª Passagem", "Barcelona", "Paris SG", "Al-Hilal", "Santos - 2ª Passagem"],
    range=["#7e57c2", "#2196f3", "#ef5350", "#009688", "#4CAF50"]
)

# Função principal do Streamlit
def main():
    st.title("💸 Neymar Jr.: Evolução do Valor de Mercado ao Longo da Carreira")
    st.markdown("""
    Esta aplicação compara a evolução do valor de mercado do Neymar Jr. em seus principais clubes,
    com base em dados históricos. Passe o mouse sobre as linhas para ver os detalhes!
    """)

    st.sidebar.header("Filtros e Visualização")
    selected_clubs = st.sidebar.multiselect(
        "Selecione os Clubes para Comparar:",
        options=df_market_value['Club'].unique().tolist(),
        default=df_market_value['Club'].unique().tolist()
    )

    if not selected_clubs:
        st.warning("Por favor, selecione ao menos um clube para exibir a análise.")
        return

    df_filtered = df_market_value[df_market_value['Club'].isin(selected_clubs)]


    st.header("Gráfico Interativo: Evolução do Valor de Mercado")

    # Tema escuro para Altair (atualizado para a nova sintaxe de altair >= 5.5.0)
    @alt.theme.register("dark_theme", enable=True)
    def dark_theme():
        return alt.theme.ThemeConfig(
            {
                "background": "#1C1C1C", # Cor de fundo da figura
                "title": {
                    "color": "white"
                },
                "axis": {
                    "gridColor": "#4A4A4A", # Cor da grade
                    "labelColor": "white",
                    "titleColor": "white"
                },
                "header": {
                    "labelColor": "white",
                    "titleColor": "white"
                },
                "legend": {
                    "labelColor": "white",
                    "titleColor": "white",
                    "fillColor": "#1C1C1C", # Cor de fundo da legenda
                    "strokeColor": "#1C1C1C" # Cor da borda da legenda
                }
            }
        )


    # --- Gráfico de Linhas Principal (com correção de sintaxe) ---
    chart = alt.Chart(df_filtered).mark_line(point=True, strokeWidth=2.5).encode(
        x=alt.X('Date:T', title='Data', axis=alt.Axis(format='%Y', labelAngle=0, tickCount='year', values=[f'{y}-01-01' for y in range(2009, 2025, 5)])),
        y=alt.Y('Market_Value_EUR_M:Q', title='Valor de Mercado (€ Milhões)', axis=alt.Axis(format='~s')),
        color=alt.Color('Club:N', scale=club_colors_altair, legend=alt.Legend(title="Clube")),
        tooltip=[
            alt.Tooltip('Date:T', title='Data', format='%Y-%m-%d'),
            alt.Tooltip('Market_Value_EUR_M:Q', title='Valor (€ Milhões)', format='~s'),
            alt.Tooltip('Club:N', title='Clube')
        ]
    ).properties(
        title='Evolução do Valor de Mercado de Neymar (em milhões de €)',
        height=400, # Altura do gráfico
        width='container' # Preenche a largura disponível no Streamlit
    ).interactive().configure_title( 
        anchor='start', # Alinha o título à esquerda
        fontSize=20,
        offset=20
    ).configure_axis(
        grid=True,
        gridColor='#4A4A4A',
        domain=False # Remove a linha da borda do eixo
    ).configure_legend(
        orient="bottom", # Legenda na parte inferior
        columns=3, # Tenta organizar em 3 colunas
        labelLimit=0, # Remove limite de caracteres do label
        titleLimit=0 # Remove limite de caracteres do título
    )


    st.altair_chart(chart, use_container_width=True)

    st.markdown("---")

    st.header("Histórico do Valor de Mercado")
    st.markdown("Veja os dados brutos da evolução do valor de mercado do Neymar, acordo com o site especializado Transfermarkt")
    st.dataframe(df_filtered.sort_values(by='Date').set_index('Date').style.format({"Market_Value_EUR_M": "€{:,.2f}M"}))
    st.markdown("---")
    
    st.info("""
    **Observação Importante:** Os dados de valor de mercado são **simulados** para fins de demonstração,
    baseados em observações visuais do gráfico do Transfermarkt. Para um projeto real,
    seria ideal coletar esses dados de forma mais precisa (ex: raspagem de dados permitida ou acesso a API)
    para garantir a exatidão da análise. A flutuação de valor de mercado pode ser influenciada por muitos fatores,
    incluindo desempenho, lesões, idade, duração do contrato, etc.
    """)

    st.markdown("""
    Este aplicativo serve como uma prova de conceito para visualizar a trajetória de valor de um jogador
    ao longo de sua carreira.
    """)

# Rodar a função principal
if __name__ == "__main__":
    main()
