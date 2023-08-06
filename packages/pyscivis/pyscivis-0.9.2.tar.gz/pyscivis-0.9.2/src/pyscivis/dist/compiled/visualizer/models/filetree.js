import { Widget, WidgetView } from "@bokehjs/models/widgets/widget";
export class TreeView extends WidgetView {
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
TreeView.__name__ = "TreeView";
export class Tree extends Widget {
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
Tree.__name__ = "Tree";
Tree.__module__ = "pyscivis.visualizer.models.filetree";
Tree.init_Tree();
//# sourceMappingURL=filetree.js.map