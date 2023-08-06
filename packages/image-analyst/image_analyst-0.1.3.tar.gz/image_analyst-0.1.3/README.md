# ImageAnalyst

ImageAnalyst is a library that simplifies image analysis. The library achieves this goal by standardizing the input and output
vectors of a few machine learning models and by providing some high-level analysis algorithms.

## Requirements

The application requires:

- [Python](https://www.python.org/) ~= 3.9
- [pip](https://pip.pypa.io/en/stable/)

## Extras

The application has some extras that can be installed:

- [cv2](https://github.com/BergLucas/ImageAnalystCV2)
- [hf](https://github.com/BergLucas/ImageAnalystHF)
- [tf](https://github.com/BergLucas/ImageAnalystTF)
- [onnx](https://github.com/BergLucas/ImageAnalystONNX)

## Download & Installation

There is two ways to download and install the application.

### Using PyPI

You can download and install the application using [PyPI](https://pypi.org/project/image-analyst/). To do so, run the following command:

```bash
pip install image-analyst
```

### Using the GitHub releases

You can download the application on the [downloads page](https://github.com/BergLucas/ImageAnalyst/releases). Then, you can install the application by running the following command:

```bash
pip install image_analyst-X.X.X-py3-none-any.whl
```

(Note: The X.X.X must be replaced by the version that you want to install.)

## Example

This example allows you to track objects from your webcam. It requires the `cv2` extra.

```python
from image_analyst.cv2.utils import convert_image, create_frame_generator
from image_analyst.cv2.models import YoloV3OpenCV
from image_analyst.trackers import IOUTracker
import cv2

def report_callback(filename: str, current_size: float, total_size: float):
    print("{} {:.2f}%".format(filename, current_size/total_size*100), end="\r", flush=True)

model = YoloV3OpenCV.coco(report_callback=report_callback)

tracker = IOUTracker()

with create_frame_generator(0) as frame_generator:
    for tracking_function, frame in zip(tracker(model), frame_generator):
        converted_frame = convert_image(frame, model.supported_format, model.supported_dtype)
        instances = tracking_function(converted_frame)

        for instance in instances:
            xmin, ymin, xmax, ymax = instance.bounding_box.as_tuple()

            text = "{} {} {:.2f}".format(instance.id, instance.class_name, instance.score)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(frame, text, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
```

## License

All code is licensed for others under a MIT license (see [LICENSE](https://github.com/BergLucas/ImageAnalyst/blob/main/LICENSE)).
