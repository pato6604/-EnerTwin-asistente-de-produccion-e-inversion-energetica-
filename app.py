import streamlit as st

st.set_page_config(page_title="EnerTwin", layout="wide")

st.title("EnerTwin")
st.subheader("Simulador de prefactibilidad eólica e hidrógeno verde")

st.write("""
EnerTwin estima la producción potencial de energía eólica de una granja,
la conversión de excedentes en hidrógeno verde y el CO₂ evitado frente a
generación termoeléctrica.
""")

st.sidebar.header("Parámetros del terreno y parque")

n_turbinas = st.sidebar.slider("Cantidad de aerogeneradores", 1, 100, 10)
potencia_turbina_mw = st.sidebar.number_input("Potencia por aerogenerador (MW)", 0.5, 10.0, 3.0)
factor_capacidad = st.sidebar.slider("Factor de capacidad estimado (%)", 0, 70, 40) / 100
horas = st.sidebar.number_input("Horas del período simulado", 1, 8760, 720)

st.sidebar.header("Hidrógeno verde")

porcentaje_electrolisis = st.sidebar.slider(
    "Energía destinada a electrólisis (%)", 0, 100, 30
) / 100

kwh_por_kg_h2 = st.sidebar.number_input(
    "Consumo electrolizador (kWh/kg H₂)", 40.0, 80.0, 55.0
)

st.sidebar.header("Impacto económico-ambiental")

factor_emision = st.sidebar.number_input(
    "Factor emisión termoeléctrica (ton CO₂/MWh)", 0.1, 1.5, 0.5
)

precio_mwh = st.sidebar.number_input("Precio energía (USD/MWh)", 0.0, 300.0, 80.0)
precio_h2 = st.sidebar.number_input("Precio H₂ verde (USD/kg)", 0.0, 20.0, 5.0)
precio_carbono = st.sidebar.number_input("Precio carbono (USD/ton CO₂)", 0.0, 200.0, 30.0)

# Cálculos principales
potencia_total_mw = n_turbinas * potencia_turbina_mw

energia_total_mwh = potencia_total_mw * horas * factor_capacidad

energia_electrolisis_mwh = energia_total_mwh * porcentaje_electrolisis
energia_venta_mwh = energia_total_mwh - energia_electrolisis_mwh

kg_h2 = (energia_electrolisis_mwh * 1000) / kwh_por_kg_h2
kg_o2 = kg_h2 * 8

co2_evitado = energia_total_mwh * factor_emision

ingreso_energia = energia_venta_mwh * precio_mwh
ingreso_h2 = kg_h2 * precio_h2
ingreso_carbono = co2_evitado * precio_carbono

ingreso_total = ingreso_energia + ingreso_h2 + ingreso_carbono

col1, col2, col3, col4 = st.columns(4)

col1.metric("Potencia instalada", f"{potencia_total_mw:.2f} MW")
col2.metric("Energía estimada", f"{energia_total_mwh:,.0f} MWh")
col3.metric("H₂ verde estimado", f"{kg_h2:,.0f} kg")
col4.metric("CO₂ evitado", f"{co2_evitado:,.0f} ton")

st.divider()

col5, col6, col7 = st.columns(3)

col5.metric("O₂ generado", f"{kg_o2:,.0f} kg")
col6.metric("Ingreso potencial", f"USD {ingreso_total:,.0f}")
col7.metric("Energía vendida", f"{energia_venta_mwh:,.0f} MWh")

st.subheader("Resumen de resultados")

st.write(f"""
Para una granja de **{n_turbinas} aerogeneradores** de **{potencia_turbina_mw} MW**
cada uno, EnerTwin estima una producción de **{energia_total_mwh:,.0f} MWh**
durante el período simulado.

De esa energía, **{energia_electrolisis_mwh:,.0f} MWh** se destinan a electrólisis,
produciendo aproximadamente **{kg_h2:,.0f} kg de hidrógeno verde** y
**{kg_o2:,.0f} kg de oxígeno** como subproducto.

Frente a una alternativa termoeléctrica, se evitarían aproximadamente
**{co2_evitado:,.0f} toneladas de CO₂**.
""")

st.caption("""
Esta demo utiliza un modelo simplificado de prefactibilidad. En una versión real,
EnerTwin se calibraría con datos meteorológicos locales, sensores en campo,
curvas de potencia reales de aerogeneradores y datos operativos históricos.
""")