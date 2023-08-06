import numpy as np

from fusion_engine_client.messages import PoseMessage, PoseAuxMessage
from fusion_engine_client.parsers import FusionEngineEncoder
from fusion_engine_client.utils import trace as logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('point_one').setLevel(logging.DEBUG)


P1_POSE_MESSAGE1 = b".1\x00\x00\xc0@\xdb\x1a\x02\x01\x10'\x00\x00\x00\x00\x8c\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f"
P1_POSE_MESSAGE2 = b".1\x00\x00q\x95\xfd\x8a\x02\x01\x10'\x01\x00\x00\x00\x8c\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x08@\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f"
P1_POSE_AUX_MESSAGE3 = b".1\x00\x00\xac\xa4\x08\x94\x02\x00\x13'\x02\x00\x00\x00\xa0\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f\x00\x00\xc0\x7f"


def test_pose_encode():
    encoder = FusionEngineEncoder()
    pose = PoseMessage()
    pose.velocity_body_mps = np.array([1.0, 2.0, 3.0])
    pose_aux = PoseAuxMessage()

    data = encoder.encode_message(pose)
    assert data == P1_POSE_MESSAGE1
    data = encoder.encode_message(pose)
    assert data == P1_POSE_MESSAGE2
    data = encoder.encode_message(pose_aux)
    assert data == P1_POSE_AUX_MESSAGE3
