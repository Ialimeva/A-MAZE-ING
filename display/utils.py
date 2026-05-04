# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  utils.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/29 11:59:44 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/01 18:05:36 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any
# from config import elements, CELL_HEIGHT, CELL_WIDTH

MlxApp = Any
MlxPtr = Any
WindowPtr = Any
ImagePtr = Any

# def exit_window(param) -> None:
#     m, mlx_ptr, window_ptr = param
#     m.mlx_destroy_window(mlx_ptr, window_ptr)
#     m.mlx_release(mlx_ptr)


# def compute_key(keycode, param) -> None:
#     if (keycode == Key.get("esc")):
#         exit_window(param)


# def offset(x: int, y: int, line: int) -> int:
#     res: int = (y * line) + (x * 4);
#     return (res)

# # class Draw():
# def draw_floor(m, mlx_ptr,
#                 img_adr, img_line,
#                 buff_adr, buff_line,
#                 col, row
#             ) -> None:
#     grid_x, grid_y = elements["floor"]
#     src_x = grid_x * 16
#     src_y = grid_y * 16
#     for r in range(row):
#         for c in range(col):
#             # Iterates through each cell
#             cell_position_x = c * 48
#             cell_position_y = r * 64
#             for j in range(4):
#                 for i in range(3):
#                     # Iterates through each tile(16x16) in a cell
#                     dest_x = cell_position_x + (i * 16)
#                     dest_y = cell_position_y + (j * 16)
#                     for y in range(16):
#                             # Iterates through all 16 pixels on a row
#                             off_src = offset(
#                                 src_x,
#                                 src_y + y,
#                                 img_line
#                             )
#                             color = img_adr[off_src : off_src + 64]
#                             off_dst = offset(
#                                 dest_x,
#                                 dest_y + y,
#                                 buff_line
#                             )
#                             buff_adr[off_dst : off_dst + 64] = color




# def draw_north_wall(m, mlx_ptr,
#                     img_adr, img_line,
#                     buff_adr, buff_line,
#                     col, row
#                 ) -> None:
#     grid_x, grid_y = elements["north"]
#     src_x = grid_x * 16
#     src_y = grid_y * 16
#     for y in range(16):
#         for x in range(16):
#             off_src = offset(src_x + x, src_y + y, img_line)
#             color = img_adr[off_src : off_src + 4]
#             if (color[3] != 0):
#                 dest_x = col * 16
#                 dest_y = row * 16
#                 off_dst = offset(dest_x + x, dest_y + y, buff_line)
#                 buff_adr[off_dst : off_dst + 4] = color


# def draw_south_wall(m, mlx_ptr,
#                     img_adr, img_line,
#                     buff_adr, buff_line,
#                     col, row
#                 ) -> None:
#     grid_x, grid_y = elements["north"]
#     src_x = grid_x * 16
#     src_y = grid_y * 16
#     for y in range(16):
#         for x in range(16):
#             off_src = offset(src_x + x, src_y + y, img_line)
#             color = img_adr[off_src : off_src + 4]
#             if (color[3] != 0):
#                 dest_x = col * 16
#                 dest_y = row * 16
#                 off_dst = offset(dest_x + x, dest_y + y, buff_line)
#                 buff_adr[off_dst : off_dst + 4] = color

# def draw_east_wall(m, mlx_ptr,
#                     img_adr, img_line,
#                     buff_adr, buff_line,
#                     col, row
#                 ) -> None:
#     grid_x, grid_y = elements["east"]
#     src_x = grid_x * 16
#     src_y = grid_y * 16
#     for y in range(16):
#         for x in range(16):
#             off_src = offset(src_x + x, src_y + y, img_line)
#             color = img_adr[off_src : off_src + 4]
#             # final_color = color + 0x00330000 
#             if (color[3] != 0):
#                 dest_x = col * 16
#                 dest_y = row * 16
#                 off_dst = offset(dest_x + x, dest_y + y, buff_line)
#                 buff_adr[off_dst : off_dst + 4] = color

# def draw_west_wall(m, mlx_ptr,
#                     img_adr, img_line,
#                     buff_adr, buff_line,
#                     col, row
#                 ) -> None:
#     grid_x, grid_y = elements["west"]
#     src_x = grid_x * 16
#     src_y = grid_y * 16
#     for y in range(16):
#         for x in range(16):
#             off_src = offset(src_x + x, src_y + y, img_line)
#             color = img_adr[off_src : off_src + 4]
#             if (color[3] != 0):
#                 dest_x = col * 16
#                 dest_y = row * 16
#                 off_dst = offset(dest_x + x, dest_y + y, buff_line)
#                 buff_adr[off_dst : off_dst + 4] = color