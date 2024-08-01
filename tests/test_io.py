import os
import pytest

def assert_tiff(path, shape, levels=4):
    from tiff_utils.image_readers import get_image_reader

    # assert pyramidal structure
    for level in range(levels):
        with get_image_reader(path, level=level) as f:
            assert f.X <= shape[0]
            assert f.Y <= shape[1]
            assert len(f.shape) == 5
            assert len(f.read(T=0, C=0).shape) == 2
            shape = (f.X, f.Y)

    # assert pyramidal depth
    def try_read():
        with get_image_reader(path, level=levels + 1) as f:
            return f.read(T=0, C=0)
    pytest.raises(ValueError, try_read)


def test_convert(path_dice, path_temp):
    from tiff_utils import convert_to_tiff

    # convert
    convert_to_tiff(
        path_dice,
        path_temp,
        subresolutions=3,
    )
    assert os.path.exists(path_temp)

    # read
    assert_tiff(path_temp, shape=(640, 480), levels=3)


def test_store(path_temp, random_img):
    from tiff_utils import write_tiff

    # save
    write_tiff(random_img, path_temp, subresolutions=5)
    assert_tiff(path_temp, shape=random_img.shape, levels=5)
