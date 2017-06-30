#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import sys
import numpy as np
import math

class MeanShift(object):
    def __init__(self, image, h_s=16, h_r=16, L=4, N=10, epsilon=):
        super(MeanShift, self).__init__(name)
        self.img = cv2.imread(image, cv2.IMREAD_UNCHANGED)
        if len(self.img.shape) == 3:
            self.height = self.img.shape[0]
            self.width = self.img.shape[1]
            self.channels = self.img.shape[2]
        else:
            self.height = self.img.shape[0]
            self.width = self.img.shape[1]
            self.channels = 1
        self.h_s = h_s
        self.h_r = h_r
        self.L = L
        self.N = N
        self.epsilon = epsilon
        self.candidate_list = self._in_radius_pixel()

    def run_mean_shift(self):
        img_pyramid = self._create_image_pyramid()
        output_num = 0
        for image in reversed(img_pyramid):
            name = "output"+str(output_num)
            #TODO
            output_image = self.mean_algo(image)

            output_num += 1
            cv2.imwrite(name, output_image)
        return True

    def _create_image_pyramid(self):
        image_pyramid = []
        for l in range(self.L):
            resized_img = cv2.resize(self.img, (self.width/2**l, self.height/2**l))
            image_pyramid.append(resized_img)
        return image_pyramid

    def mean_algo(self, img):
        output_img = img.copy()
        img_height = img.shape[0]
        img_width = img.shape[1]
        for x in range(img_height):
            for y in range(img_width):
                r, g, b = self.xy_to_rgb(img, x, y)
                n = 0
                while(True):
                    close_list = self.find_close_pixel(x, y, r, g, b, img, img_height, img_width)
                    x_, y_, r_, g_, b_ = self.find_center(img, close_list)
                    eps_checker = math.fabs(x_ - x) + math.fabs(y_ - y) + (r - r_)**2 + (g - g_)**2 + (b - b_)**2
                    if n >= self.N or eps_checker <= self.epsilon or (x==x_ and y==y_):
                        break
                    else:
                        x = x_
                        y = y_
                        r = r_
                        g = g_
                        b = b_
                        n += 1
                output_img[x][y] = [r_, g_, b_]
        return output_img

    def _in_radius_pixel(self):
        candidate_list = []
        for k in range(-self.h_s, self.h_s+1):
            for l in range(-self.h_s, self.h_s+1):
                distance = math.sqrt(k**2 + l**2)
                if distance <= self.h_s:
                    candidate_list.append([k, l])
        return candidate_list

    def find_close_pixel(self, i, j, r, g, b, img, img_height, img_width):
        close_pixel = []
        for [k, l] in self.candidate_list:
            k += i
            l += j
            if 0<=k<img_height and 0<=l<img_width:
                r_ = img[k][l][0]
                g_ = img[k][l][1]
                b_ = img[k][l][2]
                distance = math.sqrt((r_ - r)**2 + (g_ - g)**2 + (b_ - b)**2)
                if distance <= self.h_r:
                    close_pixel.append([k, l])

        # for k in range(i-self.h_s, i+self.h_s+1):
        #     for l in range(j-self.h_s, j+self.h_s+1):
        #         if 0<=k<img_height and 0<=l<img_width:
        #             r_ = img[k][l][0]
        #             g_ = img[k][l][1]
        #             b_ = img[k][l][2]
        #             distance = math.sqrt((r_ - r)**2 + (g_ - g)**2 + (b_ - b)**2)
        #             if distance <= self.h_r:
        #                 close_pixel.append([k, l])
        return close_pixel

    def xy_to_rgb(self, img, x, y):
        return img[x][y][0], img[x][y][1], img[x][y][2]

    def find_center(self, img, pixel_array):
        x_center, y_center = 0.0, 0.0
        r_center, g_center, b_center = 0.0, 0.0, 0.0
        p_num = len(pixel_array)
        for i in range(p_num):
            x = pixel_array[i][0]
            y = pixel_array[i][1]
            r, g, b = xy_to_rgb(img, x, y)
            x_center += x
            y_center += y
            r_center += r
            g_center += g
            b_center += b
        x_center = int(round(x_center/p_num))
        y_center = int(round(y_center/p_num))
        r_center = int(round(r_center/p_num))
        g_center = int(round(g_center/p_num))
        b_center = int(round(b_center/p_num))
        return x_center, y_center, r_center, g_center, b_center

    


def main():
    mean_shift = MeanShift()
    mean_shift.run_mean_shift("dishes.jpg")
    return True

if __name__ == '__main__':
    main()
