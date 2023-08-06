/*!
 * Copyright (c) 2012 - 2021, Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */
(function(root, factory) {
  factory(root["Bokeh"], undefined);
})(this, function(Bokeh, version) {
  var define;
  return (function(modules, entry, aliases, externals) {
    const bokeh = typeof Bokeh !== "undefined" && (version != null ? Bokeh[version] : Bokeh);
    if (bokeh != null) {
      return bokeh.register_plugin(modules, entry, aliases);
    } else {
      throw new Error("Cannot find Bokeh " + version + ". You have to load it prior to loading plugins.");
    }
  })
({
"b5bf9b8817": /* index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const tslib_1 = require("tslib");
    const VizModels = tslib_1.__importStar(require("88dea9ae8f") /* ./visualizer/models/index */);
    exports.VizModels = VizModels;
    const base_1 = require("@bokehjs/base");
    base_1.register_models(VizModels);
},
"88dea9ae8f": /* visualizer\models\index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    var offset_log_color_mapper_1 = require("31d02535b8") /* ./offset_log_color_mapper */;
    __esExport("OffsetLogColorMapper", offset_log_color_mapper_1.OffsetLogColorMapper);
    var offset_log_tick_formatter_1 = require("3571f5e394") /* ./offset_log_tick_formatter */;
    __esExport("OffsetLogTickFormatter", offset_log_tick_formatter_1.OffsetLogTickFormatter);
    var throttled_slider_1 = require("c7269ba5d4") /* ./throttled_slider */;
    __esExport("ThrottledSlider", throttled_slider_1.ThrottledSlider);
    var filetree_1 = require("342f084289") /* ./filetree */;
    __esExport("Tree", filetree_1.Tree);
},
"31d02535b8": /* visualizer\models\offset_log_color_mapper.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const log_color_mapper_1 = require("@bokehjs/models/mappers/log_color_mapper");
    const arrayable_1 = require("@bokehjs/core/util/arrayable");
    class OffsetLogColorMapper extends log_color_mapper_1.LogColorMapper {
        constructor(attrs) {
            super(attrs);
        }
        static init_OffsetLogColorMapper() {
            this.define(({ Array, Number }) => ({
                log_span: [Array(Number), [1, 10]],
            }));
        }
        scan(data, n) {
            // retrieve specified low and high or calculate it if unspecified
            let low = this.low != null ? this.low : arrayable_1.min(data);
            let high = this.high != null ? this.high : arrayable_1.max(data);
            let span = this.log_span != null ? this.log_span : [1, 10];
            const interval = [low, high];
            // n: Palette-size
            const scale = n / (Math.log(span[1]) - Math.log(span[0]));
            return { max: span[1], min: span[0], scale, interval };
        }
        cmap(d, palette, low_color, high_color, scan_data) {
            const max_key = palette.length - 1;
            let _max = scan_data.max;
            let _min = scan_data.min;
            let interval = scan_data.interval;
            // mapping our interval [_min, _max] onto the logspan [interval[0], interval[1]]
            // https://math.stackexchange.com/a/914843
            d = _min + (_max - _min) / (interval[1] - interval[0]) * (d - interval[0]);
            if (d > _max) {
                return high_color;
            }
            // This handles the edge case where d == high, since the code below maps
            // values exactly equal to high to palette.length, which is greater than
            // max_key
            if (d == _max) {
                return palette[max_key];
            }
            else if (d < _min) {
                return low_color;
            }
            // Get the palette-color key by calculating the log of the
            // to-be-colormapped value and multiplying it by the scale
            const log = Math.log(d) - Math.log(_min); // subtract the low offset
            let key = Math.floor(log * scan_data.scale);
            // Deal with upper bound
            if (key > max_key) {
                key = max_key;
            }
            return palette[key];
        }
    }
    exports.OffsetLogColorMapper = OffsetLogColorMapper;
    OffsetLogColorMapper.__name__ = "OffsetLogColorMapper";
    OffsetLogColorMapper.__module__ = "pyscivis.visualizer.models.offset_log_color_mapper";
    OffsetLogColorMapper.init_OffsetLogColorMapper();
},
"3571f5e394": /* visualizer\models\offset_log_tick_formatter.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const log_tick_formatter_1 = require("@bokehjs/models/formatters/log_tick_formatter");
    const arrayable_1 = require("@bokehjs/core/util/arrayable");
    class OffsetLogTickFormatter extends log_tick_formatter_1.LogTickFormatter {
        constructor(attrs) {
            super(attrs);
        }
        static init_OffsetLogTickFormatter() {
            this.define(({ Array, Number }) => ({
                low: [Number, 0],
                high: [Number, 0],
                log_span: [Array(Number), [1, 10]]
            }));
        }
        format_graphics(ticks, opts) {
            if (ticks.length == 0)
                return [];
            const start = arrayable_1.min(this.log_span);
            const end = arrayable_1.max(this.log_span);
            ticks = ticks.map((value) => {
                return this.low + (this.high - this.low) / (end - start) * (value - start);
            });
            return this.basic_formatter.format_graphics(ticks, opts);
        }
    }
    exports.OffsetLogTickFormatter = OffsetLogTickFormatter;
    OffsetLogTickFormatter.__name__ = "OffsetLogTickFormatter";
    OffsetLogTickFormatter.__module__ = "pyscivis.visualizer.models.offset_log_tick_formatter";
    OffsetLogTickFormatter.init_OffsetLogTickFormatter();
},
"c7269ba5d4": /* visualizer\models\throttled_slider.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const slider_1 = require("@bokehjs/models/widgets/slider");
    class ThrottledSlider extends slider_1.Slider {
    }
    exports.ThrottledSlider = ThrottledSlider;
    ThrottledSlider.__name__ = "ThrottledSlider";
    ThrottledSlider.__module__ = "pyscivis.visualizer.models.throttled_slider";
},
"342f084289": /* visualizer\models\filetree.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const widget_1 = require("@bokehjs/models/widgets/widget");
    class TreeView extends widget_1.WidgetView {
        render() {
            $(this.el)
                .on('select_node.jstree', (_e, data) => {
                // Only returns the name if it is a leaf (is in leaf_types)
                // Only 1 Leaf can be selected max -> selected[0]
                var selected_node = data.instance.get_node(data.selected[0]);
                var leaf_types = ["images", "header", "acquisitions"];
                if (leaf_types.includes(selected_node.type)) {
                    this.model.selected = [selected_node.parent, selected_node.id, selected_node.type];
                }
            })
                .on('loaded.jstree', () => {
                $(this.el).jstree('open_all');
            })
                .jstree(this.get_data());
        }
        get_data() {
            return {
                "types": {
                    "images": {
                        "valid_children": "none",
                        "icon": "glyphicon glyphicon-picture",
                    },
                    "acquisitions": {
                        "valid_children": "none",
                        "icon": "glyphicon glyphicon-list"
                    },
                    "header": {
                        "valid_children": "none",
                        "icon": "glyphicon glyphicon-file"
                    },
                    "container": {
                        "valid_children": ["folder", "image", "acquisition", "header"],
                        "icon": "glyphicon glyphicon-folder-open"
                    },
                    "file": {
                        "valid_children": ["folder", "image", "acquisition", "header"],
                        "icon": "glyphicon glyphicon-hdd"
                    },
                    "default": {
                        "valid_children": ["folder", "image", "acquisition", "header"],
                        "icon": "glyphicon glyphicon-question-sign"
                    }
                },
                'core': {
                    'multiple': false,
                    'data': this.model.tree,
                    'themes': {
                        'name': this.model.theme == "dark" ? "default-dark" : "default",
                        "dots": true,
                        "icons": true
                    }
                },
                "plugins": ["types"],
            };
        }
    }
    exports.TreeView = TreeView;
    TreeView.__name__ = "TreeView";
    class Tree extends widget_1.Widget {
        constructor(attrs) {
            super(attrs);
        }
        static init_Tree() {
            this.prototype.default_view = TreeView;
            this.define(({ Tuple, String, Any }) => ({
                selected: [Tuple(String, String, String)],
                theme: [String],
                tree: [Any],
            }));
        }
    }
    exports.Tree = Tree;
    Tree.__name__ = "Tree";
    Tree.__module__ = "pyscivis.visualizer.models.filetree";
    Tree.init_Tree();
},
}, "b5bf9b8817", {"index":"b5bf9b8817","visualizer/models/index":"88dea9ae8f","visualizer/models/offset_log_color_mapper":"31d02535b8","visualizer/models/offset_log_tick_formatter":"3571f5e394","visualizer/models/throttled_slider":"c7269ba5d4","visualizer/models/filetree":"342f084289"}, {});});
//# sourceMappingURL=pyscivis.js.map
