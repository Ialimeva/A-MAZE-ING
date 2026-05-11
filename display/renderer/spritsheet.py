# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  spritsheet.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/05 19:28:27 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/11 13:52:45 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from display import np

class Spritesheet:
    def __init__(self, three_dimension_img):
        self.img_3d = three_dimension_img

    def get_tileset(self, x_min: int, x_max: int, y_min: int, y_max: int):
        tileset = self.img_3d[y_min : y_max, x_min : x_max]
        tile_mask = tileset[:,:, 3] > 0
        rows, cols = np.where(tile_mask)
        start_x, end_x = (min(cols), max(cols))
        start_y, end_y = (min(rows), max(rows))
        final_tile = self.img_3d[start_y : end_y + 1, start_x : end_x + 1]
        return (final_tile)