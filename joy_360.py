import time
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class Joy360:
    def __init__(self):
        self.__line_x = 0
        self.__angle_z = 0
        self.__pub_cmd_vel = None #:
        self.__start = False
        pass

    def joy_callback(self,data:Joy):
        if data.buttons[7] == 1:
            self.__start = not self.__start
        # rospy.loginfo(str(data.axes))
        self.__line_x = data.axes[4]
        self.__angle_z = data.axes[0]

    def start(self):
        print("start init this node")
        rospy.init_node("joy_360_cmd", disable_signals=True)
        rospy.loginfo("init node ok!!")
        rospy.Subscriber("/joy",Joy,self.joy_callback)
        self.__pub_cmd_vel = rospy.Publisher("/cmd_vel",Twist,queue_size=100)

        try:
            while not rospy.is_shutdown():
                time.sleep(0.05)
                if self.__start:
                    data_pub = Twist()
                    data_pub.linear.x = self.__line_x
                    data_pub.angular.z = self.__angle_z
                    self.__pub_cmd_vel.publish(data_pub)

        except KeyboardInterrupt as e:
            print("quit by user " + str(e))


if __name__=="__main__":
    joy_ins = Joy360()
    joy_ins.start()