import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
import matplotlib.animation as animation

SensorCor=[[4,-4.5],[0.5,-5],[-3.5,-4],[-6,4.5],[-0.5,-1.5],[-2.5,2.5],[0.5,2.5],[1,5.5],[1,4.5],[0,7],[-4.5,5],[-1.5,7],[1.5,-7]]
SensorCorArr=np.asarray(SensorCor)
print(SensorCorArr)

import matplotlib
backend = matplotlib.get_backend()


AlldataDF=pd.read_csv("Sensor.csv", header=0,index_col=0).fillna(0)

depth=float(input("Please enter a depth from 0 to 22.5 you want to get the plot: "))
Layer=depth/2.5                    # starts from surface , 0 layer

#print(AlldataDF)



if True:
    row=AlldataDF.iloc[0]
    #print(row)
    templist=[]
    #get sensor data at the specified layer
    if Layer<5:
        if depth%2.5==0:
            for i in range(5):
                templist.append(row[9 - Layer + i * 10])
            for j in range(8):
                templist.append(row[50 + 4 - Layer + j * 5])
        else:
            for i in range(5):
                Top=row[9 - int(depth//2.5) + i * 10]
                Bot=row[9 - int(depth//2.5+1) + i * 10]
                temp=Top+(Bot-Top)*(depth%2.5)/2.5
                templist.append(temp)
            for j in range(8):
                Top1 = row[50+4 - int(depth // 2.5) + j * 5]
                Bot1 = row[50+4 - int(depth // 2.5 + 1) + j * 5]
                temp1 = Top1 + (Bot1 - Top1) * (depth % 2.5) / 2.5
                templist.append(temp1)



    else:
        if depth % 2.5 == 0:
            for i in range(5):
                templist.append(row[9 - Layer + i * 10])
        else:
            for i in range(5):
                Top = row[9 - int(depth // 2.5) + i * 10]
                Bot = row[9 - int(depth // 2.5 + 1) + i * 10]
                temp = Top + (Bot - Top) * (depth % 2.5) / 2.5
                templist.append(temp)


    #print(templist)
    #make interpolation
    if Layer<5:
        xmin = np.min(SensorCorArr[:, 0])
        xmax = np.max(SensorCorArr[:, 0])
        ymin = np.min(SensorCorArr[:, 1])
        ymax = np.max(SensorCorArr[:, 1])
        grid_x, grid_y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        grid_z0 = griddata(SensorCorArr, np.asarray(templist), (grid_x, grid_y), method='nearest')

        grid_z1 = griddata(SensorCorArr, np.asarray(templist), (grid_x, grid_y), method='linear')


        grid_z2 = griddata(SensorCorArr, np.asarray(templist), (grid_x, grid_y), method='cubic')
        fig, axs=plt.subplots(2,2,figsize=(6, 6))
        fig.canvas.manager.window.wm_geometry("+%d+%d" % (100, 0))

        im1=axs[0,0].imshow(grid_z0.T, extent=(xmin, xmax, ymin, ymax), origin='lower')
        axs[0,0].set_xticks(np.mgrid[xmin:xmax:5j])
        axs[0,0].plot(SensorCorArr[:, 0], SensorCorArr[:, 1], 'k.', ms=1)
        axs[0,0].set_title('Nearest')
        fig.colorbar(im1, ax=axs[0,0], boundaries=np.mgrid[np.min(AlldataDF.min()):np.max(AlldataDF.max()):6j])

        im2 = axs[0, 1].imshow(grid_z1.T, extent=(xmin, xmax, ymin, ymax), origin='lower')
        axs[0, 1].set_xticks(np.mgrid[xmin:xmax:5j])
        axs[0, 1].plot(SensorCorArr[:, 0], SensorCorArr[:, 1], 'k.', ms=1)
        axs[0, 1].set_title('linear')
        fig.colorbar(im2, ax=axs[0, 1], boundaries=np.mgrid[np.min(AlldataDF.min()):np.max(AlldataDF.max()):6j])

        im3 = axs[1, 0].imshow(grid_z2.T, extent=(xmin, xmax, ymin, ymax), origin='lower')
        axs[1, 0].set_xticks(np.mgrid[xmin:xmax:5j])
        axs[1, 0].plot(SensorCorArr[:, 0], SensorCorArr[:, 1], 'k.', ms=1)
        axs[1, 0].set_title('cubic')
        fig.colorbar(im3, ax=axs[1, 0], boundaries=np.mgrid[np.min(AlldataDF.min()):np.max(AlldataDF.max()):6j])

        XI, YI = grid_x, grid_y
        rbf = Rbf(SensorCorArr[:,0], SensorCorArr[:,1], np.asarray(templist), epsilon=2)
        ZI = rbf(XI, YI)

        im4 = axs[1, 1].imshow(ZI.T, extent=(xmin, xmax, ymin, ymax), origin='lower')
        axs[1, 1].set_xticks(np.mgrid[xmin:xmax:5j])
        axs[1, 1].plot(SensorCorArr[:, 0], SensorCorArr[:, 1], 'k.', ms=1)
        axs[1, 1].set_title('RBF interpolation')
        fig.colorbar(im4, ax=axs[1, 1], boundaries=np.mgrid[np.min(AlldataDF.min()):np.max(AlldataDF.max()):6j])

        plt.tight_layout()




    else:
        xmin = np.min(SensorCorArr[:5, 0])
        xmax = np.max(SensorCorArr[:5, 0])
        ymin = np.min(SensorCorArr[:5, 1])
        ymax = np.max(SensorCorArr[:5, 1])

        grid_x, grid_y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        grid_z0 = griddata(SensorCorArr[:5,:], np.asarray(templist), (grid_x, grid_y), method='nearest')
        grid_z1 = griddata(SensorCorArr[:5,:], np.asarray(templist), (grid_x, grid_y), method='linear')
        grid_z2 = griddata(SensorCorArr[:5,:], np.asarray(templist), (grid_x, grid_y), method='cubic')
        fig, axs = plt.subplots(2, 2, figsize=(6, 6))
        fig.canvas.manager.window.wm_geometry("+%d+%d" % (100, 0))

        im1 = axs[0, 0].imshow(grid_z0.T, extent=(xmin, xmax, ymin, ymax), origin='lower')
        axs[0, 0].set_xticks(np.mgrid[xmin:xmax:5j])
        axs[0, 0].plot(SensorCorArr[:5, 0], SensorCorArr[:5, 1], 'k.', ms=1)
        axs[0, 0].set_title('Nearest')
        fig.colorbar(im1, ax=axs[0, 0], boundaries=np.mgrid[np.min(AlldataDF.min()):np.max(AlldataDF.max()):6j])

        im2 = axs[0, 1].imshow(grid_z1.T, extent=(xmin, xmax, ymin, ymax), origin='lower')
        axs[0, 1].set_xticks(np.mgrid[xmin:xmax:5j])
        axs[0, 1].plot(SensorCorArr[:5, 0], SensorCorArr[:5, 1], 'k.', ms=1)
        axs[0, 1].set_title('linear')
        fig.colorbar(im2, ax=axs[0, 1], boundaries=np.mgrid[np.min(AlldataDF.min()):np.max(AlldataDF.max()):6j])

        im3 = axs[1, 0].imshow(grid_z2.T, extent=(xmin, xmax, ymin, ymax), origin='lower')
        axs[1, 0].set_xticks(np.mgrid[xmin:xmax:5j])
        axs[1, 0].plot(SensorCorArr[:5, 0], SensorCorArr[:5, 1], 'k.', ms=1)
        axs[1, 0].set_title('cubic')
        fig.colorbar(im3, ax=axs[1, 0], boundaries=np.mgrid[np.min(AlldataDF.min()):np.max(AlldataDF.max()):6j])

        XI, YI = grid_x, grid_y
        rbf = Rbf(SensorCorArr[:5, 0], SensorCorArr[:5, 1], np.asarray(templist), epsilon=2)
        ZI = rbf(XI, YI)

        im4 = axs[1, 1].imshow(ZI.T, extent=(xmin, xmax, ymin, ymax), origin='lower')
        axs[1, 1].set_xticks(np.mgrid[xmin:xmax:5j])
        axs[1, 1].plot(SensorCorArr[:5, 0], SensorCorArr[:5, 1], 'k.', ms=1)
        axs[1, 1].set_title('RBF interpolation')
        fig.colorbar(im4, ax=axs[1, 1], boundaries=np.mgrid[np.min(AlldataDF.min()):np.max(AlldataDF.max()):6j])

        plt.tight_layout()


def animate(k):
    # print(row)
    row=AlldataDF.iloc[k]
    #print(row)
    templist = []
    # get sensor data at the specified layer
    if Layer < 5:
        if depth % 2.5 == 0:
            for i in range(5):
                templist.append(row[9 - Layer + i * 10])
            for j in range(8):
                templist.append(row[50 + 4 - Layer + j * 5])
        else:
            for i in range(5):
                Top = row[9 - int(depth // 2.5) + i * 10]
                Bot = row[9 - int(depth // 2.5 + 1) + i * 10]
                temp = Top + (Bot - Top) * (depth % 2.5) / 2.5
                templist.append(temp)
            for j in range(8):
                Top1 = row[50 + 4 - int(depth // 2.5) + j * 5]
                Bot1 = row[50 + 4 - int(depth // 2.5 + 1) + j * 5]
                temp1 = Top1 + (Bot1 - Top1) * (depth % 2.5) / 2.5
                templist.append(temp1)



    else:
        if depth % 2.5 == 0:
            for i in range(5):
                templist.append(row[9 - Layer + i * 10])
        else:
            for i in range(5):
                Top = row[9 - int(depth // 2.5) + i * 10]
                Bot = row[9 - int(depth // 2.5 + 1) + i * 10]
                temp = Top + (Bot - Top) * (depth % 2.5) / 2.5
                templist.append(temp)
    #print(templist)
    # make interpolation
    if Layer < 5:
        xmin = np.min(SensorCorArr[:, 0])
        xmax = np.max(SensorCorArr[:, 0])
        ymin = np.min(SensorCorArr[:, 1])
        ymax = np.max(SensorCorArr[:, 1])
        grid_x, grid_y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        grid_z0 = griddata(SensorCorArr, np.asarray(templist), (grid_x, grid_y), method='nearest')
        grid_z1 = griddata(SensorCorArr, np.asarray(templist), (grid_x, grid_y), method='linear')
        grid_z2 = griddata(SensorCorArr, np.asarray(templist), (grid_x, grid_y), method='cubic')

        print(k)
        im1.set_data(grid_z0.T)
        axs[0, 0].set_title('Nearest_'+str(k))

        im2.set_data(grid_z1.T)
        axs[0, 1].set_title('linear')

        im3.set_data(grid_z2.T)
        axs[1, 0].set_title('cubic')

        XI, YI = grid_x, grid_y
        rbf = Rbf(SensorCorArr[:, 0], SensorCorArr[:, 1], np.asarray(templist), epsilon=2)
        ZI = rbf(XI, YI)

        im4.set_data(ZI.T)
        axs[1, 1].set_title('RBF interpolation')
    else:
        xmin = np.min(SensorCorArr[:5, 0])
        xmax = np.max(SensorCorArr[:5, 0])
        ymin = np.min(SensorCorArr[:5, 1])
        ymax = np.max(SensorCorArr[:5, 1])
        grid_x, grid_y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        grid_z0 = griddata(SensorCorArr[:5,:], np.asarray(templist), (grid_x, grid_y), method='nearest')
        grid_z1 = griddata(SensorCorArr[:5,:], np.asarray(templist), (grid_x, grid_y), method='linear')
        grid_z2 = griddata(SensorCorArr[:5,:], np.asarray(templist), (grid_x, grid_y), method='cubic')

        print(k)
        im1.set_data(grid_z0.T)
        axs[0, 0].set_title('Nearest_' + str(k))

        im2.set_data(grid_z1.T)
        axs[0, 1].set_title('linear')

        im3.set_data(grid_z2.T)
        axs[1, 0].set_title('cubic')

        XI, YI = grid_x, grid_y
        rbf = Rbf(SensorCorArr[:5, 0], SensorCorArr[:5, 1], np.asarray(templist), epsilon=2)
        ZI = rbf(XI, YI)

        im4.set_data(ZI.T)
        axs[1, 1].set_title('RBF interpolation')
    return im1, im2, im3, im4


ani = animation.FuncAnimation(fig, animate, frames=AlldataDF.shape[0],
                            interval = 1,
                            blit = True)

#plt.show()
writergif = animation.PillowWriter(fps=15)
ani.save('Sensor_Layer_'+str(Layer)+'.gif',writer=writergif)