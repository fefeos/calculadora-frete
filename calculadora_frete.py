import streamlit as st
import googlemaps

# Configuração inicial da página
st.set_page_config(page_title="Calculadora de Frete", page_icon="🚚", layout="centered")

# Estilo CSS personalizado com fundo mais escuro para o resultado
st.markdown("""
    <style>
        .main {background-color: #f8f9fa;}
        .titulo {color: #1f77b4; font-size: 2.5rem; font-weight: 700;}
        .subtitulo {color: #555; font-size: 1.1rem;}
        .resultado-box {
            background-color: #1e3a5f;  /* Azul mais escuro */
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1rem;
            border: 1px solid #0d2a47;
            color: #f1f1f1;  /* Texto claro */
        }
        .info {
            color: #7dd3fc;  /* Azul claro para destaque */
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# API Google Maps
API_KEY = 'AIzaSyAkHMRQeKlTckbizlNI5c8fQ38Z8HpL82k'
gmaps = googlemaps.Client(key=API_KEY)

# Cabeçalho
st.markdown('<div class="titulo">📍 Calculadora de Frete</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Calcule distâncias e valores estimados de frete</div>', unsafe_allow_html=True)
st.divider()

# Endereço fixo de origem
origem = "R. Ten. Alberto Spicciati, 156 - São Paulo - SP"
st.markdown(f"**Endereço de origem:** `{origem}`")

# Formulário do destino
with st.form(key="formulario"):
    destino = st.text_input("Digite o endereço de destino:")
    calcular = st.form_submit_button("🚗 Calcular Distância")

# Processamento
if calcular:
    if destino.strip() == "":
        st.warning("⚠️ Por favor, digite um endereço válido.")
    else:
        try:
            resultado = gmaps.distance_matrix(origem, destino, mode='driving', language='pt-BR')

            if resultado['status'] != 'OK':
                raise Exception('Erro na resposta da API.')

            distancia_metros = resultado['rows'][0]['elements'][0]['distance']['value']
            distancia_km = distancia_metros / 1000

            ida_volta = distancia_km * 2
            distancia_x4 = ida_volta * 3
            resultado_final = distancia_x4 * 2

            # Exibindo resultado com fundo mais escuro
            st.markdown(f"""
                <div class="resultado-box">
                    <h4>✅ Resultado:</h4>
                    <p><b>Destino:</b> <span class="info">{destino}</span></p>
                    <p><b>Distância (ida):</b> {distancia_km:.2f} km</p>
                    <p><b>Distância (ida e volta):</b> {ida_volta:.2f} km</p>
                    <p><b>Valor total do frete:</b> <span class="info">R$ {distancia_x4:.2f}</span></p>
                    <p><b>Taxas adicionais (transporte e alimentação):</b> <span class="info">R$ {resultado_final:.2f}</span></p>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Erro: {e}")
