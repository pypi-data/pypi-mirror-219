import os
import yaml

CACHE_DIR_NAME = '.fro_config'


class ArmCameraParams:
    """机械臂相机参数
    """

    def __init__(self, default_dir=None) -> None:
        if default_dir is None:
            if not os.access(os.path.expanduser('~'), os.W_OK):
                default_dir = os.path.join('/tmp', CACHE_DIR_NAME)
            else:
                default_dir = os.path.join(os.path.expanduser('~'),
                                           CACHE_DIR_NAME)
        self._default_dir = default_dir
        self.config_file = os.path.join(self._default_dir,
                                        'camera_params.yaml')
        os.makedirs(self._default_dir, exist_ok=True)

    def save(self, params):
        with open(self.config_file, 'w', encoding="utf-8") as f:
            yaml.dump(params, f)

    def load(self, path=None):
        if path is None:
            path = self.config_file
        with open(path, 'r', encoding='utf-8') as f:
            params = yaml.load(f, Loader=yaml.Loader)
        return params
