import leafmap.foliumap as leafmap

def render_risk_map(risk_gdf, score_column="Child Wind Risk"):
    m = leafmap.Map(center=[23.7, 90.4], zoom=6)

    # Add the full GeoDataFrame using specified score
    m.add_gdf(
        risk_gdf,
        layer_name="Risk Map",
        info_mode="on_hover",
        info_fields=[score_column],
        style={"fillOpacity": 0.6}
    )

    # Highlight the region with the max score
    max_risk = risk_gdf[score_column].max()
    riskiest = risk_gdf[risk_gdf[score_column] == max_risk]
    if not riskiest.empty:
        m.add_gdf(
            riskiest,
            layer_name="Highest Risk Zone",
            style={"color": "red", "weight": 3, "fillOpacity": 0.5},
            info_mode="on_hover"
        )
        centroid = riskiest.geometry.centroid.iloc[0]
        m.set_center(centroid.y, centroid.x, zoom=9)

    return m, max_risk
