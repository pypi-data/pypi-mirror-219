from dash import dcc
import plotly.graph_objs as go

graph_1_extra_large = {
    "width": "1140px",
    "height": "476px",
    "background": "#FFFFFF",
}

graph_1_large = {
    "width": "960px",
    "height": "401px",
    "background": "#FFFFFF",
}

graph_1_medium = {
    "width": "720px",
    "height": "358px",
    "background": "#FFFFFF",
}

graph_2_extra_large = {
    "width": "848px",
    "height": "524px",
    "background": "#FFFFFF",
}

graph_2_large = {
    "width": "960px",
    "height": "575px",
    "background": "#FFFFFF",
}

graph_2_medium = {
    "width": "720px",
    "height": "447px",
    "background": "#FFFFFF",
}

categorical_color_palette_1 = ["#0084D0", "#00A6DE", "#00C4D0", "#00DCAD", "#97EF86", "#F9F871", "#4D7AD0", "#756DC9", "#955EBA", "#AE4CA5", "#79EEE2", "#C0398A", "#64B9FF", "#DAF3FF", "#DF9F1F", "#FFEDCB", "#897456", "#3D4856", "#A1ACBD", "#C65A83"]

categorical_color_palette_2 = ["#005977", "#008DA1", "#1CC4B9", "#81F9BF", "#B9D3DE", "#98E2E9", "#7DEFDD", "#86F9BC", "#f1ea8f", "#FFDA86", "#FFC989", "#FFB897", "#4e5858", "#588C83", "#6AC1A1", "#94F7B2", "#54284f", "#566AA8", "#00B3E9", "#00FCFC"]

categorical_color_palette_3 = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"]

categorical_color_palette_4 = ["#A49592", "#FFCCBB", "#6EB5C0", "#006C84", "#E2E8E4", "#FCC875", "#BAA896", "#E6CCB5", "#E38B75", "#2F3131", "#F8F1E5", "#426E86", "#2988BC"]

categorical_color_palette_5 = ["#252b69", "#515587", "#157dbc", "#639ccb", "#75787b", "#919395", "#d9ab28", "#ce1f3a", "#2d2926"]

categorical_color_palette_6 = ["#A49592", "#FBCD4B", "#335252", "#AA4B41", "#2D3033", "#524A3A", "#919636", "#5A5F37", "#E5E2CA", "#DDBC95", "#52958b", "#32384D"]

categorical_color_palette_7 = ["#A49592", "#626D71", "#CDCDC0", "#DDBC95", "#B38867", "#F69454", "#FBCB7B", "#F9A603", "#A1BE95", "#E2DFA2", "#92AAC7", "#ED5752", "#AF4425", "#662E1C", "#EBDCB2", "#C9A66B", "#C1E1DC", "#FFCCAC", "#FFEB94", "#FDD475"]

categorical_color_palette_8 = ["#0084d0", "#48A7DD", "#90C9EB", "#D8ECF8"]

categorical_color_palette_9 = ["#0084d0", "#00A6DE", "#35b4e4", "#00CAE2", "#d8ecf8", "#B7F5FF", "#8a8c8f", "#81A5B4"]

categorical_color_palette_10 = ["#005977", "#3E8299", "#7BAABC", "#B9D3DE"]

categorical_color_palette_11 = ["#005977", "#007D91", "#B9D3DE", "#9FE1E7", "#f1ea8f", "#A5D08C", "#4e5858", "#a6bcaf"]

categorical_color_palette_12 = ['#005977', '#17809c', '#b9d3de', '#bbdaed', '#f1ea8f', '#54284f', '#4e5858', '#a6bcaf']

categorical_color_palette_13 = ['#005977', '#17809c', '#b9d3de', '#f1ea8f', '#4e5858', '#a6bcaf', '#54284f', '#796497', '#B594E4', '#DFD1F4']

categorical_color_palette_14 = ['#E99787', '#67BACA', '#A5C05B', '#DBAE58', '#688B8A', '#A57C65', '#6EB5C0', '#FCC875', '#E2DFA2', '#A1BE95', '#5BC8AC', '#68829E', '#AEBD38', '#EED8C9', '#727077', '#B66353', '#90728F', '#BB7693', '#B6992D', '#79706E']

