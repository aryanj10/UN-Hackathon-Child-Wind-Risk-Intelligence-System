import leafmap.foliumap as leafmap

def render_risk_map(risk_gdf, title="Child Wind Risk Map"):
    m = leafmap.Map(center=[23.7, 90.4], zoom=6)
    m.add_gdf(risk_gdf, layer_name="Child Wind Risk", info_mode="on_hover")

    max_risk = risk_gdf["Child Wind Risk"].max()
    riskiest = risk_gdf[risk_gdf["Child Wind Risk"] == max_risk]
    if not riskiest.empty:
        m.add_gdf(
            riskiest,
            layer_name="Highest Risk Areas",
            style={"color": "red", "weight": 5, "fillOpacity": 0.5},
            info_mode="on_hover"
        )
        centroid = riskiest.geometry.centroid.iloc[0]
        m.set_center(centroid.y, centroid.x, zoom=9)
    return m, max_risk
