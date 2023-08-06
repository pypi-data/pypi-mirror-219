import { LogColorMapper } from "@bokehjs/models/mappers/log_color_mapper";
import { Arrayable } from "@bokehjs/core/types";
import * as p from "@bokehjs/core/properties";
export declare type OffsetLogScanData = {
    min: number;
    max: number;
    scale: number;
    interval: number[];
};
export declare namespace OffsetLogColorMapper {
    type Attrs = p.AttrsOf<Props>;
    type Props = LogColorMapper.Props & {
        log_span: p.Property<number[]>;
    };
}
export interface OffsetLogColorMapper extends OffsetLogColorMapper.Attrs {
}
export declare class OffsetLogColorMapper extends LogColorMapper {
    properties: OffsetLogColorMapper.Props;
    static __module__: string;
    constructor(attrs?: Partial<OffsetLogColorMapper.Attrs>);
    static init_OffsetLogColorMapper(): void;
    protected scan(data: Arrayable<number>, n: number): OffsetLogScanData;
    protected cmap<T>(d: number, palette: Arrayable<T>, low_color: T, high_color: T, scan_data: OffsetLogScanData): T;
}
//# sourceMappingURL=offset_log_color_mapper.d.ts.map