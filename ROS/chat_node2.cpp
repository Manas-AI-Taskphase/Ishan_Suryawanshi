#include <ros/ros.h>
#include <std_msgs/String.h>
#include <iostream>
#include <thread>

class Node2 {
public:
    Node2() {
        // Initialize ROS
        ros::NodeHandle nh;

        // Prompt for username
        std::cout << "Enter your username for Node2: ";
        std::getline(std::cin, username_);

        // Advertise and subscribe to the chat topic
        pub_ = nh.advertise<std_msgs::String>("chat", 10);
        sub_ = nh.subscribe("chat", 10, &Node2::messageCallback, this);

        // Inform that user has joined the chat
        std::cout << username_ << " joined the chat." << std::endl;

        // Start the publishing thread
        publishThread_ = std::thread(&Node2::publishMessages, this);

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
            std::cout << "Message received from Node1: " << msg->data << std::endl;
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
    ros::init(argc, argv, "node2");
    Node2 node2;

    return 0;
}
