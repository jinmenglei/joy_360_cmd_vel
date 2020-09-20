import time
import rospy
from geometry_msgs.msg import Twist
from can_msgs.msg import Frame

PERC = 0.386

class Cmd2can:
    def __init__(self):
        self.__line_x = 0
        self.__angle_z = 0
        self.__pub_can_vel = None #:
        self.__start = False
        pass

    def cmd_callback(self,data:Twist):
        x_speed=data.linear.x
        z_speed=data.angular.z

        l_speed = (x_speed+z_speed)/2
        r_speed = (x_speed-z_speed)/2

        l_turn = l_speed/PERC
        r_turn = r_speed/PERC

        l_turn = l_turn*8192/3000 *60
        r_turn = r_turn * 8192 / 3000 *60

        l_turn_data_byte = int(l_turn).to_bytes(4, byteorder='big', signed=True)
        r_turn_data_byte = int(r_turn).to_bytes(4, byteorder='big', signed=True)

        send_data = Frame()
        send_data.dlc = 8
        send_data.id = 2
        send_data.data = [0x00, 0xDA, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00]

        send_data.data[4] = l_turn_data_byte[0]
        send_data.data[5] = l_turn_data_byte[1]
        send_data.data[6] = l_turn_data_byte[2]
        send_data.data[7] = l_turn_data_byte[3]

        self.__pub_can_vel.publish(send_data)

        send_data.id = 3
        send_data.data[4] = r_turn_data_byte[0]
        send_data.data[5] = r_turn_data_byte[1]
        send_data.data[6] = r_turn_data_byte[2]
        send_data.data[7] = r_turn_data_byte[3]

        self.__pub_can_vel.publish(send_data)




    def start(self):
        print("start init this node")
        rospy.init_node("cmd_vel_2_can", disable_signals=True)
        rospy.loginfo("init node ok!!")
        rospy.Subscriber("/cmd_vel",Twist,self.cmd_callback)
        self.__pub_can_vel = rospy.Publisher("/sent_messages",Frame,queue_size=100)

        try:
            while not rospy.is_shutdown():
                time.sleep(0.05)

        except KeyboardInterrupt as e:
            print("quit by user " + str(e))


if __name__=="__main__":
    # data = -100
    # data_byte = data.to_bytes(4, byteorder='big', signed=True)
    # print(data_byte[1])
    # exit(0)
    cmd_ins = Cmd2can()
    cmd_ins.start()