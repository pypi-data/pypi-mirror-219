import { LogTickFormatter } from "@bokehjs/models/formatters/log_tick_formatter";
import { GraphicsBox } from "@bokehjs/core/graphics";
import * as p from "@bokehjs/core/properties";
export declare namespace OffsetLogTickFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = LogTickFormatter.Props & {
        min_exponent: p.Property<number>;
        low: p.Property<number>;
        high: p.Property<number>;
        log_span: p.Property<number[]>;
    };
}
export interface OffsetLogTickFormatter extends OffsetLogTickFormatter.Attrs {
}
export declare class OffsetLogTickFormatter extends LogTickFormatter {
    properties: OffsetLogTickFormatter.Props;
    static __module__: string;
    constructor(attrs?: Partial<OffsetLogTickFormatter.Attrs>);
    static init_OffsetLogTickFormatter(): void;
    format_graphics(ticks: number[], opts: {
        loc: number;
    }): GraphicsBox[];
}
//# sourceMappingURL=offset_log_tick_formatter.d.ts.map