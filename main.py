import hsv_color_picker
import air_canvas

lower, upper = hsv_color_picker.hsv_color_picker()

air_canvas.air_canvas(lower, upper)
