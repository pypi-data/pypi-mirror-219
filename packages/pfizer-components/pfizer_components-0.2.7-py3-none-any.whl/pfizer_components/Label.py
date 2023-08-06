from dash import html

Font_style = {'font-family': 'Noto Sans', 'padding': '5px'}


class Label(html.Label):
    """A Label component.
    A component for adding labels to inputs in forms with added sizing controls.

    Keyword arguments:

        - children (a list of or a singular dash component, string or number; optional):
            The children of this component.

        - id (string; optional):
            The ID of this component, used to identify dash components in
            callbacks. The ID needs to be unique across all of the components
            in an app.

        - align (a value equal to: 'start', 'center', 'end'; default 'center'):
            Set vertical alignment of the label, options: 'start', 'center',
            'end', default: 'center'.

        - check (boolean; optional):
            Set to True when using to label a Checkbox or RadioButton.

        - className (string; optional):
            **DEPRECATED** Use `class_name` instead.  Often used with CSS to
            style elements with common properties.

        - class_name (string; optional):
            Often used with CSS to style elements with common properties.

        - color (string; optional):
            Text color, options: primary, secondary, success, warning, danger,
            info, muted, light, dark, body, white, black-50, white-50 or any
            valid CSS color of your choice (e.g. a hex code, a decimal code or
            a CSS color name).

        - hidden (boolean; optional):
            Hide label from UI, but allow it to be discovered by
            screen-readers.

        - html_for (string; optional):
            Set the `for` attribute of the label to bind it to a particular
            element.

        - key (string; optional):
            A unique identifier for the component, used to improve performance
            by React.js while rendering components See
            https://reactjs.org/docs/lists-and-keys.html for more info.

        - lg (optional):
            Specify label width on a large screen  Valid arguments are
            boolean, an integer in the range 1-12 inclusive, or a dictionary
            with keys 'offset', 'order', 'size'. See the documentation for
            more details.

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

        - md (optional):
            Specify label width on a medium screen  Valid arguments are
            boolean, an integer in the range 1-12 inclusive, or a dictionary
            with keys 'offset', 'order', 'size'. See the documentation for
            more details.

        - size (string; optional):
            Set size of label. Options 'sm', 'md' (default) or 'lg'.

        - sm (optional):
            Specify label width on a small screen  Valid arguments are
            boolean, an integer in the range 1-12 inclusive, or a dictionary
            with keys 'offset', 'order', 'size'. See the documentation for
            more details.

        - style (dict; optional):
            Defines CSS styles which will override styles previously set.

        - width (optional):
            Specify width of label for use in grid layouts. Accepts the same
            values as the Col component.

        - xl (optional):
            Specify label width on an extra large screen  Valid arguments are
            boolean, an integer in the range 1-12 inclusive, or a dictionary
            with keys 'offset', 'order', 'size'. See the documentation for
            more details.

        - xs (optional):
            Specify label width on extra small screen  Valid arguments are
            boolean, an integer in the range 1-12 inclusive, or a dictionary
            with keys 'offset', 'order', 'size'. See the documentation for
            more details."""

    def __init__(self, children=None, **label_props):
        label_props = label_props.copy() if label_props else {}
        style = label_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        label_props['style'] = default_style
        super().__init__(children=children, **label_props)


class FontStyle(Label):
    """
    Class representing the 'FontStyle' style.

    Style:
        - font-family: Noto Sans
        - padding: 5px
    """

    def __init__(self, children=None, **label_props):
        label_props = label_props.copy() if label_props else {}
        style = label_props.pop('style', None)
        default_style = Font_style
        if style is not None:
            default_style.update(style)
        label_props['style'] = default_style
        super().__init__(children=children, **label_props)

