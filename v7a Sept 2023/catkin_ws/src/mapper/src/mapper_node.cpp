#include <ros/ros.h>
#include <sensor_msgs/PointCloud2.h>
#include <octomap/octomap.h>
#include <octomap_ros/conversions.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <fstream>
#include <sstream>

class OctomapMapper {
public:

    OctomapMapper() : nh("~"), octree(0.1) { //0.1mm resolution
        velodyne_sub = nh.subscribe("/velodyne_points", 10, &OctomapMapper::pointCloudCallback, this); // subscribe to velodyne
    }

    ~OctomapMapper() {
        saveMap("octomap.bt");
    }

    void saveMap(const std::string& filename) { // save map
        octree.writeBinary(filename);
        ROS_INFO("Saved OctoMap to %s", filename.c_str());
    }

    void pointCloudCallback(const sensor_msgs::PointCloud2ConstPtr& cloud_msg) {

        // convert pointcloud2 to PCL pointcloud
        pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
        pcl::fromROSMsg(*cloud_msg, *cloud);

        // convert PCL pointcloud to octomap pointcloud
        octomap::Pointcloud octomapCloud;
        for (auto& pt : cloud->points) {
            octomapCloud.push_back(pt.x, pt.y, pt.z);
        }

        // insert octomap pointcloud into octree
        octomap::point3d sensorOrigin(0, 0, 0);
	    octree.insertPointCloud(octomapCloud, sensorOrigin);

        octree.updateInnerOccupancy(); // update
    }

    void spin() {
        ros::spin();
    }

private:
    ros::NodeHandle nh;
    ros::Subscriber velodyne_sub;
    octomap::OcTree octree;
};

int main(int argc, char** argv) {
    ros::init(argc, argv, "octomap_mapper");
    OctomapMapper mapper;
    mapper.spin();
    return 0;
}