# view.py - User interface for app
# rcampbel@purdue.edu - 2020-07-14

import sys
import ipywidgets as widgets
from IPython.display import HTML, display, clear_output

from nb.log import logger, log_handler


"""Store app-wide constants, including values and language text."""

# NOTE Simple language string definiitions below: for better features, consider using the following:
# - Multilingual internationalization: https://docs.python.org/2/library/gettext.html
# - Data classes: https://docs.python.org/3/library/dataclasses.html
# - Bound attributes: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s16.html

# General
APP_TITLE = 'Land-Ocean Temperature Index'
CSS_JS_HTML = 'nb/custom.html'
LOGO_IMAGE = 'nb/logo.png'
ALL = 'All'
EMPTY = ''
NO_DATA_MSG = '''<br>(There's no data to display.)'''
TAB_TITLES = ['Welcome', 'Data', 'Selection', 'Visualize', 'Settings']
PLOT_TITLE = 'Land-Ocean Temperature Index'

# Welcome tab
USING_TITLE = 'Using This App'
USING_TEXT = '''<p>
In the <b>Data</b> tab above, you can review the dataset.
In the <b>Selection</b> tab, you can search for and download data of interest.
Once you've selected data, generate plots in the <b>Visualize</b> tab.
</p>'''
SOURCES_TITLE = 'Data Sources'
SOURCES_TEXT = '''<p>
<b>Land-Ocean Temperature Index</b>
<a href="https://climate.nasa.gov/vital-signs/global-temperature/"
target="_blank">Global Temperature (NASA)</a>
,
<a href="https://data.giss.nasa.gov/gistemp/"
target="_blank">GISS Surface Temperature Analysis (NASA)</a>
</p><p>
This site is based on data downloaded from the following site on 2020-07-14:
<a href="https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt"  # noqa
target="_blank">Global Mean Estimates based on Land_and Ocean Data (NASA)</a>
<br>
The code behind this site is intended as a template for anyone wanting to develop similar appliations. Source code
is available <a href="https://github.com/rcpurdue/nbtmpl" target="_blank">here</a>.
</p>'''

# Data tab
PREVIEW_SECTION_TITLE = 'Data'
EXPORT_LINK_PROMPT = "Click here to save file: "

# Selection tab
CRITERIA_TITLE = 'Selection Criteria'
CRITERIA_APPLY = 'Filter'
OUTPUT_TITLE = 'Results'
OUTPUT_PRE = 'Limit to '
OUTPUT_POST = 'lines'
EXPORT_TITLE = 'Export'
EXPORT_BUTTON = 'Create Download Link'
START_YEAR = 'From Year'
END_YEAR = 'To Year'

# Visualize tab
NOTE_TITLE = 'Note'
NOTE_TEXT = 'The plot is based on results from the Selection tab.'
PLOT_TITLE = 'Plot'
PLOT_LABEL = 'Select data field'

# Setting tab
PLOT_SETTINGS_SECTION_TITLE = 'Plot Settings'
THEME = 'Theme'
THEMES = ['onedork', 'grade3', 'oceans16', 'chesterish', 'monokai', 'solarizedl', 'solarizedd']
CONTEXT = 'Context'
CONTEXTS = ['paper', 'notebook', 'talk', 'poster']
FONT_SCALE = 'Font Scale'
SPINES = 'Spines'
GRIDLINES = 'Gridlines'
TICKS = 'Ticks'
GRID = 'Grid'
FIG_WIDTH = 'Width'
FIG_HEIGHT = 'Height'
APPLY = 'Apply'

LO10 = widgets.Layout(width='10%')
LO15 = widgets.Layout(width='15%')
LO20 = widgets.Layout(width='20%')

view = sys.modules[__name__]

# The view's "public" attributes are listed here, with type hints, for quick reference

# Filer ("Selection" tab) controls
filter_txt_startyr: widgets.Text
filter_txt_endyr: widgets.Text
filter_btn_apply: widgets.Button
filter_ddn_ndisp: widgets.Dropdown
filter_output: widgets.Output
filter_btn_refexp: widgets.Button
filter_out_export: widgets.Output

# Plot ("Visualize" tab) controls
plot_ddn: widgets.Dropdown
plot_output: widgets.Output

# Settings controls
theme: widgets.Dropdown
context: widgets.Dropdown
fscale: widgets.FloatSlider
spines: widgets.Checkbox
gridlines: widgets.Text
ticks: widgets.Checkbox
grid: widgets.Checkbox
figsize1: widgets.FloatSlider
figsize2: widgets.FloatSlider
apply: widgets.Button


def start(show_log):
    """Build the user interface."""

    # Send app's custom styles (CSS code) down to the browser
    display(HTML(filename=CSS_JS_HTML))

    # Create large title for app
    app_title = widgets.HTML(APP_TITLE)
    app_title.add_class('app_title')  # Example of custom widget style via CSS, see custom.html

    # Create app logo - example of using exposed layout properties
    with open(LOGO_IMAGE, "rb") as logo_file:
        logo = widgets.Image(value=logo_file.read(), format='png', layout={'max_height': '32px'})

    # Create tabs and fill with UI content (widgets)

    tabs = widgets.Tab()

    # Add title text for each tab
    for i, tab_title in enumerate(TAB_TITLES):
        tabs.set_title(i, tab_title)

    # Build conent (widgets) for each tab
    tab_content = []
    tab_content.append(view.build_welcome_tab())
    tab_content.append(view.build_data_tab())
    tab_content.append(view.build_selection_tab())
    tab_content.append(view.build_visualize_tab())
    tab_content.append(view.build_settings_tab())

    tabs.children = tuple(tab_content)  # Fill tabs with content

    # Show the app
    header = widgets.HBox([app_title, logo])
    header.layout.justify_content = 'space-between'  # Example of custom widget layout
    display(widgets.VBox([header, tabs]))
    logger.info('UI build completed')

    # Optionally, display a widget that shows the log items
    # Log items always appear in Jupyter Lab's log.
    # However, this addl. log widget is useful in some contexts (e.g. HUBzero tools)
    if show_log:
        display(log_handler.log_output_widget)


