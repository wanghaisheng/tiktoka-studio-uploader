from scenedetect import VideoManager, SceneManager, StatsManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images, write_scene_list_html
import os

class AiThumbnailGenerator:
    def __init__(self, video_path):
        self.video_path = video_path
        self.filename=os.path.splitext(video_path)[0]
        self.video_manager = VideoManager([self.video_path])
        self.stats_manager = StatsManager()
        self.scene_manager = SceneManager(self.stats_manager)

        self.scene_manager.add_detector(ContentDetector(threshold=30))

        self.video_manager.set_downscale_factor()

        self.generate()
        self.getMainScene()

    def generate(self):
        self.video_manager.start()
        self.scene_manager.detect_scenes(frame_source=self.video_manager)

        # # result
        # with open("result.csv", 'w') as f:
        #     self.stats_manager.save_to_csv(
        #         f, self.video_manager.get_base_timecode())

    def getMainScene(self):

        scene_list = self.scene_manager.get_scene_list()

        main_scene = []

        for scene in scene_list:
            start, end = scene
            t = end.get_seconds() - start.get_seconds()
            main_scene.append([t, scene])

        sorted(main_scene, key=lambda x: x[0])

        result = []
        if len(main_scene) > 3:
            main_scene = main_scene[0:3]
        for scene in main_scene:
            result.append(scene[-1])
        print(self.filename.split(os.sep)[0],'==========')
        save_images(result, self.video_manager, num_images=1,
                    image_name_template=self.filename+'-'+'$SCENE_NUMBER', output_dir=self.filename.split(os.sep)[0])

        return self.filename+'-1.jpg'
