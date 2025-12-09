import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Guía de gráficos HSE / SST", layout="wide")

st.title("📊 Guía práctica para elegir el gráfico adecuado en análisis de Incidentalidad (HSE / SST)")

st.markdown("""
Esta aplicación está diseñada para ayudar al personal de **Seguridad y Salud en el Trabajo (SST)** a identificar cuál es el **gráfico más adecuado** para cada tipo de análisis relacionado con incidentes, accidentalidad, severidad, frecuencia, horas-hombre trabajadas y cumplimiento.
""")

# ---------------------------------------------------------
# DATOS FALSOS PARA LA DEMO
# ---------------------------------------------------------

meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
         "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

df_incidentes = pd.DataFrame({
    "Mes": meses,
    "Casi incidente": np.random.randint(0, 5, 12),
    "Primer auxilio": np.random.randint(0, 4, 12),
    "Sin incapacidad": np.random.randint(0, 3, 12),
    "Con incapacidad": np.random.randint(0, 2, 12),
})

df_comparativo = pd.DataFrame({
    "Mes": meses,
    "2024": np.random.randint(0, 5, 12),
    "2025": np.random.randint(0, 5, 12),
})

df_severidad = pd.DataFrame({
    "Tipo de incidente": ["Casi incidente", "Primeros auxilios", "Sin incapacidad", "Con incapacidad"],
    "Días perdidos": np.random.randint(0, 15, 4)
})

df_acciones = pd.DataFrame({
    "Estado": ["Pendiente", "En proceso", "Cerrada"],
    "Cantidad": np.random.randint(2, 15, 3)
})

df_objetivos = pd.DataFrame({
    "Objetivo": [f"Objetivo {i}" for i in range(1, 8)],
    "Cumplimiento": np.random.choice(["SI", "NO"], 7)
})

df_indices = pd.DataFrame({
    "Mes": meses,
    "IF": np.random.uniform(0.2, 2.0, 12),
    "IS": np.random.uniform(1.0, 8.0, 12)
})

df_hht_area = pd.DataFrame({
    "Área": ["Operaciones", "Mantenimiento", "Administrativa", "Seguridad Física", "Ambiental"],
    "HHT": np.random.randint(500, 4000, 5)
})

df_hht_hist = pd.DataFrame({
    "HHT": np.random.randint(300, 5000, 200)
})

# Asegurar orden correcto de meses
categoria_meses = pd.CategoricalDtype(categories=meses, ordered=True)
df_incidentes["Mes"] = df_incidentes["Mes"].astype(categoria_meses)
df_comparativo["Mes"] = df_comparativo["Mes"].astype(categoria_meses)
df_indices["Mes"] = df_indices["Mes"].astype(categoria_meses)


# ---------------------------------------------------------
# MENÚ DE OPCIONES
# ---------------------------------------------------------

opcion = st.selectbox(
    "¿Qué deseas analizar?",
    [
        "Incidentes por mes",
        "Tipos de incidentes",
        "Comparación 2024 vs 2025",
        "Tendencia anual",
        "Proporción de tipos de incidente",
        "Seguimiento de acciones",
        "Pendientes vs cerrados",
        "Acciones seguras por área vs porcentaje de cumplimiento",
        "Cumplimiento de objetivos HSE",
        "Índice de Frecuencia y Severidad",
        "Horas Hombre Trabajadas por área",
        "Histograma de HHT"
    ]
)

st.markdown("---")


# ---------------------------------------------------------
# BLOQUES DE ANÁLISIS Y COMENTARIOS
# ---------------------------------------------------------

# ========================= 1. INCIDENTES POR MES =========================
if opcion == "Incidentes por mes":
    st.subheader("📌 ¿Por qué usar línea + barras para incidentes por mes?")
    st.info("""
Este tipo de gráfico es ideal porque:

- **La línea muestra la tendencia histórica**: si la accidentalidad va subiendo, bajando o está estable.
- **Las barras permiten comparar categorías entre sí**, mes por mes.
- Es útil para **identificar meses críticos**, estacionalidad y picos inesperados.
- Facilita la toma de decisiones preventivas basadas en comportamiento mensual.
""")

    st.plotly_chart(px.line(df_incidentes, x="Mes", y=df_incidentes.columns[1:], markers=True), use_container_width=True)
    st.plotly_chart(px.bar(df_incidentes, x="Mes", y=df_incidentes.columns[1:], barmode="group"), use_container_width=True)


# ========================= 2. TIPOS DE INCIDENTES =========================
elif opcion == "Tipos de incidentes":
    st.subheader("📌 ¿Por qué barras + gráfico circular para tipos de incidente?")
    st.info("""
- **Las barras** permiten ver claramente cuál tipo de incidente es más frecuente.
- El gráfico **circular muestra la proporción real**, reforzando visualmente la magnitud del riesgo.
- Esto ayuda al área SST a **priorizar controles** según el tipo de evento más común.
""")

    totales = df_incidentes.drop(columns="Mes").sum().reset_index()
    totales.columns = ["Tipo", "Cantidad"]

    st.plotly_chart(px.bar(totales, x="Tipo", y="Cantidad"), use_container_width=True)
    st.plotly_chart(px.pie(totales, names="Tipo", values="Cantidad"), use_container_width=True)


