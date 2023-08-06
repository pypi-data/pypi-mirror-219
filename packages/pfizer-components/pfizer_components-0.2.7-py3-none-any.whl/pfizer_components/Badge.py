import dash_bootstrap_components as dbc

normal_style = {'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': '700', 'font-size': '13px',
                'line-height': '18px', 'text-align': 'center', 'letter-spacing': '-0.5px', 'color': '#FFFFFF'}


class Badge(dbc.Badge):
    """A Badge component.
    Badges can be used to add counts or labels to other components.

    Keyword arguments:

        - children (a list of or a singular dash component, string or number; optional):
            The children of this component.

        - id (string; optional):
            The ID of this component, used to identify dash components in
            callbacks. The ID needs to be unique across all of the components
            in an app.

        - className (string; optional):
            **DEPRECATED** Use `class_name` instead.  Often used with CSS to
            style elements with common properties.

        - class_name (string; optional):
            Often used with CSS to style elements with common properties.

        - color (string; default 'secondary'):
            Badge color, options: primary, secondary, success, info, warning,
            danger, link or any valid CSS color of your choice (e.g. a hex
            code, a decimal code or a CSS color name) Default: secondary.

        - external_link (boolean; optional):
            If True, the browser will treat this as an external link, forcing
            a page refresh at the new location. If False, this just changes
            the location without triggering a page refresh. Use this if you
            are observing dcc.Location, for instance. Defaults to True for
            absolute URLs and False otherwise.

        - href (string; optional):
            Attach link to badge.

        - key (string; optional):
            A unique identifier for the component, used to improve performance
            by React.js while rendering components See
            https://reactjs.org/docs/lists-and-keys.html for more info.

        - loading_state (dict; optional):
            Object that holds the loading state object coming from
            dash-renderer.

            `loading_state` is a dict with keys:

            - component_name (string; optional):
                Holds the name of the component that is loading.

            - is_loading (boolean; optional):
                Determines if the component is loading or not.

            - prop_name (string; optional):
                Holds which property is loading.

        - n_clicks (number; default 0):
            An integer that represents the number of times that this element
            has been clicked on.

        - n_clicks_timestamp (number; default -1):
            An integer that represents the time (in ms since 1970) at which
            n_clicks changed. This can be used to tell which button was
            changed most recently.

        - pill (boolean; optional):
            Make badge \"pill\" shaped (rounded ends, like a pill). Default:
            False.

        - style (dict; optional):
            Defines CSS styles which will override styles previously set.

        - tag (string; optional):
            HTML tag to use for the Badge. Default: span.

        - target (string; optional):
            Target attribute to pass on to the link. Only applies to external
            links.

        - text_color (string; optional):
            Badge color, options: primary, secondary, success, info, warning,
            danger, link or any valid CSS color of your choice (e.g. a hex
            code, a decimal code or a CSS color name) Default: secondary.

        - title (string; optional):
            Sets the title attribute of the underlying HTML button."""

    def __init__(self, children=None, **badge_props):
        badge_props = badge_props.copy() if badge_props else {}
        style = badge_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        badge_props['style'] = default_style
        super().__init__(children=children, **badge_props)


class NormalStyle(Badge):
    """
    Class representing the 'NormalStyle' style.

    Style:
        - font-family: Noto Sans
        - font-style: normal
        - font-weight: 700
        - font-size: 13px,
        - line-height: 18px
        - text-align: center
        - letter-spacing: -0.5px
        - color: #FFFFFF
    """

    def __init__(self, children=None, **badge_props):
        badge_props = badge_props.copy() if badge_props else {}
        style = badge_props.pop('style', None)
        default_style = normal_style
        if style is not None:
            default_style.update(style)
        badge_props['style'] = default_style
        super().__init__(children=children, **badge_props)
