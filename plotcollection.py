import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator, interp1d
import kitcolors as kit
from scipy.interpolate import interp1d
from scipy.interpolate import RegularGridInterpolator
from .getvalues import getcircles, getcuts
import os
from scipy.special import sph_harm as Y
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import kitcolors as kit
from camminapy import *
from matplotlib.colors import LinearSegmentedColormap

n_bin = 101


def plotls(fig, ax, data, title):

    plt.style.use("kitish")
    ny, nx = data.shape
    x = np.linspace(-1.5, 1.5, nx + 1)
    y = np.linspace(-1.5, 1.5, ny + 1)
    p = ax.pcolormesh(x, y, data, cmap="plasma", vmin=0, vmax=0.4, rasterized=True)
    ax.set_xticks([-1.5, 1.5])
    ax.set_xticklabels([r"$-1.5$", r"$1.5$"])
    ax.set_xlabel(r"$x$ [cm]", labelpad=-5)
    ax.set_yticks([-1.5, 1.5])
    ax.set_yticklabels([r"$-1.5$", r"$1.5$"])
    ax.set_ylabel(r"$y$ [cm]", labelpad=-15)

    # cbaxes = fig.add_axes([1.05, 0.0, 0.05, 0.5])
    p.cmap.set_over("gray")
    clb = fig.colorbar(
        p,
        orientation="vertical",
        ax=ax,
        ticks=[0, 0.2, 0.4],
        extend="max",
        extendfrac=0.05,
        shrink=0.55,
        pad=-0.04,
        aspect=10,
    )
    clb.ax.set_title(r"$\phi(x,y)$", horizontalalignment="center")
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_aspect("equal", "box")
    ax.margins(x=0.0, y=0)
    ax.set_title(title)
    plt.setp(ax.spines.values(), linewidth=0)


def plotlslarge(fig, ax, data, title):

    plt.style.use("kitish")
    ny, nx = data.shape
    x = np.linspace(-1.5, 1.5, nx + 1)
    y = np.linspace(-1.5, 1.5, ny + 1)
    p = ax.pcolormesh(x, y, data, cmap="plasma", vmin=0, vmax=0.4, rasterized=True)
    ax.set_xticks([])  # [-1.5,1.5])
    # ax.set_xticklabels([r"$-1.5$", r"$1.5$"])
    # ax.set_xlabel(r"$x$ [cm]",labelpad = -5)
    ax.set_yticks([])  # [-1.5,1.5])
    # ax.set_yticklabels([r"$-1.5$", r"$1.5$"])
    # ax.set_ylabel(r"$y$ [cm]",labelpad = -15)

    # cbaxes = fig.add_axes([1.05, 0.0, 0.05, 0.5])
    p.cmap.set_over("gray")
    # clb = fig.colorbar(p,orientation = "vertical",ax=ax,ticks = [ 0,0.2,0.4],
    #                   extend='max',extendfrac=0.05,shrink = 0.55,pad = -0.04,aspect = 10)
    # clb.ax.set_title(r"$\phi(x,y)$",horizontalalignment="center")
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_aspect("equal", "box")
    ax.margins(x=0.0, y=0)
    ax.set_title(title, fontsize=22, pad=+5)
    plt.setp(ax.spines.values(), linewidth=0)


def plotlslargedelta(fig, ax, data, title):

    plt.style.use("kitish")
    ny, nx = data.shape
    x = np.linspace(-1.5, 1.5, nx + 1)
    y = np.linspace(-1.5, 1.5, ny + 1)
    cmap = mycmapdiv(kit.cyan, "white", kit.purple, nbins=201)
    p = ax.pcolormesh(x, y, data, cmap=cmap, vmin=-0.2, vmax=0.2, rasterized=True)
    ax.set_xticks([])  # [-1.5,1.5])
    # ax.set_xticklabels([r"$-1.5$", r"$1.5$"])
    # ax.set_xlabel(r"$x$ [cm]",labelpad = -5)
    ax.set_yticks([])  # [-1.5,1.5])
    # ax.set_yticklabels([r"$-1.5$", r"$1.5$"])
    # ax.set_ylabel(r"$y$ [cm]",labelpad = -15)

    # cbaxes = fig.add_axes([1.05, 0.0, 0.05, 0.5])
    # p.cmap.set_over("gray")
    clb = fig.colorbar(
        p,
        orientation="horizontal",
        ax=ax,
        ticks=[-0.2, 0, 0.2],
        extendfrac=0.05,
        shrink=0.55,
        pad=-0.04,
        aspect=10,
    )
    # clb.ax.set_title(r"$\phi(x,y)$",horizontalalignment="center")
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_aspect("equal", "box")
    ax.margins(x=0.0, y=0)
    ax.set_title(title, fontsize=22, pad=+5)
    plt.setp(ax.spines.values(), linewidth=0)