# ========================= 3. COMPARACIÓN =========================
elif opcion == "Comparación 2024 vs 2025":
    st.subheader("📌 ¿Por qué barras comparativas y no apiladas?")
    st.info("""
- Comparar 2024 vs 2025 **lado a lado** permite ver diferencias directo por mes.
- Las barras apiladas ocultan diferencias, por eso **no deben usarse en SST para comparaciones anuales**.
- Este gráfico ayuda a evaluar si los controles implementados **están funcionando** respecto al año anterior.
""")

    df_long = df_comparativo.melt(id_vars="Mes", var_name="Año", value_name="Incidentes")
    st.plotly_chart(px.bar(df_long, x="Mes", y="Incidentes", color="Año", barmode="group"), use_container_width=True)


# ========================= 4. TENDENCIA =========================
elif opcion == "Tendencia anual":
    st.subheader("📌 ¿Por qué usar una línea para tendencia?")
    st.info("""
La línea ayuda a responder preguntas críticas de SST:
- ¿La accidentalidad está **aumentando**, **disminuyendo** o **estabilizada**?
- ¿Hay meses con cambios bruscos que deban investigarse?
- ¿Los controles aplicados están mostrando impacto real?

Es el gráfico más usado en **informes de gestión**.
""")

    st.plotly_chart(px.line(df_incidentes, x="Mes", y=df_incidentes.columns[1:], markers=True), use_container_width=True)


# ========================= 5. SEVERIDAD =========================
elif opcion == "Días perdidos / severidad":
    st.subheader("📌 ¿Por qué barras + circular en severidad?")
    st.info("""
Porque permiten atacar dos preguntas claves:

1. **¿Qué tipo de incidente genera más días perdidos?**  
   (impacto directo en productividad)

2. **¿Cómo se distribuye la severidad entre tipos de evento?**  
   (riesgo crítico vs riesgo leve)

Esto es esencial en SST para orientar controles a **los eventos más dañinos**.
""")

    st.plotly_chart(px.bar(df_severidad, x="Tipo de incidente", y="Días perdidos"), use_container_width=True)
    st.plotly_chart(px.pie(df_severidad, names="Tipo de incidente", values="Días perdidos"), use_container_width=True)


# ========================= 6. PROPORCIÓN =========================
elif opcion == "Proporción de tipos de incidente":
    st.subheader("📌 ¿Por qué usar gráfico circular para proporciones?")
    st.info("""
El gráfico circular facilita ver:
- Qué tipo de incidente domina.
- La relación de un evento respecto a los otros.
- Qué actividad debe recibir **mayor control operativo**.

Es perfecto para presentar a **gerencia**.
""")

    totales = df_incidentes.drop(columns="Mes").sum().reset_index()
    totales.columns = ["Tipo", "Cantidad"]
    st.plotly_chart(px.pie(totales, names="Tipo", values="Cantidad"), use_container_width=True)


# ========================= 7. ACCIONES =========================
elif opcion == "Seguimiento de acciones":
    st.subheader("📌 ¿Por qué usar barras en acciones?")
    st.info("""
Las barras muestran rápidamente:
- Cuántas acciones están pendientes.
- Cuáles están en proceso.
- Cuáles se cerraron.

Esto ayuda a evaluar **eficiencia del sistema de investigación**.
""")

    st.plotly_chart(px.bar(df_acciones, x="Estado", y="Cantidad"), use_container_width=True)


# ========================= 8. PENDIENTES VS CERRADOS =========================
elif opcion == "Pendientes vs cerrados":
    st.subheader("📌 ¿Por qué barras + circular?")
    st.info("""
- La **barra** muestra la cantidad exacta.  
- El **circular** permite ver la proporción cerrada vs pendiente.  

Es la mejor forma de evaluar si el sistema es **reactivo o realmente preventivo**.
""")

    st.plotly_chart(px.bar(df_acciones, x="Estado", y="Cantidad"), use_container_width=True)
    st.plotly_chart(px.pie(df_acciones, names="Estado", values="Cantidad"), use_container_width=True)


# ========================= 9. CUMPLIMIENTO =========================
elif opcion == "Cumplimiento de objetivos HSE":
    st.subheader("📌 ¿Por qué usar un gráfico radial (gauge)?")
    st.info("""
Un indicador radial permite entender el cumplimiento **de un solo vistazo**.  
Es el formato estándar en:

- Auditorías
- Informes de gestión
- Revisión por la dirección
- Presentaciones de indicadores

Permite identificar si el área SST está **en verde, amarillo o rojo**.
""")

    cumplimiento = (df_objetivos["Cumplimiento"] == "SI").mean() * 100

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cumplimiento,
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "green"}}
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.write("Detalle por objetivo:")
    st.dataframe(df_objetivos)


