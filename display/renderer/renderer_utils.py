# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  renderer_utils.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/24 11:42:36 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/24 15:32:24 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from display import np

def scale_pixel(sprite: np.ndarray, scale: int) -> np.ndarray:
    scaled_img: np.ndarray = np.repeat(sprite, scale, axis=0)
    scaled_img: np.ndarray = np.repeat(scaled_img, scale, axis=1)

    return (scaled_img)


def recolor_pixel(
        sprite: np.ndarray,
        target_color: list[int, int, int, int],
        new_color: list[int, int, int, int]
    ) -> None:

    mask = np.all(sprite == target_color, axis=2)
    sprite[mask] = new_color