categorical_color_palette_15 = ['#796497', '#B594E4', '#918A44', '#B5AC55', '#999999', '#C5C5C5', '#EFE8F9', '#9A9EAB', '#5D535E', '#EC96A4', '#DFE166', '#75B1A9', '#D9B44A', '#4F6457', '#ACD0C0', '#F1F1F2', '#BCBABE', '#A1D6E2', '#1995AD', '#1b9e77']

categorical_color_palette_16 = ['#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666', '#F4CC70', '#DE7A22', '#20948B', '#6AB187', '#FFCCBB', '#6EB5C0', '#006C84', '#E2E8E4', '#FCC875', '#BAA896', '#E6CCB5', '#E38B75', '#2F3131']

categorical_color_palette_17 = ['#796497', '#B594E4', '#DFD1F4', '#918A44', '#B5AC55', '#D9CF66', '#E9E4A8', '#999999', '#C5C5C5', '#EFE8F9']

categorical_color_palette_18 = ['#A49592', '#488a99', '#DBAE58', '#FBE9E7', '#B4B4B4', '#DDDEDE', '#232122', '#A5C05B', '#7BA4A8', '#E4535E', '#E38533', '#1B4B5A', '#0F1F38', '#F55449', '#FFBEBD', '#FCFCFA', '#337BAE', '#1A405F', '#88A550', '#A3A599']

categorical_color_palette_19 = ['#4C3F54', '#D13525', '#F2C057', '#486824', '#FD974F', '#805A3B', '#EAE2D6', '#D5C3AA', '#867666', '#E1B80D', '#B6452C']

categorical_color_palette_20 = ['#A49592', '#2988BC', '#2F496E', '#F4EADE', '#ED8C72', '#000B29', '#D70026', '#F8F5F2', '#EDB83D', '#F9BA32', '#426E86', '#F8F1E5', '#04202C', '#304040', '#5B7065', '#C9D1C8', '#217CA3', '#E29930', '#32384D']

categorical_color_palette_21 = ['#211F30', '#004D47', '#52958b', '#B9C4C9', '#506D2F', '#2A2922', '#F3EBDD', '#7D5642', '#F47D4A', '#E1315B', '#FFE5C5', '#B6452C']

categorical_color_palette_22 = ['#A49592', '#E99787', '#67BACA', '#A5C05B', '#DBAE58', '#688B8A', '#A57C65', '#6EB5C0', '#FCC875', '#E2DFA2', '#A1BE95', '#5BC8AC', '#68829E', '#AEBD38', '#EED8C9', '#727077', '#B66353', '#90728F', '#BB7693', '#B6992D', '#79706E']

categorical_color_palette_23 = ['#A49592', '#9A9EAB', '#5D535E', '#EC96A4', '#DFE166']

categorical_color_palette_24 = ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0', '#f0027f', '#bf5b17', '#666666']

categorical_color_palette_25 = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999']

categorical_color_palette_26 = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3']

categorical_color_palette_27 = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f]']

fresh_bright = ['#A49592', '#F98866', '#FF420E', '#80BD9E', '#89DA59']

subdued_professional = ['#A49592', '#90AFC5', '#336B87', '#2A3132', '#763626']

smoky_purples = ['#A49592', '#A49592', '#727077', '#EED8C9', '#E99787']

dark_earthy = ['#A49592', '#46211A', '#693D3D', '#BA5536', '#A43820']

crisp_dramatic = ['#A49592', '#505160', '#68829E', '#AEBD38', '#598234']

refreshing_pretty = ['#A49592', '#98DBC6', '#5BC8AC', '#E6D72A', '#F18D9E']

playful_greens_blues = ['#A49592', '#324851', '#86AC41', '#34675C', '#7DA3A1']

fresh_energetic = ['#A49592', '#4CB5F5', '#B7B8B6', '#34675C', '#B3C100']

surf_turf = ['#A49592', '#F4CC70', '#DE7A22', '#20948B', '#6AB187']

autumn_vermont = ['#A49592', '#8D230F', '#1E434C', '#9B4F0F', '#C99E10']

icy_blues = ['#A49592', '#F1F1F2', '#BCBABE', '#A1D6E2', '#1995AD']

birds_berries = ['#A49592', '#9A9EAB', '#5D535E', '#EC96A4', '#DFE166', '#75B1A9', '#D9B44A', '#4F6457', '#ACD0C0']