# ========================= 10. IF / IS =========================
elif opcion == "Índice de Frecuencia y Severidad":
    st.subheader("📌 ¿Por qué este gráfico para IF/IS?")
    st.info("""
Este gráfico responde preguntas cruciales:

- ¿Estamos **por encima** de los límites aceptables?  
- ¿Hay meses donde la severidad se dispara?  
- ¿Los incidentes están siendo graves o solo frecuentes?

Incluye indicadores visuales para IF = 1 y IS = 4,  
que son límites **estándar en SST**.
""")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_indices["Mes"], y=df_indices["IF"], mode="lines+markers", name="IF"))
    fig.add_trace(go.Scatter(x=df_indices["Mes"], y=df_indices["IS"], mode="lines+markers", name="IS"))

    fig.add_hline(y=1, line_dash="dot", line_color="red", annotation_text="Límite IF=1")
    fig.add_hline(y=4, line_dash="dot", line_color="orange", annotation_text="Límite IS=4")

    st.plotly_chart(fig, use_container_width=True)


# ========================= 11. HHT por área =========================
elif opcion == "Horas Hombre Trabajadas por área":
    st.subheader("📌 ¿Por qué usar barras en HHT por área?")
    st.info("""
Porque permite identificar **qué áreas están más expuestas al riesgo**,  
debido a mayor carga de trabajo o mayor presencia operativa.

Es clave para:
- Dimensionar recursos,
- Programar inspecciones,
- Evaluar exposición.
""")

    st.plotly_chart(px.bar(df_hht_area, x="Área", y="HHT"), use_container_width=True)


# ========================= 12. HISTOGRAMA =========================
elif opcion == "Histograma de HHT":
    st.subheader("📌 ¿Por qué usar un histograma para HHT?")
    st.info("""
El histograma muestra:
- Variabilidad de horas trabajadas,
- Concentración de valores,
- Valores extremos (picos operativos),
- Comportamientos atípicos.

Esto ayuda a entender la **carga operativa real** en la empresa.
""")

    st.plotly_chart(px.histogram(df_hht_hist, x="HHT", nbins=20), use_container_width=True)

# ========================= 13. GRAFICO 3 VARIABLES (MIXTO) =========================
elif opcion == "Acciones seguras por área vs porcentaje de cumplimiento":
    st.subheader("📌 Acciones seguras por área vs porcentaje de cumplimiento")
    
    st.info("""
Este gráfico es ideal para SST porque combina **cantidad y desempeño**:
    
- Las **barras** muestran cuántas actividades seguras realizó cada área  
  (inspecciones, pausas activas, reportes seguros, observaciones, etc.)
- La **línea con segundo eje Y** muestra el porcentaje de cumplimiento del programa.
- Las **etiquetas sobre cada punto** permiten ver el cumplimiento exacto.
    
Esto permite identificar:
- Áreas que hacen muchas actividades pero **no cumplen la meta**
- Áreas que cumplen al 100% con esfuerzo eficiente
- Dónde priorizar apoyo, capacitaciones o inspecciones
""")

    # Datos ficticios
    df_mix = pd.DataFrame({
        "Área": ["Operaciones", "Mantenimiento", "Administrativa", "Seguridad Física", "Ambiental"],
        "Actividades_seguras": np.random.randint(10, 60, 5),
        "Cumplimiento_%": np.random.uniform(40, 100, 5).round(1)
    })

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Barras
    fig.add_trace(
        go.Bar(
            x=df_mix["Área"],
            y=df_mix["Actividades_seguras"],
            name="Actividades seguras realizadas",
            marker_color="steelblue"
        ),
        secondary_y=False
    )

    # Línea con segundo eje
    fig.add_trace(
        go.Scatter(
            x=df_mix["Área"],
            y=df_mix["Cumplimiento_%"],
            name="Cumplimiento (%)",
            mode="lines+markers+text",
            text=df_mix["Cumplimiento_%"].astype(str) + "%",
            textposition="top center",
            line=dict(color="orange", width=3),
            marker=dict(size=9)
        ),
        secondary_y=True
    )

    fig.update_layout(
        title="Actividades seguras realizadas vs porcentaje de cumplimiento por área",
        xaxis_title="Área",
        yaxis_title="Actividades seguras",
        legend_title="Variables evaluadas",
        bargap=0.3
    )

    fig.update_yaxes(
        title_text="Cumplimiento (%)",
        secondary_y=True,
        range=[0, 120]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write("📄 **Tabla de datos usados en el gráfico:**")
    st.dataframe(df_mix)

# ---------------------------------------------------------
# GUÍA FINAL SST
# ---------------------------------------------------------

st.markdown("---")
st.success("""
### 📘 Guía rápida SST (resumen final)
- **Meses →** Línea + barras  
- **Categorías →** Barras  
- **Proporciones →** Circular  
- **Comparaciones por año →** Barras comparativas  
- **Severidad →** Barras + circular  
- **Acciones →** Barras  
- **Cumplimiento →** Indicador radial  
- **IF / IS →** Líneas + límites  
- **HHT por área →** Barras  
- **Variabilidad HHT →** Histograma  
""")




