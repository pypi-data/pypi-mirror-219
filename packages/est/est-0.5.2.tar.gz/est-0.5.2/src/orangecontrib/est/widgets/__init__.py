import sysconfig

# Category metadata.

# Category icon show in the menu
ICON = "icons/icon.png"

# Background color for category background in menu
# and widget icon background in workflow.
BACKGROUND = "light-green"

URL = "https://gitlab.esrf.fr/workflow/est"

WIDGET_HELP_PATH = (
    # Used for development.
    # You still need to build help pages using
    # make htmlhelp
    # inside doc folder
    ("{DEVELOP_ROOT}/build/sphinx/htmlhelp/index.html", None),
    #
    # Documentation included in wheel
    # Correct DATA_FILES entry is needed in setup.py and documentation has to be built
    # # before the wheel is created.
    ("{}/help/est/index.html".format(sysconfig.get_path("data")), None),
    ("http://www.silx.org/pub/doc/est/.htmlhelp/latest/", ""),
)


# Entry point for main Orange categories/widgets discovery
def widget_discovery(discovery):
    import pkg_resources

    dist = pkg_resources.get_distribution("est")
    pkgs = [
        "orangecontrib.est.widgets.pymca",
        "orangecontrib.est.widgets.larch",
        "orangecontrib.est.widgets.utils",
    ]
    for pkg in pkgs:
        discovery.process_category_package(pkg, distribution=dist)
