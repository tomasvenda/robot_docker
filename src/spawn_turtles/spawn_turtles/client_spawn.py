import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
import time
from geometry_msgs.msg import Twist

class TurtleSpawner(Node):
    def __init__(self):
        super().__init__('turtle_spawner')
        self.client = self.create_client(Spawn, '/spawn')

        # Wait for the service to be available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for spawn service...')

        self.turtle_names = []

        self.velocity_publishers = {}

        self.spawn_turtles()

        for turtle in self.turtle_names:
            pub = self.create_publisher(Twist, f'/{turtle}/cmd_vel', 10)
            self.velocity_publishers[turtle] = pub

        self.timer = self.create_timer(0.5, self.move_turtles)


    def spawn_turtles(self):
        """Spawn 10 turtles in different positions"""
        for i in range(10):
            turtle_name = f'turtle{i+1}'
            x, y, theta = (2.0 + i * 0.5, 2.0 + i * 0.5, 0.0)

            request = Spawn.Request()
            request.x = x
            request.y = y
            request.theta = theta
            request.name = turtle_name

            self.get_logger().info(f'Spawning {turtle_name} at ({x}, {y})')

            future = self.client.call_async(request)
            rclpy.spin_until_future_complete(self, future)

            if future.result() is not None:
                self.get_logger().info(f'Successfully spawned {turtle_name}')
                self.turtle_names.append(turtle_name)
            else:
                self.get_logger().error(f'Failed to spawn {turtle_name}')
            
            time.sleep(1)  # Small delay to prevent flooding the service

    def move_turtles(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 1.0
        
        for turtle, publisher in self.velocity_publishers.items():
                publisher.publish(msg)
                self.get_logger().info(f'Moving {turtle} in a circle')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
