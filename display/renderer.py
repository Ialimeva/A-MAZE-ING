from config import WIDTH, HEIGHT, PIXEL_SIZE, BPP, elements
from utils import offset

def create_buff_image(m, mlx_ptr, img_ptr, img_line):
    buff_image = m.mlx_new_image(mlx_ptr, WIDTH, HEIGHT)
    img_adrss, img_bpp, img_line, img_ed = m.mlx_get_data_addr(
                                        img_ptr
                                    )

    buff_adrss, buff_bpp, buff_line, buff_ed = m.mlx_get_data_addr(
                                            buff_image
                                        )


    grid_x, grid_y = elements["floor"]

    for y in range(16):
        for x in range(16):
            src_x = grid_x * 16
            src_y = grid_y * 16
            off_src = offset(src_x + x, src_y + y, img_line)
            pxl_color = img_adrss[off_src : off_src + 4]

            off_dst = offset(x, y, buff_line)
            buff_adrss[off_dst : off_dst + 4] = pxl_color

    return (buff_image)