def plotcuts(fig, ax, data, n, ls):
    hori, verti, dia = getcuts(data, n)
    x = np.linspace(-1.4, 1.4, n)

    plt.style.use("kitish")
    ax.plot(x, hori, lw=1.5, linestyle="-", label="horizontal", color=kit.blue)
    ax.plot(x, verti, linestyle="-", lw=1.5, label="vertical", color=kit.purple)
    ax.plot(
        np.sqrt(2) * x, dia, lw=1.5, linestyle="-", label="diagonal", color=kit.orange
    )
    ax.plot(ls[:, 0], ls[:, 1], lw=1.5, label="reference", color=kit.black)

    ax.legend(loc="lower center", ncol=2, fontsize="x-small")
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([0, 0.6])
    ax.set_xlabel(r"$x$, $y$, $r$ [cm]")
    ax.set_ylabel("$\phi$")


def plotcutslarge(fig, ax, data, n, ls, title):
    hori, verti, dia = getcuts(data, n)
    x = np.linspace(-1.4, 1.4, n)

    plt.style.use("kitish")
    ax.plot(x, hori, lw=1.5, linestyle="-", label="horizontal", color=kit.blue)
    ax.plot(x, verti, linestyle="-", lw=1.5, label="vertical", color=kit.purple)
    ax.plot(
        np.sqrt(2) * x, dia, lw=1.5, linestyle="-", label="diagonal", color=kit.orange
    )
    ax.plot(ls[:, 0], ls[:, 1], lw=1.5, label="reference", color=kit.black)

    ax.legend(loc="lower left",ncol = 1,fontsize="large")
    ax.set_xlim([0, 1.2])
    ax.set_ylim([0, 0.5])
    ax.set_xlabel(r"Distance from the origin [cm]", fontsize=15)

    # ax.set_xlabel(r"$x$, $y$, $r$ [cm]",fontsize=15)
    ax.set_ylabel("$\phi$", fontsize=15)
    ax.set_title(title, fontsize=22, pad=+5)


def plotcircles(fig, ax, data, n, ls,title):
    radii = [1.0,0.9, 0.6, 0.2]
    sols = getcircles(data, n, radii)

    interpolant = interp1d(ls[:, 0], ls[:, 1])

    x = np.linspace(0, 2 * np.pi, n + 1)[:-1]

    plt.style.use("kitish")
    colors = [kit.blue, kit.orange, kit.purple, kit.green]
    for sol, rad, color in zip(sols, radii, colors):
        ax.plot(x, sol, lw=1.5, label="$r={}$".format(rad), color=color)
        refri = interpolant(rad)
        ax.axhline(refri, zorder=+100, lw=0.75, color=kit.black)
        ax.text(
            2 * np.pi + 0.05,
            refri,
            "$r={}$".format(rad),
            fontsize=8,
            verticalalignment="center",
        )

    ax.legend(loc="lower center", ncol=2, fontsize="large",framealpha=0.5)
    ax.set_xlim([0, 2 * np.pi])
    ax.set_ylim([0, 0.5])
    ax.set_xlabel(r"Cardinal direction",fontsize = 15)
    ax.set_ylabel("$\phi$",fontsize = 15)
    ax.set_xticks([0, 0.5 * np.pi, np.pi, 1.5 * np.pi, 2 * np.pi])
    ax.set_xticklabels(["N", "E", "S", "W", "N"])
    ax.set_title(title, fontsize=22, pad=+5)


