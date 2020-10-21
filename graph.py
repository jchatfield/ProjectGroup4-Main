# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:38:54 2020

@author: Dime
"""

import matplotlib.pyplot as plt
import numpy as np

DARKGREY = '#222222'
LIGHTGREY = '#555555'

plt.style.use('dark_background')
plt.rcParams['axes.facecolor'] = DARKGREY
plt.rcParams['axes.edgecolor'] = LIGHTGREY
plt.rcParams['axes.labelcolor'] = LIGHTGREY
plt.rcParams['patch.edgecolor'] = LIGHTGREY
plt.rcParams['savefig.facecolor'] = DARKGREY
plt.rcParams['figure.facecolor'] = DARKGREY

CMAP = plt.get_cmap("cool")


def plot_wave(wave, title='', save=False):
    """ Plot a single wave """

    plt.plot(wave, color=CMAP(0))

    if not save:
        plt.title(title, color=LIGHTGREY)

    frame = plt.gca()
    frame.axes.xaxis.set_ticklabels([])
    frame.axes.yaxis.set_ticklabels([])
    frame.spines['bottom'].set_color(LIGHTGREY)
    frame.spines['top'].set_color(LIGHTGREY)
    frame.xaxis.label.set_color(LIGHTGREY)
    frame.tick_params(axis='x', colors=DARKGREY)
    frame.tick_params(axis='y', colors=DARKGREY)

    plt.grid(True, color=LIGHTGREY)
    plt.tight_layout(pad=0.0)

    if save:
        plt.savefig(save)
    else:
        plt.show()

    plt.gcf().clear()


def plot_wavetable(wavetable, title='', save=False, spacing=None):
    """ Plot all waves in a wavetable """

    colors = [CMAP(i) for i in np.linspace(0, 1, wavetable.num_slots)]

    if not save:
        plt.title(title, color=LIGHTGREY)

    if spacing is None:
        spacing = 0.0
        for prev, wave in zip(wavetable.waves[:-1], wavetable.waves[1:]):
            spacing = max(spacing, np.amax(prev - wave))
        spacing += 0.1

    for i, wave in enumerate(wavetable.waves):
        plt.plot(wave + spacing * i, color=colors[i])

    frame = plt.gca()
    frame.axes.xaxis.set_ticklabels([])
    frame.axes.yaxis.set_ticklabels([])
    frame.spines['bottom'].set_color(LIGHTGREY)
    frame.spines['top'].set_color(LIGHTGREY)
    frame.xaxis.label.set_color(LIGHTGREY)
    frame.tick_params(axis='x', colors=DARKGREY)
    frame.tick_params(axis='y', colors=DARKGREY)

    plt.grid(True, color=LIGHTGREY)
    plt.tight_layout(pad=0.0)

    if save:
        plt.savefig(save)
    else:
        plt.show()

    plt.gcf().clear()