warm_naturals_1 = ['#A49592', '#2E2300', '#6E6702', '#C05805', '#DB9501']

warm_naturals_2 = ['#A49592', '#2E2300', '#6E6702', '#C05805', '#DB9501']

muted_classy = ['#A49592', '#2E2300', '#6E6702', '#C05805', '#DB9501']

dark_naturals = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666']

pastels_1 = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc', '#e5d8bd', '#fddaec', '#f2f2f2']

pastels_2 = ['#b3e2cd', '#fdcdac', '#cbd5e8', '#f4cae4', '#e6f5c9', '#fff2ae', '#f1e2cc', '#cccccc']

sequential_grey = ['#ffffff', '#f0f0f0', '#d9d9d9', '#bdbdbd', '#969696', '#737373', '#525252', '#252525', '#000000']

sequential_red = ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d']

sequential_blue = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b']

sequential_bu_gn = ['#f7fcfd', '#e5f5f9', '#ccece6', '#99d8c9', '#66c2a4', '#41ae76', '#238b45', '#006d2c', '#00441b']

sequential_bu_pu = ['#f7fcfd', '#e0ecf4', '#bfd3e6', '#9ebcda', '#8c96c6', '#8c6bb1', '#88419d', '#810f7c', '#4d004b']

sequential_pu_bu_gn = ['#fff7fb', '#ece2f0', '#d0d1e6', '#a6bddb', '#67a9cf', '#3690c0', '#02818a', '#016c59', '#014636']

sequential_green = ['#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#006d2c', '#00441b']

sequential_orange = ['#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#a63603', '#7f2704']