def plotcblarge(fig, ax, data, title):

    plt.style.use("kitish")
    ny, nx = data.shape
    x = np.linspace(-1.5, 1.5, nx + 1)
    y = np.linspace(-1.5, 1.5, ny + 1)
    data = np.log10(data + 1e-8)

    p = ax.pcolormesh(x, y, data, cmap="plasma", vmin=-7, vmax=0, rasterized=True)
    xc = (x[1:] + x[:-1]) / 2
    yc = (y[1:] + y[:-1]) / 2
    lines = [-5, -4, -3]
    CS = ax.contour(
        xc,
        yc,
        data,
        lines,
        colors=["white", "silver", "black"],
        linestyles="-",
        linewidths=1.0,
    )
    manual_locations = [(-1.3, +0.5), (-1.25, +1.2), (-0.1, 0.1)]
    ax.clabel(CS, inline=1, fontsize=8, fmt="%d", manual=manual_locations)

    ax.set_xticks([])  # [-1.5,1.5])
    # ax.set_xticklabels([r"$-1.5$", r"$1.5$"])
    # ax.set_xlabel(r"$x$ [cm]",labelpad = -5)
    ax.set_yticks([])  # [-1.5,1.5])
    # ax.set_yticklabels([r"$-1.5$", r"$1.5$"])
    # ax.set_ylabel(r"$y$ [cm]",labelpad = -15)

    # cbaxes = fig.add_axes([1.05, 0.0, 0.05, 0.5])
    # p.cmap.set_over("gray")
    # clb = fig.colorbar(p,orientation = "vertical",ax=ax,ticks = [ 0,0.2,0.4],
    #                   extend='max',extendfrac=0.05,shrink = 0.55,pad = -0.04,aspect = 10)
    # clb.ax.set_title(r"$\phi(x,y)$",horizontalalignment="center")
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_aspect("equal", "box")
    ax.margins(x=0.0, y=0)
    ax.set_title(title, fontsize=18, pad=+5)
    plt.setp(ax.spines.values(), linewidth=0)
    clb = fig.colorbar(
        p,
        orientation="horizontal",
        ax=ax,
        ticks=[-7, -6, -5, -4, -3, -2, -1, 0],
        shrink=0.65,
        pad=-0.022,
        aspect=30,
    )

    clb.ax.set_title(
        r"$\log_{10} \, \phi(x,y)$",
        horizontalalignment="center",
        verticalalignment="center",
    )

    # fig.colorbar(p, orientation="horizontal", pad=0.01,shrink = 0.6,)


def plotall(data, prefix, title, testcaseid):
    ls = np.loadtxt("/home/qd4314/Software/camminapy/camminapy/exactLineSource.txt", delimiter=",")
    ls[0,0] = -2.5
    ls[-1,0] = 2.5
    if testcaseid == 1:  # Linesource
        plt.style.use("kitish")
        fig, ax = plt.subplots(1, 1, figsize=(3.0, 4.0))
        plotlslarge(fig, ax, data, title)
        fn = prefix + "imagesclarge.pdf"
        plt.savefig(fn, rasterized=True)
        os.system("pdfcrop --margins '1 1 1 40' {} {}".format(fn, fn))

        plt.style.use("kitish")
        fig, ax = plt.subplots(1, 1, figsize=(3.0, 4.0))
        plotcutslarge(fig, ax, data, 1000, ls, title)
        fn = prefix + "cuts.pdf"
        plt.savefig(fn, rasterized=True)
        os.system("pdfcrop --margins '1 1 1 20' {} {}".format(fn, fn))

        plt.style.use("kitish")
        fig, ax = plt.subplots(1, 1, figsize=(3.0, 4.0))
        plotcircles(fig, ax, data, 1000, ls, title)
        fn = prefix + "circles.pdf"
        plt.savefig(fn, rasterized=True)
        os.system("pdfcrop --margins '1 1 1 20' {} {}".format(fn, fn))
    else:  # Checkerboard
        pass
        plt.style.use("kitish")
        fig, ax = plt.subplots(1, 1, figsize=(3.0, 3.0))
        plotcblarge(fig, ax, data, title)
        fn = prefix + "imagesclarge.pdf"
        plt.savefig(fn, rasterized=True)
        os.system("pdfcrop --margins '1 1 1 20' {} {}".format(fn, fn))


# 	plt.style.use("kitish")
# 	fig,ax = plt.subplots(1,1,figsize=(3.0,2.6))
# 	plotls(fig,ax,data,title)
# 	plt.savefig(prefix+"imagesc.pdf",rasterized=True)

# 	plt.style.use("kitish")
# 	fig,ax = plt.subplots(1,1,figsize=(3.0,2.6))
# 	plotcuts(fig,ax,data,1000,ls)
# 	plt.savefig(prefix + "cuts.pdf",rasterized=True)

# 	plt.style.use("kitish")
# 	fig,ax = plt.subplots(1,1,figsize=(3.0,2.6))
# 	plotcircles(fig,ax,data,1000,ls)
# 	plt.savefig(prefix + "circles.pdf",rasterized=True)


# 	plt.style.use("kitish")
# 	fig,ax = plt.subplots(1,1,figsize=(3.0,3.0))
# 	plotlslargedelta(fig,ax,data,title)
# 	fn = prefix+"imagesclargedelta.pdf"#
# 	plt.savefig(fn,rasterized=True)
# 	os.system("pdfcrop --margins '1 1 1 40' {} {}".format(fn,fn))

# plt.style.use("kitish")
# fig,ax = plt.subplots(1,1,figsize=(3.0,4.0))
# plotcutslarge(fig,ax,data,1000,ls,title)
# fn = prefix + "cuts.pdf"
# plt.savefig(fn,rasterized=True)
# os.system("pdfcrop --margins '1 1 1 20' {} {}".format(fn,fn))
