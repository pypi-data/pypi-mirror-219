import io
import mimetypes
import os

import boto3
from boto3.session import Session
from typing import Optional, List
from PIL import Image
from .pdfhandler import pdf_to_image


class BotAWSTextractPlugin:
    def __init__(self, region_name: Optional[str] = 'us-east-1', use_credentials_file: Optional[bool] = True,
                 access_key_id: Optional[str] = None, secret_access_key: Optional[str] = None) -> None:
        """
        BotAWSTextractPlugin

        Args:
            region_name (str): Default region when creating new connections.
            use_credentials_file (bool, optional): If set to True will make
                authentication via AWS credentials file.
            access_key_id (str, optional): AWS access key ID.
            secret_access_key (str, optional): AWS secret access key.
        """
        if use_credentials_file:
            self._client = boto3.client(service_name='textract')
        else:
            self._client = boto3.client(
                service_name='textract',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name
            )

        self._render_rate = 72
        self._full_text = ""
        self._entries = []

    @property
    def textract_client(self) -> Session.client:
        """
        Returns the aws client instance.

        Returns:
            boto3_instance: The aws client instance.
        """
        return self._client

    @property
    def render_rate(self) -> int:
        """
        The render resolution rate

        Returns:
            int: resolution rate
        """
        return self._render_rate

    @render_rate.setter
    def render_rate(self, rate: int):
        """
        Sets the render resolution rate.

        Args:
            rate (int): resolution rate
        """
        self._render_rate = rate

    @property
    def entries(self) -> List[List]:
        """
        Get the list of entries after reading the file.

        Each element contains a list of values in which are:
        `text`, `x1`, `y1`, `x2`, `y2`, `x3`, `y3`, `x4`, `y4` and `page`.

        Returns:
            List[List]: List of entries.
       """
        return self._entries

    def full_text(self) -> str:
        """
        Get the full text from the image.

        Returns:
            str: The full text.
        """
        return self._full_text

    def read(self, filepath: str, **kwargs) -> "BotAWSTextractPlugin":
        """
        Read the file and set the entries list.

        Args:
          filepath (str): The file path for the image or PDF to be read.

        Raises:
            ValueError: If file is not an image or PDF.
        """
        # reset the entries list
        self._entries = []

        if not mimetypes.inited:
            mimetypes.init()
        file_type = mimetypes.guess_type(filepath)[0]

        images = []
        if "/pdf" in file_type:
            images.extend(pdf_to_image(filepath, resolution=self._render_rate))
        elif "image/" in file_type:
            images.append(Image.open(filepath))
        else:
            raise ValueError("Invalid file type. Only images and PDFs are accepted.")

        page_heights = []
        for page_idx, page in enumerate(images, start=1):
            buffer = io.BytesIO()
            page.save(buffer, format='PNG')

            response = self._client.analyze_document(
                Document={'Bytes': buffer.getvalue()},
                FeatureTypes=['FORMS'],
                **kwargs
            )

            page_width, page_height = page.size
            page_heights.append(page_height)

            page_offset = 0 if page_idx == 1 else page_heights[page_idx - 2]
            for block in response["Blocks"]:
                if block["BlockType"] == "WORD":
                    self._full_text += block["Text"] + os.linesep
                    bb = block["Geometry"]["BoundingBox"]

                    # bb.left * page_width
                    x1 = bb["Left"] * page_width

                    # bb.top * page_height
                    y1 = (bb["Top"] * page_height) + page_offset

                    # bb.width * page_width + (bb.left * page_width)
                    x3 = (bb["Width"] * page_width) + x1

                    # bb.height * page_height + (bb.top * page_height)
                    y3 = ((bb["Height"] * page_height) + y1 + page_offset)

                    self._entries.append([
                        block["Text"],
                        x1, y1,
                        x3, y1,
                        x3, y3,
                        x1, y3,
                        page_idx
                    ])
        return self
