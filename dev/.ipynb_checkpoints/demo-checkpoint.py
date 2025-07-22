import marimo

__generated_with = "0.14.12"
app = marimo.App(width="medium")


app._unparsable_cell(
    r"""
    import panel as pn
    import panel_material_ui as pmui
    #from panel_material_ui.theme import MaterialLightTheme
    from panel_siemens_ix.theme import siemens_ix_light_theme, siemens_ix_dark_theme

    pn.extension()#'material-ui', template='material', sizing_mode='stretch_width')
    template = pmui.Page(theme_config=dict(light=siemens_ix_light_theme(), dark=siemens_ix_dark_theme(), )
    # Create a Material-UI template with the Siemens iX light theme
    #pmui.param.Page.

    # Example content
    template.main.append(pmui.Button(name=\"Primary Button\", button_type=\"primary\"))
    template.main.append(pmui.Button(name=\"Secondary Button\", button_type=\"default\"))
    template.main.append(pmui.TextInput(name=\"Text Input\", value=\"Hello Siemens iX!\"))

    template.servable()
    """,
    name="_"
)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
