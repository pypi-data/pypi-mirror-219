import {LogColorMapper} from "@bokehjs/models/mappers/log_color_mapper"
import {Arrayable} from "@bokehjs/core/types"
import {min, max} from "@bokehjs/core/util/arrayable"
import * as p from "@bokehjs/core/properties"

export type OffsetLogScanData = {
  min: number
  max: number
  scale: number
  interval: number[]
}

export namespace OffsetLogColorMapper {
  export type Attrs = p.AttrsOf<Props>

  export type Props = LogColorMapper.Props & {
    log_span: p.Property<number[]>
  }
}

export interface OffsetLogColorMapper extends OffsetLogColorMapper.Attrs {}

export class OffsetLogColorMapper extends LogColorMapper {
  properties: OffsetLogColorMapper.Props

  static __module__ = "pyscivis.visualizer.models.offset_log_color_mapper"

  constructor(attrs?: Partial<OffsetLogColorMapper.Attrs>) {
    super(attrs)
  }

  static init_OffsetLogColorMapper(): void {
    this.define<OffsetLogColorMapper.Props>(({Array, Number}) => ({
      log_span: [Array(Number), [1, 10]],
    }))
  }

  protected scan(data: Arrayable<number>, n: number): OffsetLogScanData {
    // retrieve specified low and high or calculate it if unspecified
    let low = this.low != null ? this.low : min(data)
    let high = this.high != null ? this.high : max(data)

    let span = this.log_span !=null ? this.log_span : [1, 10]

    const interval = [low, high]
    // n: Palette-size
    const scale = n / (Math.log(span[1]) - Math.log(span[0]))
    return {max: span[1], min: span[0], scale, interval}
  }

  protected cmap<T>(d: number, palette: Arrayable<T>, low_color: T, high_color: T, scan_data: OffsetLogScanData): T {
    const max_key = palette.length - 1
    let _max = scan_data.max
    let _min = scan_data.min
    let interval = scan_data.interval

    // mapping our interval [_min, _max] onto the logspan [interval[0], interval[1]]
    // https://math.stackexchange.com/a/914843
    d = _min + (_max-_min)/(interval[1]-interval[0])*(d-interval[0])

    if (d > _max) {
      return high_color
    }
    // This handles the edge case where d == high, since the code below maps
    // values exactly equal to high to palette.length, which is greater than
    // max_key
    if (d == _max){
      return palette[max_key]
    }
    else if (d < _min){
      return low_color
    }

    // Get the palette-color key by calculating the log of the
    // to-be-colormapped value and multiplying it by the scale
    const log = Math.log(d) - Math.log(_min)  // subtract the low offset
    let key = Math.floor(log * scan_data.scale)

    // Deal with upper bound
    if (key > max_key) {
      key = max_key
    }
    return palette[key]
  }
}
