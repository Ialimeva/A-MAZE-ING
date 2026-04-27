from mlx import Mlx
from utils import compute_key, exit_window, draw_floor, draw_east_wall, draw_south_wall, draw_north_wall, draw_west_wall
from config import WIDTH, HEIGHT
from renderer import create_buff_image
 

m = Mlx()
mlx_ptr = m.mlx_init()
window_ptr = m.mlx_new_window(mlx_ptr, WIDTH, HEIGHT, "A-MAZE-ING")
m.mlx_key_hook(window_ptr, compute_key, [m, mlx_ptr, window_ptr])
m.mlx_hook(window_ptr, 33, 0, exit_window, [m, mlx_ptr, window_ptr])

img_ptr, width, height = m.mlx_png_file_to_image(
                            mlx_ptr, "assets/tileset_full.png"
                        )

img_adr, img_bpp, img_line, img_ed = m.mlx_get_data_addr(
                                        img_ptr
                                    )

draw_north_wall(m, mlx_ptr, img_adr, img_line, window_ptr)
draw_floor(m, mlx_ptr, img_adr, img_line, window_ptr)
# draw_east_wall(m, mlx_ptr, img_adr, img_line, window_ptr)
# draw_south_wall(m, mlx_ptr, img_adr, img_line, window_ptr)
draw_north_wall(m, mlx_ptr, img_adr, img_line, window_ptr)
draw_west_wall(m, mlx_ptr, img_adr, img_line, window_ptr)
m.mlx_loop(mlx_ptr)
