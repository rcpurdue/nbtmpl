# controller.py - Central logic for app
# rcampbel@purdue.edu - 2020-07-14

import logging
import sys
import traceback
from IPython.display import display, clear_output, FileLink
from jupyterthemes import jtplot
from matplotlib import pyplot as plt

from nb import model
from nb import view
from nb.log import logger, log_handler


ctrl = sys.modules[__name__]


def start(debug=False):
    """Begin running the app."""

    # Optionally show additional info in log
    if debug:
        log_handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    model.start()  # Load data or prepare access to data
    view.start(debug)  # Build user interface (specify "True" to show log under UI)

    # Show data preview
    with view.data_preview_out:
        display(model.data)

    # Setup callbacks
    try:
        # Connect UI widgets to callback methods ("cb_...").
        # These methods will be run when user changes a widget.
        # NOTE "on_click()" connects buttons, "observe()" connects other widgets.
        view.select_btn_apply.on_click(ctrl.when_apply_select)
        view.select_ddn_ndisp.observe(ctrl.when_ndisp_changed, 'value')
        view.select_btn_refexp.on_click(ctrl.when_fill_results_export)
        view.plot_ddn.observe(ctrl.when_plot_type_selected, 'value')
        view.apply.on_click(ctrl.when_apply_plot_settings)
        logger.info('App running')
    except Exception:
        logger.debug('Exception while setting up callbacks...\n'+traceback.format_exc())
        raise


def when_fill_results_export(_):
    """React to user pressing button to download results."""
    try:
        # Create link for select results
        if model.res_count > 0:
            filename = model.create_download_file(model.results, 'csv')

            with view.select_out_export:
                clear_output(wait=True)
                display(FileLink(filename, result_html_prefix=view.EXPORT_LINK_PROMPT))

    except Exception:
        logger.debug('Exception during download creation...\n' + traceback.format_exc())
        raise


def when_apply_select(_):
    """React to apply select button press."""
    try:
        view.select_out_export.clear_output()
        model.clear_selection_results()  # New search attempt so reset
        model.select_data(view.select_txt_startyr.value, view.select_txt_endyr.value)
        ctrl.refresh_select_output()
    except Exception:
        logger.debug('Exception while selecting data...\n'+traceback.format_exc())


def when_ndisp_changed(_):
    """React to user changing result page size."""
    try:
        ctrl.refresh_select_output()
    except Exception:
        logger.debug('Exception while changing number of out lines to display...\n'+traceback.format_exc())


def when_plot_type_selected(_):
    """React to use requesting plot."""
    try:

        if not view.plot_ddn.value == view.EMPTY:
            view.plot_output.clear_output(wait=True)
            # TODO Add ability to download plot as an image

            with view.plot_output:
                plt.plot(model.results[model.headers[0]], model.results[view.plot_ddn.value])
                plt.xlabel(model.headers[0])
                plt.ylabel(view.plot_ddn.value)
                plt.suptitle(view.PLOT_TITLE)
                plt.show()
                logger.debug('Plot finished')
    except Exception:
        logger.debug('Exception while plotting...')
        raise
    finally:
        plt.close()


def when_apply_plot_settings(_):
    """React to user applying settings"""
    try:
        jtplot.style(theme=view.theme.value,
                     context=view.context.value,
                     fscale=view.fscale.value,
                     spines=view.spines.value,
                     gridlines=view.gridlines.value,
                     ticks=view.ticks.value,
                     grid=view.grid.value,
                     figsize=(view.figsize1.value, view.figsize2.value))
    except Exception:
        logger.debug('Exception while applying plot settings...')
        raise


def refresh_select_output():
    """Display select results. Enable/disable plot widget(s)."""

    if model.res_count > 0:

        # Calc set output line limit
        if view.select_ddn_ndisp.value == view.ALL:
            limit = model.res_count
        else:
            limit = int(view.select_ddn_ndisp.value)

        # Display results

        model.set_disp(limit=limit)

        with view.select_output:
            clear_output(wait=True)
            display(model.results.head(limit))

        # Enable plot
        view.plot_ddn.disabled = False
        view.plot_ddn.options = [view.EMPTY]+model.headers[1:]
    else:
        view.set_no_data()  # Show "empty list" msg
        view.plot_ddn.disabled = True
