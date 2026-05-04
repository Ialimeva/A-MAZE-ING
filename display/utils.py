# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  utils.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/04/29 11:59:44 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/04 17:30:39 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

MlxApp = Any
MlxPtr = Any
WindowPtr = Any
ImagePtr = Any

def offset(x: int, y: int, line: int) -> int:
    res: int = (y * line) + (x * 4);
    return (res)

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