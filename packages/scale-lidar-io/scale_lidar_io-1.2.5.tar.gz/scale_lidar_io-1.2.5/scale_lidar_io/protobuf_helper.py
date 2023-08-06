from collections import defaultdict
import numpy as np
from pyquaternion import Quaternion
from typing import List

from google.protobuf.json_format import MessageToDict
from .lidar_frame_1_pb2 import CameraImage, LidarFrame

from .transform import Transform


# Protobuf Helpers

def create_scene_from_protobufs(scene, protobufs: List[str]):
    """
    Create a LidarScene object from a list of protobuf files
    Args:
        scene: LidarScene object
        protobufs: List of filepaths to the protobuf files

    Returns: The updated LidarScene

    """
    for frame_num, protobuf in enumerate(protobufs):
        with open(protobuf, "rb") as f:
            frame = LidarFrame.FromString(f.read())

        pose = Transform.from_Rt(
            R=Quaternion(
                frame.device_heading.w,
                frame.device_heading.x,
                frame.device_heading.y,
                frame.device_heading.z,
            ),
            t=[
                frame.device_position.x,
                frame.device_position.y,
                frame.device_position.z,
            ],
        )

        # Group points by device ID
        points_by_sensor = defaultdict(list)
        for point in frame.points:
            sensor_id = getattr(point, "d", 0)
            points_by_sensor[sensor_id].append(point)

        for sensor_id, lidar_points in points_by_sensor.items():
            points = np.asarray([[p.x, p.y, p.z, p.i] for p in lidar_points])
            scene.get_frame(frame_num).add_points(points, sensor_id=sensor_id)

        scene.get_frame(frame_num).apply_transform(pose)

        for camera in frame.images:
            camera_num = camera.camera_index
            image_url = camera.image_url

            # Calibrate cameras once
            if frame_num == 0:
                calibrate_camera(scene, camera)

            scene.get_frame(frame_num).get_image(camera_num).load_file(image_url)

    return scene


def calibrate_camera(scene, camera: CameraImage):
    camera_pose = Transform.from_Rt(
        R=Quaternion(
            camera.heading.w,
            camera.heading.x,
            camera.heading.y,
            camera.heading.z,
        ),
        t=[camera.position.x, camera.position.y, camera.position.z],
    )

    distortion_model = camera.WhichOneof("camera_intrinsics")
    intrinsics = getattr(camera, distortion_model)

    # Protobuf supports xi for omnidirectional but not supported by calibrate
    if hasattr(intrinsics, "xi"):
        print('NOTE: For omnnidirectional intrinsics, xi is not supported.')

    intrinsics_params = MessageToDict(intrinsics)

    scene.get_camera(camera.camera_index).calibrate(
        pose=camera_pose, **intrinsics_params
    )
