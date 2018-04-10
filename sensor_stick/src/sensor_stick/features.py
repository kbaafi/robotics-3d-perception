import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from pcl_helper import *


def rgb_to_hsv(rgb_list):
    rgb_normalized = [1.0*rgb_list[0]/255, 1.0*rgb_list[1]/255, 1.0*rgb_list[2]/255]
    hsv_normalized = matplotlib.colors.rgb_to_hsv([[rgb_normalized]])[0][0]
    return hsv_normalized

def compute_color_histogram(data,nbins=32,hrange=(0,256)):
    img_hist = np.histogram(data,bins=nbins,range=hrange)
    
    return img_hist[0]

def compute_histogram(data,nbins=10,hrange=(-1,1)):
    hist = np.histogram(data,bins=nbins)
    return hist[0]

def normalize(data):
    norm = data / np.sum(data)
    return norm


def compute_color_histograms(cloud,bin_size, using_hsv=True):

    # Compute histograms for the clusters
    point_colors_list = []

    # Step through each point in the point cloud
    for point in pc2.read_points(cloud, skip_nans=True):
        rgb_list = float_to_rgb(point[3])
        if using_hsv:
            point_colors_list.append(rgb_to_hsv(rgb_list) * 255)
        else:
            point_colors_list.append(rgb_list)

    # Populate lists with color values
    channel_1_vals = []
    channel_2_vals = []
    channel_3_vals = []

    for color in point_colors_list:
        channel_1_vals.append(color[0])
        channel_2_vals.append(color[1])
        channel_3_vals.append(color[2])
    
    # TODO: Compute histograms
    channel_1_hist = compute_color_histogram(channel_1_vals,nbins=bin_size)
    channel_2_hist = compute_color_histogram(channel_2_vals,nbins=bin_size)
    channel_3_hist = compute_color_histogram(channel_3_vals,nbins=bin_size)

    # TODO: Concatenate and normalize the histograms
    color_features = np.concatenate((channel_1_hist, channel_2_hist, channel_3_hist)).astype(np.float64)

    normed_features = normalize(color_features)
    
    return normed_features 


def compute_normal_histograms(normal_cloud, bin_size):
    norm_x_vals = []
    norm_y_vals = []
    norm_z_vals = []

    for norm_component in pc2.read_points(normal_cloud,
                                          field_names = ('normal_x', 'normal_y', 'normal_z'),
                                          skip_nans=True):
        norm_x_vals.append(norm_component[0])
        norm_y_vals.append(norm_component[1])
        norm_z_vals.append(norm_component[2])

    # TODO: Compute histograms of normal values (just like with color)
    x_hist = compute_histogram(norm_x_vals, nbins=bin_size)
    y_hist = compute_histogram(norm_y_vals, nbins=bin_size)
    z_hist = compute_histogram(norm_z_vals, nbins=bin_size)
    

    # TODO: Concatenate and normalize the histograms
    #normals_features = np.concatenate((x_hist, y_hist,z_hist)).astype(np.float64)
    normals_features = np.concatenate((x_hist, y_hist,z_hist)).astype(np.float64)

    # Generate random features for demo mode.  
    # Replace normed_features with your feature vector
    normed_features = normalize(normals_features)

    return normals_features
