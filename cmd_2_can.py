import time
import rospy
from geometry_msgs.msg import Twist
from can_msgs.msg import Frame

PERC = 0.386

class Cmd2can:
    def __init__(self):
        self.__line_x = 0
        self.__angle_z = 0
        self.__pub_cmd_vel = None #:
        self.__start = False
        pass

    def cmd_callback(self,data:Twist):
        x_speed=data.linear.x
        z_speed=data.angular.z
        l_speed = (x_speed+z_speed)/2
        r_speed = (x_speed-z_speed)/2
        l_turn = l_speed/PERC
        r_turn = r_speed/PERC
        l_turn = l_turn*8192/3000
        r_turn = r_turn * 8192 / 3000
        print(hex(int(l_turn)))



    def start(self):
        print("start init this node")
        rospy.init_node("cmd_vel_2_can", disable_signals=True)
        rospy.loginfo("init node ok!!")
        rospy.Subscriber("/cmd_vel",Twist,self.cmd_callback)
        self.__pub_cmd_vel = rospy.Publisher("/sent_messages",Frame,queue_size=100)

        try:
            while not rospy.is_shutdown():
                time.sleep(0.05)

        except KeyboardInterrupt as e:
            print("quit by user " + str(e))


if __name__=="__main__":
    cmd_ins = Cmd2can()
    cmd_ins.start()