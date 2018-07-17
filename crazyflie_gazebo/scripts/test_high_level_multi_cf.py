#!/usr/bin/env python

import rospy
import crazyflie
import time
import uav_trajectory

if __name__ == '__main__':
    rospy.init_node('test_high_level_multi_cf')
    listcf = [crazyflie.Crazyflie("cf1", "/cf1") , crazyflie.Crazyflie("cf2", "/cf2") , crazyflie.Crazyflie("cf3", "/cf3") , crazyflie.Crazyflie("cf_11", "/cf_11")]
    # listcf = [crazyflie.Crazyflie("cf1", "/cf1") , crazyflie.Crazyflie("cf2", "/cf2") , crazyflie.Crazyflie("cf3", "/cf3") , crazyflie.Crazyflie("cf_11", "/cf_11")]
    #cf1 = crazyflie.Crazyflie("cf1", "/cf1")
    #cf2 = crazyflie.Crazyflie("cf2", "/cf2")

    for cf_i in listcf :
        cf_i.setParam("commander/enHighLevel", 1)

    time.sleep(1.0)

    for cf_i in listcf:
        cf_i.takeoff(targetHeight = 0.5, duration = 10.0)
    time.sleep(7.0)

    for cf_i in listcf:
        cf_i.goTo(goal = [0.5, 0.0, 0.0], yaw=0.2, duration = 2.0, relative = True)
    time.sleep(7.0)

    for cf_i in listcf:
        cf_i.land(targetHeight = 0.0, duration = 2.0)
    time.sleep(7.0)
    
    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv("takeoff.csv")

    traj2 = uav_trajectory.Trajectory()
    traj2.loadcsv("figure8.csv")

    print(traj1.duration)

    for cf_i in listcf:
        cf_i.uploadTrajectory(0, 0, traj1)
        cf_i.uploadTrajectory(1, len(traj1.polynomials), traj2)

    for cf_i in listcf:
        cf_i.startTrajectory(0, timescale=1.0)
    time.sleep(traj1.duration * 2.0)

    for cf_i in listcf:
        cf_i.startTrajectory(1, timescale=2.0)
    time.sleep(traj2.duration * 2.0)

    for cf_i in listcf:
        cf_i.startTrajectory(0, timescale=1.0, reverse=True)
    time.sleep(traj1.duration * 1.0)

    for cf_i in listcf:
        cf_i.stop()
