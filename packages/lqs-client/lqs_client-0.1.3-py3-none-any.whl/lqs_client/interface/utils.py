from collections import OrderedDict
import io
import os
import logging
from uuid import UUID
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

import av
from lqs_client.interface.ark_deserialization import extract_ark_message_from_bytes
from lqs_client.interface.ros_deserialization import CustomROSDeserializer

import numpy as np
from PIL import Image as ImagePIL
from sensor_msgs.msg import Image, CompressedImage

logging.basicConfig(
    level=os.getenv("LQS_LOG_LEVEL") or logging.INFO,
    format="%(asctime)s  (%(levelname)s - %(name)s): %(message)s",
)
logger = logging.getLogger(__name__)


class S3Resource(str, Enum):
    extraction = "extraction"
    ingestion = "ingestion"
    log = "log"
    record = "record"
    topic = "topic"


class Utils:
    def __init__(self, getter, s3, gen, config):
        self._getter = getter
        self._s3 = s3
        self._gen = gen
        self._config = config
        self._cached_ingestions = {}
        self._cached_message_types = {}
        self._cached_topics = {}

        if self._config.get("aws_access_key_id"):
            self._use_s3_directly = True
        else:
            self._use_s3_directly = False

        if self._config.get("verbose"):
            logger.setLevel(logging.DEBUG)

    def upload_part(
        self,
        resource: S3Resource,
        resource_id: UUID,
        file_path: str,
        upload_id: str,
        part_number: int,
        key: str = None,
        part_size: int = 5 * 1024 * 1024,
    ):
        file = open(file_path, "rb")
        file.seek((part_number - 1) * part_size)
        part_data = file.read(part_size)

        logger.debug(f"Uploading part {part_number} ({len(part_data)} bytes)")

        if key is None:
            key = file_path.split("/")[-1]

        r_headers, r_params, r_body = self._s3.upload_part(
            resource=resource,
            resource_id=resource_id,
            key=key,
            part_number=part_number,
            upload_id=upload_id,
            body=part_data,
        )
        e_tag = r_headers["ETag"]
        return {"PartNumber": part_number, "ETag": e_tag}

    def upload(
        self,
        resource: S3Resource,
        resource_id: UUID,
        file_path: str,
        key: str = None,
        part_size: int = 5 * 1024 * 1024,
        max_workers: int = 8,
        exist_ok: bool = False,
    ):
        if key is None:
            key = file_path.split("/")[-1]

        if not exist_ok:
            r_headers, r_params, r_body = self._s3.head_object(
                resource=resource, resource_id=resource_id, key=key
            )
            logger.debug(f"HEAD {resource} ({resource_id}): {key} - {r_body}")
            if r_body["exists"]:
                raise FileExistsError(f"File already exists in S3: {key}")

        logger.debug("Uploading %s to %s", file_path, key)
        logger.debug("Creating multipart upload for %s %s", resource, resource_id)
        (
            _create_mpu_headers,
            _create_mpu_params,
            create_mpu_body,
        ) = self._s3.create_multipart_upload(
            resource=resource, resource_id=resource_id, key=key
        )
        try:
            upload_id = create_mpu_body["InitiateMultipartUploadResult"]["UploadId"]
            logger.debug("Upload ID: %s", upload_id)
        except KeyError as e:
            logger.error("Error creating multipart upload: %s", create_mpu_body)
            raise e

        file = open(file_path, "rb")
        file_size = os.fstat(file.fileno()).st_size
        part_count = (file_size // part_size) + 1
        logger.debug("File size: %s", file_size)
        logger.debug("Part size: %s", part_size)

        parts = []
        futures = []
        logger.debug("Uploading parts with %s workers", max_workers)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(part_count):
                part_number = i + 1
                future = executor.submit(
                    self.upload_part,
                    resource=resource,
                    resource_id=resource_id,
                    file_path=file_path,
                    upload_id=upload_id,
                    part_number=part_number,
                    key=key,
                    part_size=part_size,
                )
                futures.append(future)

        for future in futures:
            parts.append(future.result())
            logger.debug("Uploaded part %s of %s", len(parts), part_count)

        logger.debug("Completing multipart upload")
        (
            _complete_mpu_headers,
            _complete_mpu_params,
            complete_mpu_body,
        ) = self._s3.complete_multipart_upload(
            resource=resource,
            resource_id=resource_id,
            key=key,
            upload_id=upload_id,
            parts=parts,
        )
        logger.debug("Completed multipart upload %s", complete_mpu_body)

    # Message Processing

    def get_message_data_from_record(self, record):
        ingestion_id = record["ingestion_id"]
        s3_bucket = record["s3_bucket"]
        s3_key = record["s3_key"]
        if s3_bucket is None or s3_key is None:
            # the record doesn't have the s3 bucket and key, so we need to get them from the ingestion
            if ingestion_id is None:
                raise ValueError(
                    "No S3 bucket or key and no ingestion is available on record."
                )
            elif ingestion_id in self._cached_ingestions:
                ingestion = self._cached_ingestions[ingestion_id]
            elif ingestion_id is not None:
                ingestion = self._getter.ingestion(ingestion_id)["data"]
                self._cached_ingestions[ingestion_id] = ingestion

            s3_bucket = ingestion["s3_bucket"]
            s3_key = ingestion["s3_key"]
            if s3_bucket is None or s3_key is None:
                raise ValueError("No S3 bucket or key available on record's ingestion.")

        message_data = self._s3.get_message_data_from_record(
            record=record, s3_bucket=s3_bucket, s3_key=s3_key, ingestion_id=ingestion_id
        )

        return message_data

    def get_message_class(self, message_type_id):
        if message_type_id in self._cached_message_types:
            message_type = self._cached_message_types[message_type_id]
        else:
            message_type = self._getter.message_type(message_type_id)["data"]
            self._cached_message_types[message_type_id] = message_type

        message_type_name = message_type["name"]
        if "_generated" not in message_type or True:
            self._gen.process_message_definition(
                message_type["definition"], *message_type_name.split("/")
            )
            self._gen.generate_messages()
            self._cached_message_types[message_type_id]["_generated"] = True

        message_class = self._gen.get_message_class(message_type_name)
        return message_class

    def get_ros_message_from_message_data(
        self, message_data, schema_registry, message_type
    ):
        if schema_registry is None:
            return None
        deserializer = CustomROSDeserializer(msg_definitions_dict=schema_registry)
        return deserializer.deserialize(message_type=message_type, bytes=message_data)

    def get_ros_message_from_record(self, record):
        message_data = self.get_message_data_from_record(record=record)
        (
            schema_registry,
            package_name,
            message_class_name,
        ) = self.get_schema_registry_from_record(record=record)
        message_data_dict = self.get_ros_message_from_message_data(
            message_data=message_data,
            schema_registry=schema_registry,
            message_type=f"{package_name}/{message_class_name}",
        )
        if not message_data_dict:
            # get the message class
            message_class = self.get_message_class(
                message_type_id=record["message_type_id"]
            )
            # deserialize the message
            message_data_dict = message_class().deserialize(message_data)
        return message_data_dict, message_class_name

    def get_schema_registry_from_record(self, record):
        topic_id = record["topic_id"]
        if topic_id in self._cached_topics:
            topic = self._cached_topics[topic_id]
        else:
            topic = self._getter.topic(record["topic_id"])["data"]
            self._cached_topics[topic_id] = topic
        package_name, message_class_name = topic["type_name"].rsplit("/", 1)
        schema_registry = topic["type_schema"]
        if schema_registry:
            for k, v in schema_registry.items():
                if isinstance(v, list):
                    # load it as a OrderedDict
                    schema_registry[k] = OrderedDict(v)
        return schema_registry, package_name, message_class_name

    def get_image_from_ros_message(
        self, message, image_mode=None, message_class_name=None
    ):
        # We assume that if the message class name is "Image" or "CompressedImage",
        # then the message type matches the ROS message type.
        if not isinstance(message, dict):
            message_class_name = message.__class__.__name__
            message = {
                "data": message.data,
                "width": message.width,
                "height": message.height,
                "encoding": message.encoding,
            }
            if hasattr(message, "format"):
                message["format"] = message.format

        if isinstance(message["data"], list):
            message["data"] = bytes(message["data"])

        if message_class_name == "Image":
            img_modes = {
                "16UC1": "I;16",
                "mono8": "L",
                "mono16": "I;16",
                "32FC1": "F",
                "8UC1": "L",
                "8UC3": "RGB",
                "rgb8": "RGB",
                "bgr8": "RGB",
                "rgba8": "RGBA",
                "bgra8": "RGBA",
                "bayer_rggb": "L",
                "bayer_rggb8": "L",
                "bayer_gbrg": "L",
                "bayer_gbrg8": "L",
                "bayer_grbg": "L",
                "bayer_grbg8": "L",
                "bayer_bggr": "L",
                "bayer_bggr8": "L",
                "yuv422": "YCbCr",
                "yuv411": "YCbCr",
            }
            if image_mode is None:
                if not message["encoding"]:
                    logger.warn(f"No encoding: {message['encoding']}")
                    return None
                image_mode = img_modes[message["encoding"]]
            img = ImagePIL.frombuffer(
                image_mode,
                (message["width"], message["height"]),
                message["data"],
                "raw",
                image_mode,
                0,
                1,
            )
            if message["encoding"] == "bgr8":
                b, g, r = img.split()
                img = ImagePIL.merge("RGB", (r, g, b))

            if message["encoding"] in ["mono16", "16UC1", "32FC1"]:
                pixels = np.asarray(img)
                pixel_range = np.max(pixels) - np.min(pixels)
                if pixel_range == 0:
                    pixels *= 0
                else:
                    pixels = ((pixels - np.min(pixels)) / pixel_range) * 255.0
                img = ImagePIL.fromarray(pixels)
                img = img.convert("L")
        elif message_class_name == "CompressedImage":
            if message["format"] == "h264":
                codec = av.CodecContext.create("h264", "r")
                packets = av.packet.Packet(message["data"])
                img = codec.decode(packets)[0].to_image()
            else:
                img = ImagePIL.open(io.BytesIO(message["data"]))
        else:
            raise NotImplementedError(
                f"Message type {type(message)} not supported for image conversion."
            )

        return img

    def process_image(
        self,
        img,
        format="PNG",
        output_path=None,
        resize_width=None,
        resize_height=None,
        resize_scale=None,
    ):
        if (
            resize_width is not None
            or resize_height is not None
            or resize_scale is not None
        ):
            width = img.width
            height = img.height
            if resize_width is not None:
                width = resize_width
            if resize_height is not None:
                height = resize_height
            if resize_scale is not None:
                width = int(width * resize_scale)
                height = int(height * resize_scale)
            img = img.resize((width, height))

        if output_path is not None:
            img.save(output_path, format)
            return None
        else:
            buffered_img = io.BytesIO()
            img.save(buffered_img, format)
            buffered_img.seek(0)
            return buffered_img

    def get_image_from_record(self, record):
        message, message_class_name = self.get_ros_message_from_record(record=record)
        return self.get_image_from_ros_message(
            message, message_class_name=message_class_name
        )

    def get_processed_image_from_record(self, record):
        img = self.get_image_from_record(record)
        return self.process_image(img)

    def get_image_from_ark_json_msg(self, message, image_format=None):
        data = bytes(message["data"])

        if image_format is None:
            image_format = message["data_format"]

        image_format = image_format.lower()

        if image_format == "depthz16":
            ark_img = np.frombuffer(data, dtype=np.float16)
            pixel_range = np.max(ark_img) - np.min(ark_img)

            if pixel_range != 0:
                ark_img = ((ark_img - np.min(ark_img)) / pixel_range) * 65535.0

            ark_img = ark_img.astype(np.uint16)
            data = ark_img
            image_mode = "I;16"
        elif image_format == "grey":
            image_mode = "L"
        elif image_format == "rgb" or image_format == "bgr":
            image_mode = "RGB"
        elif image_format == "rgba" or image_format == "bgra":
            image_mode = "RGBA"
        elif image_format == "h264":
            codec = av.CodecContext.create("h264", "r")
            packets = av.packet.Packet(message.data)
            img = codec.decode(packets)[0].to_image()
            return img
        else:
            raise NotImplementedError(
                f"Message type {type(image_mode)} not supported for image conversion."
            )

        img = ImagePIL.frombuffer(
            image_mode,
            (message["width"], message["height"]),
            data,
            "raw",
            image_mode,
            0,
            1,
        )

        if image_format == "bgr":
            b, g, r = img.split()
            img = ImagePIL.merge("RGB", (r, g, b))
        elif image_format == "bgra":
            b, g, r, a = img.split()
            img = ImagePIL.merge("RGBA", (r, g, b, a))
        return img

    def get_ark_message_from_record(self, record):
        message_data = self._s3.get_message_data_for_ark_record(record=record)
        topic_id = record["topic_id"]
        if topic_id in self._cached_topics:
            topic = self._cached_topics[topic_id]
        else:
            topic = self._getter.topic(record["topic_id"])["data"]
            self._cached_topics[topic_id] = topic

        ark_json_msg = extract_ark_message_from_bytes(topic, message_data)
        return ark_json_msg

    def get_image_from_ark_record(self, record, image_format=None):
        ark_json_msg = self.get_ark_message_from_record(record)
        img = self.get_image_from_ark_json_msg(ark_json_msg, image_format=image_format)
        return img
