import { Widget, WidgetView } from "@bokehjs/models/widgets/widget";
import * as p from "@bokehjs/core/properties";
export declare class TreeView extends WidgetView {
    model: Tree;
    render(): void;
    get_data(): any;
}
export declare namespace Tree {
    type Attrs = p.AttrsOf<Props>;
    type Props = Widget.Props & {
        selected: p.Property<[string, string, string]>;
        theme: p.Property<string>;
        tree: p.Property<any[]>;
    };
}
export interface Tree extends Tree.Attrs {
}
export declare class Tree extends Widget {
    properties: Tree.Props;
    __view_type__: TreeView;
    static __module__: string;
    constructor(attrs?: Partial<Tree.Attrs>);
    static init_Tree(): void;
}
//# sourceMappingURL=filetree.d.ts.map