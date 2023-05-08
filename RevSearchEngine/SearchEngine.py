from typing import Optional, List, Tuple
from DeepSearchLite import LoadData, SearchSetup
from PIL import Image

import os
import sys

# Get the absolute path of the parent directory of the script
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from RevSearchEngine.FeatureExtractor import CustomFeatureExtractor


class ImageSearchEngine:
    def __init__(
        self,
        model_path: str,
        images_dir: str,
        mode: str = "search",
        metadata_dir: str = "metadata_dir",
        feature_extractor_name: str = "feature_extractor",
        dim_reduction: Optional[int] = None,
        image_count: Optional[int] = None,
    ) -> None:
        self.images_dir = images_dir
        self.model_path = model_path
        self.mode = mode
        self.metadata_dir = metadata_dir
        self.feature_extractor_name = feature_extractor_name
        self.dim_reduction = dim_reduction
        self.image_count = image_count

    def _create_search_engine(self) -> SearchSetup:
        """
        Create a search engine instance with the given configuration.

        Returns:
            SearchSetup: An instance of the search engine.
        """
        image_list_all = LoadData().from_folder([self.images_dir])
        image_list = image_list_all[:]

        feature_extractor = CustomFeatureExtractor(model_path=self.model_path)

        search_engine = SearchSetup(
            item_list=image_list,
            feature_extractor=feature_extractor,
            dim_reduction=self.dim_reduction,
            metadata_dir=self.metadata_dir,
            feature_extractor_name=self.feature_extractor_name,
            mode=self.mode,
        )

        return search_engine

    def get_similar_images_list_from_image(
        self, image: Image.Image, number_of_images: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Get a list of similar images from the given image.

        Args:
            image (Image.Image): The input image.
            number_of_images (int, optional): The number of similar images to return. Defaults to 3.

        Returns:
            List[Tuple[str, float]]: A list of tuples containing the image path and similarity score.
        """
        search_engine = self._create_search_engine()

        similar_images = search_engine.get_similar_items(
            item=image, number_of_items=number_of_images, return_paths=True
        )

        return similar_images


def main():
    image = Image.open("/home/ibad/Desktop/RevSearch/car.jpg")
    image = image.resize((224, 224))

    MODEL_PATH = "models/efficientnet_feature_encoder.onnx"
    MODE = "search"
    IMAGES_DIR = "/home/ibad/Desktop/RevSearch/Car196_Combined/images/"
    METADATA_DIR = "cars_dataset_metadata_dir"
    FEATURE_EXTRACTOR_NAME = "efficientnet_onnx"

    image_search_engine = ImageSearchEngine(
        model_path=MODEL_PATH,
        images_dir=IMAGES_DIR,
        mode=MODE,
        metadata_dir=METADATA_DIR,
        feature_extractor_name=FEATURE_EXTRACTOR_NAME,
    )

    similar_images = image_search_engine.get_similar_images_list_from_image(image)

    print(similar_images)


if __name__ == "__main__":
    main()