sequential_purple = ['#fcfbfd', '#efedf5', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#54278f', '#3f007d']

sequential_gn_bu = ['#f7fcf0', '#e0f3db', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3', '#2b8cbe', '#0868ac', '#084081']

sequential_palette_11 = ['#fff7ec', '#fee8c8', '#fdd49e', '#fdbb84', '#fc8d59', '#ef6548', '#d7301f', '#b30000', '#7f0000']

sequential_palette_12 = ['#f7f4f9', '#e7e1ef', '#d4b9da', '#c994c7', '#df65b0', '#e7298a', '#ce1256', '#980043', '#67001f']

diverging_palette_1 = ['#fde725', '#dde318', '#bade28', '#95d840', '#75d054', '#56c667', '#3dbc74', '#29af7f', '#20a386', '#1f968b', '#238a8d', '#287d8e', '#2d718e', '#33638d', '#39558c', '#404688', '#453781', '#482576', '#481467', '#440154']

diverging_palette_2 = ['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850', '#006837']

diverging_palette_3 = ['#ffffd9', '#edf8b1', '#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#253494', '#081d58']

diverging_palette_4 = ['#ffffe5', '#f7fcb9', '#d9f0a3', '#addd8e', '#78c679', '#41ab5d', '#238443', '#006837', '#004529']

diverging_palette_5 = ['#fcfdbf', '#fde5a7', '#fecd90', '#feb47b', '#fd9b6b', '#fa815f', '#f4695c', '#e85362', '#d6456c', '#c03a76', '#ab337c', '#942c80', '#802582', '#6a1c81', '#56147d', '#3f0f72', '#29115a', '#150e38', '#07061c', '#000004']

diverging_palette_6 = ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026']

diverging_palette_7 = ['#fcffa4', '#f1ed71', '#f6d543', '#fbba1f', '#fca108', '#f8870e', '#f1711f', '#e55c30', '#d74b3f', '#c43c4e', '#b132']

diverging_color_palette_8 = [
    "#f0f921", "#f7e225", "#fccd25", "#feb72d", "#fca338", "#f79044", "#f07f4f",
    "#e76e5b", "#dd5e66", "#d14e72", "#c5407e", "#b6308b", "#a72197", "#9511a1",
    "#8305a7", "#6e00a8", "#5901a5", "#43039e", "#2c0594", "#0d0887"
]

diverging_color_palette_9 = [
    "#87acd2", "#92cf89", "#f2e288", "#f88a8c", "#b191a9", "#ffffff"
]

diverging_color_palette_10 = [
    "#67001f", "#b2182b", "#d6604d", "#f4a582", "#fddbc7", "#f7f7f7", "#d1e5f0",
    "#92c5de", "#4393c3", "#2166ac", "#053061"
]

diverging_color_palette_11 = [
    "#67001f", "#b2182b", "#d6604d", "#f4a582", "#fddbc7", "#ffffff", "#e0e0e0",
    "#bababa", "#878787", "#4d4d4d", "#1a1a1a"
]

diverging_color_palette_12 = [
    "#fff7f3", "#fde0dd", "#fcc5c0", "#fa9fb5", "#f768a1", "#dd3497", "#ae017e",
    "#7a0177", "#49006a"
]

diverging_color_palette_13 = [
    "#a50026", "#d73027", "#f46d43", "#fdae61", "#fee090", "#ffffbf", "#e0f3f8",
    "#abd9e9", "#74add1", "#4575b4", "#313695"
]

diverging_color_palette_14 = [
    "#ffffe5", "#fff7bc", "#fee391", "#fec44f", "#fe9929", "#ec7014", "#cc4c02",
    "#993404", "#662506"
]

diverging_color_palette_15 = [
    "#9e0142", "#d53e4f", "#f46d43", "#fdae61", "#fee08b", "#ffffbf", "#e6f598",
    "#abdda4", "#66c2a5", "#3288bd", "#5e4fa2"
]

diverging_color_palette_16 = [
    "#543005", "#8c510a", "#bf812d", "#dfc27d", "#f6e8c3", "#f5f5f5", "#c7eae5",
    "#80cdc1", "#35978f", "#01665e", "#003c30"
]

diverging_color_palette_17 = [
    "#40004b", "#762a83", "#9970ab", "#c2a5cf", "#e7d4e8", "#f7f7f7", "#d9f0d3",
    "#a6dba0", "#5aae61", "#1b7837", "#00441b"
]

diverging_color_palette_18 = [
    "#8e0152", "#c51b7d", "#de77ae", "#f1b6da", "#fde0ef",
    "#f7f7f7", "#e6f5d0", "#b8e186", "#7fbc41", "#4d9221", "#276419"
]

diverging_color_palette_19 = [
    "#fff7fb", "#ece7f2", "#d0d1e6", "#a6bddb", "#74a9cf",
    "#3690c0", "#0570b0", "#045a8d", "#023858"
]

diverging_color_palette_20 = [
    "#7f3b08", "#b35806", "#e08214", "#fdb863", "#fee0b6",
    "#f7f7f7", "#d8daeb", "#b2abd2", "#8073ac", "#542788", "#2d004b"
]

custom_colors = categorical_color_palette_1

class Graph(dcc.Graph):
    """A Graph component.
    Graph can be used to render any plotly.js-powered data visualization.

    You can define callbacks based on user interaction with Graphs such as
    hovering, clicking or selecting

    Keyword arguments:

        - id (string; optional):
            The ID of this component, used to identify dash components in
            callbacks. The ID needs to be unique across all of the components
            in an app.

        - animate (boolean; default False):
            Beta: If True, animate between updates using plotly.js's `animate`
            function.

        - animation_options (dict; default {    frame: {        redraw: False,    },    transition: {        duration: 750,        ease: 'cubic-in-out',    },}):
            Beta: Object containing animation settings. Only applies if
            `animate` is `True`.

        - className (string; optional):
            className of the parent div.

        - clear_on_unhover (boolean; default False):
            If True, `clear_on_unhover` will clear the `hoverData` property
            when the user \"unhovers\" from a point. If False, then the
            `hoverData` property will be equal to the data from the last point
            that was hovered over.

        - clickAnnotationData (dict; optional):
            Data from latest click annotation event. Read-only.

        - clickData (dict; optional):
            Data from latest click event. Read-only.

        - config (dict; optional):
            Plotly.js config options. See
            https://plotly.com/javascript/configuration-options/ for more
            info.

            `config` is a dict with keys:

            - autosizable (boolean; optional):
                DO autosize once regardless of layout.autosize (use default
                width or height values otherwise).

            - displayModeBar (a value equal to: true, false, 'hover'; optional):
                Display the mode bar (True, False, or 'hover').

            - displaylogo (boolean; optional):
                Add the plotly logo on the end of the mode bar.

            - doubleClick (a value equal to: false, 'reset', 'autosize', 'reset+autosize'; optional):
                Double click interaction (False, 'reset', 'autosize' or
                'reset+autosize').

            - doubleClickDelay (number; optional):
                Delay for registering a double-click event in ms. The minimum
                value is 100 and the maximum value is 1000. By default this is
                300.

            - editable (boolean; optional):
                We can edit titles, move annotations, etc - sets all pieces of
                `edits` unless a separate `edits` config item overrides
                individual parts.

            - edits (dict; optional):
                A set of editable properties.

                `edits` is a dict with keys:

                - annotationPosition (boolean; optional):
                    The main anchor of the annotation, which is the text (if
                    no arrow) or the arrow (which drags the whole thing
                    leaving the arrow length & direction unchanged).

                - annotationTail (boolean; optional):
                    Just for annotations with arrows, change the length and
                    direction of the arrow.

                - annotationText (boolean; optional)

                - axisTitleText (boolean; optional)

                - colorbarPosition (boolean; optional)

                - colorbarTitleText (boolean; optional)

                - legendPosition (boolean; optional)

                - legendText (boolean; optional):
                    Edit the trace name fields from the legend.

                - shapePosition (boolean; optional)

                - titleText (boolean; optional):
                    The global `layout.title`.

            - fillFrame (boolean; optional):
                If we DO autosize, do we fill the container or the screen?.

            - frameMargins (number; optional):
                If we DO autosize, set the frame margins in percents of plot
                size.

            - linkText (string; optional):
                Text appearing in the sendData link.

            - locale (string; optional):
                The locale to use. Locales may be provided with the plot
                (`locales` below) or by loading them on the page, see:
                https://github.com/plotly/plotly.js/blob/master/dist/README.md#to-include-localization.

            - locales (dict; optional):
                Localization definitions, if you choose to provide them with
                the plot rather than registering them globally.

            - mapboxAccessToken (boolean | number | string | dict | list; optional):
                Mapbox access token (required to plot mapbox trace types) If
                using an Mapbox Atlas server, set this option to '', so that
                plotly.js won't attempt to authenticate to the public Mapbox
                server.

            - modeBarButtons (boolean | number | string | dict | list; optional):
                Fully custom mode bar buttons as nested array, where the outer
                arrays represents button groups, and the inner arrays have
                buttons config objects or names of default buttons.

            - modeBarButtonsToAdd (list; optional):
                Add mode bar button using config objects.

            - modeBarButtonsToRemove (list; optional):
                Remove mode bar button by name. All modebar button names at
                https://github.com/plotly/plotly.js/blob/master/src/components/modebar/buttons.js
                Common names include: sendDataToCloud; (2D) zoom2d, pan2d,
                select2d, lasso2d, zoomIn2d, zoomOut2d, autoScale2d,
                resetScale2d; (Cartesian) hoverClosestCartesian,
                hoverCompareCartesian; (3D) zoom3d, pan3d, orbitRotation,
                tableRotation, handleDrag3d, resetCameraDefault3d,
                resetCameraLastSave3d, hoverClosest3d; (Geo) zoomInGeo,
                zoomOutGeo, resetGeo, hoverClosestGeo; hoverClosestGl2d,
                hoverClosestPie, toggleHover, resetViews.

            - plotGlPixelRatio (number; optional):
                Increase the pixel ratio for Gl plot images.

            - plotlyServerURL (string; optional):
                Base URL for a Plotly cloud instance, if `showSendToCloud` is
                enabled.

            - queueLength (number; optional):
                Set the length of the undo/redo queue.

            - responsive (boolean; optional):
                Whether to change layout size when the window size changes.

            - scrollZoom (boolean; optional):
                Mousewheel or two-finger scroll zooms the plot.

            - sendData (boolean; optional):
                If we show a link, does it contain data or just link to a
                plotly file?.

            - showAxisDragHandles (boolean; optional):
                Enable axis pan/zoom drag handles.

            - showAxisRangeEntryBoxes (boolean; optional):
                Enable direct range entry at the pan/zoom drag points (drag
                handles must be enabled above).

            - showEditInChartStudio (boolean; optional):
                Should we show a modebar button to send this data to a Plotly
                Chart Studio plot. If both this and showSendToCloud are
                selected, only showEditInChartStudio will be honored. By
                default this is False.

            - showLink (boolean; optional):
                Link to open this plot in plotly.

            - showSendToCloud (boolean; optional):
                Should we include a modebar button to send this data to a
                Plotly Cloud instance, linked by `plotlyServerURL`. By default
                this is False.

            - showTips (boolean; optional):
                New users see some hints about interactivity.

            - staticPlot (boolean; optional):
                No interactivity, for export or image generation.

            - toImageButtonOptions (dict; optional):
                Modifications to how the toImage modebar button works.

                `toImageButtonOptions` is a dict with keys:

                - filename (string; optional):
                    The name given to the downloaded file.

                - format (a value equal to: 'jpeg', 'png', 'webp', 'svg'; optional):
                    The file format to create.

                - height (number; optional):
                    Height of the downloaded file, in px.

                - scale (number; optional):
                    Extra resolution to give the file after rendering it with
                    the given width and height.

                - width (number; optional):
                    Width of the downloaded file, in px.

            - topojsonURL (string; optional):
                URL to topojson files used in geo charts.

            - watermark (boolean; optional):
                Add the plotly logo even with no modebar.

        - extendData (list | dict; optional):
            Data that should be appended to existing traces. Has the form
            `[updateData, traceIndices, maxPoints]`, where `updateData` is an
            object containing the data to extend, `traceIndices` (optional) is
            an array of trace indices that should be extended, and `maxPoints`
            (optional) is either an integer defining the maximum number of
            points allowed or an object with key:value pairs matching
            `updateData` Reference the Plotly.extendTraces API for full usage:
            https://plotly.com/javascript/plotlyjs-function-reference/#plotlyextendtraces.

        - figure (dict; default {    data: [],    layout: {},    frames: [],}):
            Plotly `figure` object. See schema:
            https://plotly.com/javascript/reference  `config` is set
            separately by the `config` property.

            `figure` is a dict with keys:

            - data (list of dicts; optional)

            - frames (list of dicts; optional)

            - layout (dict; optional)

        - hoverData (dict; optional):
            Data from latest hover event. Read-only.

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

        - prependData (list | dict; optional):
            Data that should be prepended to existing traces. Has the form
            `[updateData, traceIndices, maxPoints]`, where `updateData` is an
            object containing the data to prepend, `traceIndices` (optional)
            is an array of trace indices that should be prepended, and
            `maxPoints` (optional) is either an integer defining the maximum
            number of points allowed or an object with key:value pairs
            matching `updateData` Reference the Plotly.prependTraces API for
            full usage:
            https://plotly.com/javascript/plotlyjs-function-reference/#plotlyprependtraces.

        - relayoutData (dict; optional):
            Data from latest relayout event which occurs when the user zooms
            or pans on the plot or other layout-level edits. Has the form
            `{<attr string>: <value>}` describing the changes made. Read-only.

        - responsive (a value equal to: true, false, 'auto'; default 'auto'):
            If True, the Plotly.js plot will be fully responsive to window
            resize and parent element resize event. This is achieved by
            overriding `config.responsive` to True, `figure.layout.autosize`
            to True and unsetting `figure.layout.height` and
            `figure.layout.width`. If False, the Plotly.js plot not be
            responsive to window resize and parent element resize event. This
            is achieved by overriding `config.responsive` to False and
            `figure.layout.autosize` to False. If 'auto' (default), the Graph
            will determine if the Plotly.js plot can be made fully responsive
            (True) or not (False) based on the values in `config.responsive`,
            `figure.layout.autosize`, `figure.layout.height`,
            `figure.layout.width`. This is the legacy behavior of the Graph
            component.  Needs to be combined with appropriate dimension /
            styling through the `style` prop to fully take effect.

        - restyleData (list; optional):
            Data from latest restyle event which occurs when the user toggles
            a legend item, changes parcoords selections, or other trace-level
            edits. Has the form `[edits, indices]`, where `edits` is an object
            `{<attr string>: <value>}` describing the changes made, and
            `indices` is an array of trace indices that were edited.
            Read-only.

        - selectedData (dict; optional):
            Data from latest select event. Read-only.

        - style (dict; optional):
            Generic style overrides on the plot div."""
    def __init__(self, custom_colors=custom_colors,**graph_props):
        graph_props = graph_props.copy() if graph_props else {}
        style = graph_props.pop('style', None)
        default_style = {}
        if style is not None:
            default_style.update(style)
        graph_props['style'] = default_style

        data = graph_props['figure']['data']
        data = fetch_color(data,custom_colors)
        graph_props['figure']['data'] = data
        super().__init__(**graph_props)


def fetch_color(data,custom_colors):
    for i, data_point in enumerate(data):
        if isinstance(data_point, go.Scatter):
            if not getattr(data_point.marker, 'color', None):
                if i < len(custom_colors):
                    marker = {'color': custom_colors[i]}
                    data_point.marker = marker
        else:
            if i < len(custom_colors) and not (data_point.get('marker', None)):
                marker = {'color': custom_colors[i]}
                data_point['marker'] = marker
    return data


class Graph1ExtraLarge(Graph):
    """
    Class representing the 'Graph1ExtraLarge' style.

    Style:
        - width: 1140px
        - height: 476px
        - background: #FFFFFF
    """
    def __init__(self, **graph_props):
        style = graph_props.pop('style', None)
        default_style = graph_1_extra_large
        if style is not None:
            default_style.update(style)
        graph_props['style'] = default_style
        data = graph_props['figure']['data']
        data = fetch_color(data,custom_colors)
        graph_props['figure']['data'] = data
        super().__init__(**graph_props)


class GraphLarge(Graph):
    """
    Class representing the 'GraphLarge' style.

    Style:
        - width: 960px
        - height: 401px
        - background: #FFFFFF
    """
    def __init__(self, **graph_props):
        style = graph_props.pop('style', None)
        default_style = graph_1_large
        if style is not None:
            default_style.update(style)
        graph_props['style'] = default_style
        data = graph_props['figure']['data']
        data = fetch_color(data,custom_colors)
        graph_props['figure']['data'] = data
        super().__init__(**graph_props)


class Graph1Medium(Graph):
    """
    Class representing the 'Graph1Medium' style.

    Style:
        - width: 720px
        - height: 358px
        - background: #FFFFFF
    """
    def __init__(self, **graph_props):
        style = graph_props.pop('style', None)
        default_style = graph_1_medium
        if style is not None:
            default_style.update(style)
        graph_props['style'] = default_style
        data = graph_props['figure']['data']
        data = fetch_color(data,custom_colors)
        graph_props['figure']['data'] = data
        super().__init__(**graph_props)


class Graph2ExtraLarge(Graph):
    """
    Class representing the 'Graph2ExtraLarge' style.

    Style:
        - width: 848px
        - height: 524px
        - background: #FFFFFF
    """
    def __init__(self, **graph_props):
        style = graph_props.pop('style', None)
        default_style = graph_2_extra_large
        if style is not None:
            default_style.update(style)
        graph_props['style'] = default_style
        data = graph_props['figure']['data']
        data = fetch_color(data,custom_colors)
        graph_props['figure']['data'] = data
        super().__init__(**graph_props)


class Graph2Large(Graph):
    """
    Class representing the 'Graph2Large' style.

    Style:
        - width: 960px
        - height: 575px
        - background: #FFFFFF
    """
    def __init__(self, **graph_props):
        style = graph_props.pop('style', None)
        default_style = graph_2_large
        if style is not None:
            default_style.update(style)
        graph_props['style'] = default_style
        data = graph_props['figure']['data']
        data = fetch_color(data,custom_colors)
        graph_props['figure']['data'] = data
        super().__init__(**graph_props)


class Graph2Medium(Graph):
    """
    Class representing the 'Graph2Medium' style.

    Style:
        - width: 720px
        - height: 447px
        - background: #FFFFFF
    """
    def __init__(self, **graph_props):
        style = graph_props.pop('style', None)
        default_style = graph_2_medium
        if style is not None:
            default_style.update(style)
        graph_props['style'] = default_style
        data = graph_props['figure']['data']
        data = fetch_color(data,custom_colors)
        graph_props['figure']['data'] = data

        super().__init__(**graph_props)


class Scatter(go.Scatter):
    def __init__(self, **graph_props):
        graph_props = graph_props.copy() if graph_props else {}
        # Confirm which properties to keep by default
        super().__init__(**graph_props)