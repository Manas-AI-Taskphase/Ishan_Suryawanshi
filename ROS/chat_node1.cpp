#include <ros/ros.h>
#include <std_msgs/String.h>
#include <iostream>
#include <thread>

class Node1 {
public:
    Node1() {
        // Initialize ROS
        ros::NodeHandle nh;

        // Prompt for username
        std::cout << "Enter your username for Node1: ";
        std::getline(std::cin, username_);

        // Advertise and subscribe to the chat topic
        pub_ = nh.advertise<std_msgs::String>("chat", 10);
        sub_ = nh.subscribe("chat", 10, &Node1::messageCallback, this);

        // Inform that user has joined the chat
        std::cout << username_ << " joined the chat." << std::endl;

        // Start the publishing thread
        publishThread_ = std::thread(&Node1::publishMessages, this);

        // Spin in the main thread to process incoming messages
        ros::spin();
    }

    void publishMessages() {
        while (ros::ok()) {
            std::string message;
            std::getline(std::cin, message);

            std_msgs::String msg;
            msg.data = "[" + username_ + "] " + message;
            pub_.publish(msg);
        }
    }

    void messageCallback(const std_msgs::String::ConstPtr& msg) {
        // Display received message from the other node
        if (msg->data.find("[" + username_ + "]") == std::string::npos) {
            std::cout << "Message received from Node2: " << msg->data << std::endl;
        }
    }

private:
    ros::NodeHandle nh_;
    ros::Publisher pub_;
    ros::Subscriber sub_;
    std::string username_;
    std::thread publishThread_;
};

int main(int argc, char** argv) {
    ros::init(argc, argv, "node1");
    Node1 node1;

    return 0;
}
