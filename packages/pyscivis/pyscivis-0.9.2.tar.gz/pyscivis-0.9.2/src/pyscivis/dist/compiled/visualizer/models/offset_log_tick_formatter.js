import { LogTickFormatter } from "@bokehjs/models/formatters/log_tick_formatter";
import { min, max } from "@bokehjs/core/util/arrayable";
export class OffsetLogTickFormatter extends LogTickFormatter {
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
        const start = min(this.log_span);
        const end = max(this.log_span);
        ticks = ticks.map((value) => {
            return this.low + (this.high - this.low) / (end - start) * (value - start);
        });
        return this.basic_formatter.format_graphics(ticks, opts);
    }
}
OffsetLogTickFormatter.__name__ = "OffsetLogTickFormatter";
OffsetLogTickFormatter.__module__ = "pyscivis.visualizer.models.offset_log_tick_formatter";
OffsetLogTickFormatter.init_OffsetLogTickFormatter();
//# sourceMappingURL=offset_log_tick_formatter.js.map