import {LogTickFormatter} from "@bokehjs/models/formatters/log_tick_formatter"
import {min, max} from "@bokehjs/core/util/arrayable"
import {GraphicsBox} from "@bokehjs/core/graphics"
import * as p from "@bokehjs/core/properties"


export namespace OffsetLogTickFormatter {
  export type Attrs = p.AttrsOf<Props>

  export type Props = LogTickFormatter.Props & {
    min_exponent: p.Property<number>
    low: p.Property<number>
    high: p.Property<number>
    log_span: p.Property<number[]>
  }
}

export interface OffsetLogTickFormatter extends OffsetLogTickFormatter.Attrs {}

export class OffsetLogTickFormatter extends LogTickFormatter {
  properties: OffsetLogTickFormatter.Props

  static __module__ = "pyscivis.visualizer.models.offset_log_tick_formatter"

  constructor(attrs?: Partial<OffsetLogTickFormatter.Attrs>) {
    super(attrs)
  }

  static init_OffsetLogTickFormatter(): void {
    this.define<OffsetLogTickFormatter.Props>(({Array, Number}) => ({
      low: [ Number , 0 ],
      high: [ Number , 0 ],
      log_span: [Array(Number), [1, 10]]
    }))
  }

  format_graphics(ticks: number[], opts: {loc: number}): GraphicsBox[] {
    if (ticks.length == 0)
      return []

    const start = min(this.log_span)
    const end = max(this.log_span)

    ticks = ticks.map((value)=> {
        return this.low + (this.high-this.low)/(end-start)*(value-start)
    });

    return this.basic_formatter.format_graphics(ticks, opts)

  }
}