from keymap import Keymap as Key
from config import elements

def exit_window(param) -> None:
    m, mlx_ptr, window_ptr = param
    m.mlx_destroy_window(mlx_ptr, window_ptr)
    m.mlx_release(mlx_ptr)


def compute_key(keycode, param) -> None:
    if (keycode == Key.get("esc")):
        exit_window(param)


def offset(x: int, y: int, line: int) -> int:
    res: int = (y * line) + (x * 4);
    return (res)


def draw_floor(m, mlx_ptr, img_adr, img_line, window_ptr) -> None:
    grid_x, grid_y = elements["floor"]

    buff = m.mlx_new_image(mlx_ptr, 16, 16)
    buff_adr, buff_bpp, buff_line, buff_ed = m.mlx_get_data_addr(buff)
    src_x = grid_x * 16
    src_y = grid_y * 16
    for y in range(16):
        for x in range(16):
            off_src = offset(src_x + x, src_y + y, img_line)
            color = img_adr[off_src : off_src + 4]
            off_dst = offset(x, y, buff_line)
            buff_adr[off_dst : off_dst + 4] = color
    m.mlx_put_image_to_window(mlx_ptr, window_ptr, buff, 7, 16)


def draw_north_wall(m, mlx_ptr, img_adr, img_line, window_ptr) -> None:
    grid_x, grid_y = elements["north"]

    buff = m.mlx_new_image(mlx_ptr, 16, 16)
    buff_adr, buff_bpp, buff_line, buff_ed = m.mlx_get_data_addr(buff)
    src_x = grid_x * 16
    src_y = grid_y * 16
    for y in range(16):
        for x in range(16):
            off_src = offset(src_x + x, src_y + y, img_line)
            color = img_adr[off_src : off_src + 4]
            off_dst = offset(x, y, buff_line)
            buff_adr[off_dst : off_dst + 4] = color
    m.mlx_put_image_to_window(mlx_ptr, window_ptr, buff, 7, 0)


def draw_south_wall(m, mlx_ptr, img_adr, img_line, window_ptr) -> None:
    grid_x, grid_y = elements["north"]

    buff = m.mlx_new_image(mlx_ptr, 16, 16)
    buff_adr, buff_bpp, buff_line, buff_ed = m.mlx_get_data_addr(buff)
    src_x = grid_x * 16
    src_y = grid_y * 16
    for y in range(16):
        for x in range(16):
            off_src = offset(src_x + x, src_y + y, img_line)
            color = img_adr[off_src : off_src + 4]
            off_dst = offset(x, y, buff_line)
            buff_adr[off_dst : off_dst + 4] = color
    m.mlx_put_image_to_window(mlx_ptr, window_ptr, buff, 7, 32)


def draw_east_wall(m, mlx_ptr, img_adr, img_line, window_ptr) -> None:
    grid_x, grid_y = elements["east"]

    buff = m.mlx_new_image(mlx_ptr, 2, 16)
    buff_adr, buff_bpp, buff_line, buff_ed = m.mlx_get_data_addr(buff)
    src_x = grid_x
    src_y = grid_y * 16
    for y in range(16):
        for x in range(2):
            off_src = offset(src_x + x, src_y + y, img_line)
            color = img_adr[off_src : off_src + 4]
            off_dst = offset(x, y, buff_line)
            buff_adr[off_dst : off_dst + 4] = color
    m.mlx_put_image_to_window(mlx_ptr, window_ptr, buff, 500, 1)


def draw_west_wall(m, mlx_ptr, img_adr, img_line, window_ptr) -> None:
    grid_x, grid_y = elements["west"]

    buff = m.mlx_new_image(mlx_ptr, 8, 48)
    buff_adr, buff_bpp, buff_line, buff_ed = m.mlx_get_data_addr(buff)
    src_x = grid_x * 16
    src_y = grid_y * 16
    for y in range(48):
        for x in range(7):
            off_src = offset(src_x + x, src_y + y, img_line)
            color = img_adr[off_src : off_src + 4]
            off_dst = offset(x, y, buff_line)
            buff_adr[off_dst : off_dst + 4] = color
    m.mlx_put_image_to_window(mlx_ptr, window_ptr, buff, 50, 0)