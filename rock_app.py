import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Videoclub de Rock AR", page_icon="🎸", layout="wide")

# --- ESTILO CSS REFORZADO ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .movie-card {
        background-color: #1a1c24;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #3e4452;
        margin-bottom: 10px;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .movie-title {
        color: #ff4b4b;
        font-size: 1.1rem !important;
        font-weight: bold;
    }
    .btn-ver-final {
        display: block; text-align: center; background-color: #ff4b4b;
        color: white !important; padding: 10px; border-radius: 8px;
        text-decoration: none !important; font-weight: bold; width: 100%;
    }
    /* Estilo para el indicador de página */
    .pag-info {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def cargar_datos(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    df = pd.read_csv(csv_url)
    df.columns = df.columns.str.strip()
    return df

VINCULO_SHEET = "https://docs.google.com/spreadsheets/d/1Us3o7jgxBDyAPPViIxTprXSS9lDccdEDyKNIJiw8h_g/edit?usp=sharing"

try:
    df = cargar_datos(VINCULO_SHEET)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# --- SIDEBAR: FILTROS MEJORADOS ---
st.sidebar.title("🎸 Filtros Rock")

# 1. Buscador por Artista / Título (Desplegable)
opciones_musica = ["Todos los artistas"] + sorted(df['Titulo'].unique().tolist())
seleccion = st.sidebar.selectbox("🎯 Elegí un video o artista:", opciones_musica)

# --- LÓGICA DE FILTRADO ---
if seleccion != "Todos los artistas":
    df_filtrado = df[df['Titulo'] == seleccion]
else:
    df_filtrado = df

# --- PAGINACIÓN CON INDICADOR ---
items_por_pag = 9
total_items = len(df_filtrado)
paginas_totales = max((total_items // items_por_pag) + (1 if total_items % items_por_pag > 0 else 0), 1)

st.sidebar.divider()
pagina_actual = st.sidebar.number_input(f"Página (de {paginas_totales})", min_value=1, max_value=paginas_totales, step=1)
st.sidebar.markdown(f"<div class='pag-info'>Viendo {len(df_filtrado)} resultados</div>", unsafe_allow_html=True)

inicio = (pagina_actual - 1) * items_por_pag
df_a_mostrar = df_filtrado.iloc[inicio:inicio + items_por_pag]

# --- CUERPO PRINCIPAL ---
st.title("🎥 Videoclub de Rock Argentino")

cols = st.columns(3)
for i, (idx, row) in enumerate(df_a_mostrar.iterrows()):
    with cols[i % 3]:
        with st.container():
            st.markdown(f"""
                <div class="movie-card">
                    <div>
                        <div class="movie-title">🤘 {row['Titulo']}</div>
                        <div style="font-size: 0.9rem; color: #cbd5e0; margin-top:10px;">
                            <b>🎬 Director:</b> {row['Director']}<br>
                            <b>📅 Año:</b> {row['Año']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("ℹ️ Info", str(row['Link_Info']), use_container_width=True)
            with c2:
                st.markdown(f'<a href="{row["Link_Video"]}" target="_blank" class="btn-ver-final">▶️ Ver</a>', unsafe_allow_html=True)

st.divider()
st.markdown(f"<p style='text-align: center; color: gray;'>© 2026 Archivo Rock</p>", unsafe_allow_html=True)


if __name__ == "__main__":
    pass