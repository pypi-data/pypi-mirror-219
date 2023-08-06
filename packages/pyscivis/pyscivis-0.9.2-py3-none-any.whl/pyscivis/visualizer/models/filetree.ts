
import {Widget, WidgetView} from "@bokehjs/models/widgets/widget"
import * as p from "@bokehjs/core/properties"


// declaring jquery shorthand to allow future referencing
declare function $(...args: any[]): any
export class TreeView extends WidgetView {
  model: Tree

 render(): void {
    $(this.el)
        .on('select_node.jstree', (_e: any, data: any) => {
            // Only returns the name if it is a leaf (is in leaf_types)
            // Only 1 Leaf can be selected max -> selected[0]
            var selected_node = data.instance.get_node(data.selected[0])
            var leaf_types = ["images", "header", "acquisitions"]
            if(leaf_types.includes(selected_node.type)){
                this.model.selected = [selected_node.parent, selected_node.id, selected_node.type]
            }
        })
        .on('loaded.jstree', ()=> {
            $(this.el).jstree('open_all')
        })
        .jstree(this.get_data())

  }


  get_data(): any {
    return {
        "types" : {
            "images" : { // image leaf
                "valid_children" : "none",
                "icon" : "glyphicon glyphicon-picture",
            },
            "acquisitions" : { // aquisition leaf
                "valid_children" : "none",
                "icon" : "glyphicon glyphicon-list"
            },
            "header" : { // header leaf
                "valid_children" : "none",
                "icon" : "glyphicon glyphicon-file"
            },
            "container" : { // container node
                "valid_children" : ["folder", "image", "acquisition", "header"],
                "icon" : "glyphicon glyphicon-folder-open"
            },
            "file" : { // root node
                "valid_children" : ["folder", "image", "acquisition", "header"],
                "icon" : "glyphicon glyphicon-hdd"
            },
            "default" : { // unknown
                "valid_children" : ["folder", "image", "acquisition", "header"],
                "icon" : "glyphicon glyphicon-question-sign"
            }
        },
        'core' :
            {
            'multiple': false,  // Forbids multi-selection (using shift)
            'data' : this.model.tree,
            'themes': {
                'name': this.model.theme=="dark"? "default-dark" : "default",
                "dots": true,
                "icons": true
            }

        },
        "plugins" : ["types"],
    }
  }
}

export namespace Tree {
  export type Attrs = p.AttrsOf<Props>

  export type Props = Widget.Props & {
    selected: p.Property<[string, string, string]>
    theme: p.Property<string>
    tree: p.Property<any[]>
  }
}

export interface Tree extends Tree.Attrs {}

export class Tree extends Widget {
  properties: Tree.Props
  __view_type__: TreeView

  static __module__ = "pyscivis.visualizer.models.filetree"

  constructor(attrs?: Partial<Tree.Attrs>) {
    super(attrs)
  }

  static init_Tree() {
    this.prototype.default_view = TreeView

    this.define<Tree.Props>(({Tuple, String, Any}) => ({
      selected:     [ Tuple(String, String, String) ],
      theme:        [ String ],
      tree:         [ Any ],
    }))
  }
}