def new_section(title, contents):
    '''Utility method that create a collapsible widget container'''

    if type(contents) == str:
        contents = [widgets.HTML(value=contents)]

    ret = widgets.Accordion(children=tuple([widgets.VBox(contents)]))
    ret.set_title(0, title)
    return ret


def build_welcome_tab():
    '''Create widgets for introductory tab content'''
    content = []
    content.append(view.section(USING_TITLE, USING_TEXT))
    content.append(view.section(SOURCES_TITLE, SOURCES_TEXT))
    return widgets.VBox(content)


def build_data_tab():
    '''Show data tab content'''
    view.data_preview_out = widgets.Output()
    return view.section(PREVIEW_SECTION_TITLE, [view.data_preview_out])


def build_selection_tab():
    '''Create widgets for selection tab content'''
    view.filter_txt_startyr = widgets.Text(description=START_YEAR, value='', placeholder='')
    view.filter_txt_endyr = widgets.Text(description=END_YEAR, value='', placeholder='')
    view.filter_btn_apply = widgets.Button(description=CRITERIA_APPLY, icon='filter', layout=view.LO20)
    view.filter_ddn_ndisp = widgets.Dropdown(options=['25', '50', '100', ALL], layout=view.LO10)
    view.filter_output = widgets.Output()
    view.filter_btn_refexp = widgets.Button(description=EXPORT_BUTTON, icon='download',
                                            layout=view.LO20)
    view.filter_out_export = widgets.Output(layout={'border': '1px solid black'})
    content = []

    # Section: Selection criteria
    section_list = []
    section_list.append(view.filter_txt_startyr)
    section_list.append(view.filter_txt_endyr)
    section_list.append(view.filter_btn_apply)
    content.append(view.section(CRITERIA_TITLE, section_list))

    # Section: Output (with apply button)
    section_list = []
    row = []
    row.append(widgets.HTML('<div style="text-align: right;">'+OUTPUT_PRE+'</div>', layout=view.LO15))
    row.append(view.filter_ddn_ndisp)
    row.append(widgets.HTML('<div style="text-align: left;">' + OUTPUT_POST + '</div>', layout=view.LO10))
    section_list.append(widgets.HBox(row))
    section_list.append(widgets.HBox([view.filter_output]))  # NOTE Use "layout={'width': '90vw'}" to widen
    content.append(view.section(OUTPUT_TITLE, section_list))

    # Section: Export (download)
    section_list = []
    section_list.append(widgets.VBox([view.filter_btn_refexp, view.filter_out_export]))
    content.append(view.section(EXPORT_TITLE, section_list))

    return widgets.VBox(content)


def build_visualize_tab():
    '''Create widgets for visualize tab content'''
    content = []
    content.append(view.section(NOTE_TITLE, NOTE_TEXT))
    view.plot_ddn = widgets.Dropdown(options=[EMPTY], value=None, disabled=True)
    view.plot_output = widgets.Output()
    section_list = []

    row = []
    row.append(widgets.HTML(value=PLOT_LABEL))
    row.append(widgets.Label(value='', layout=widgets.Layout(width='60%')))  # Cheat: spacer
    section_list.append(widgets.HBox(row))
    section_list.append(view.plot_ddn)
    section_list.append(view.plot_output)
    content.append(view.section(PLOT_TITLE, section_list))

    return widgets.VBox(content)


def build_settings_tab():
    """Create widgets for settings tab."""
    view.theme = widgets.Dropdown(description=THEME, options=THEMES)
    view.context = widgets.Dropdown(description=CONTEXT, options=CONTEXTS)
    view.fscale = widgets.FloatSlider(description=FONT_SCALE, value=1.4)
    view.spines = widgets.Checkbox(description=SPINES, value=False)
    view.gridlines = widgets.Text(description=GRIDLINES, value='--')
    view.ticks = widgets.Checkbox(description=TICKS, value=True)
    view.grid = widgets.Checkbox(description=GRID, value=False)
    view.figsize1 = widgets.FloatSlider(description=FIG_WIDTH, value=6)
    view.figsize2 = widgets.FloatSlider(description=FIG_HEIGHT, value=4.5)
    view.apply = widgets.Button(description=APPLY)

    return(view.section(PLOT_SETTINGS_SECTION_TITLE,
                        [view.theme, view.context, view.fscale, view.spines, view.gridlines,
                            view.ticks, view.grid, view.figsize1, view.figsize2, view.apply]))


def set_no_data():
    """Indicate there are no results."""
    # NOTE While the other view methods build the UI, this one acts an example of a helper method

    with view.filter_output:
        clear_output(wait=True)
        display(widgets.HTML(NO_DATA_MSG))
