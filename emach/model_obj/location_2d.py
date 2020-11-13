# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 23:35:50 2020

@author: Bharat
"""
import numpy as np

__all__ = ["Location2D"]


class Location2D:
    def __init__(self, anchor_xy=np.array([0, 0]), theta=0):
        self.anchor_xy = anchor_xy
        self.theta = theta * np.pi / 180
        self.rot = np.array(
            [
                [np.cos(self.theta), -np.sin(self.theta)],
                [np.sin(self.theta), np.cos(self.theta)],
            ]
        )

    def trans_coord(self, coords, add_theta=None):
        if add_theta is None:
            trans = self.rot
        else:
            trans = np.array(
                [
                    [np.cos(add_theta), -np.sin(add_theta)],
                    [np.sin(add_theta), np.cos(add_theta)],
                ]
            )
        rot_coords = np.transpose(np.matmul(trans, np.transpose(coords)))
        trans_coords = np.zeros(coords.shape)

        trans_coords[:, 0] = rot_coords[:, 0] + self.anchor_xy[0]
        trans_coords[:, 1] = rot_coords[:, 1] + self.anchor_xy[1]
        return trans_coords
