from PIL import ExifTags, TiffImagePlugin, Image
import xmltodict
import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import re
import json


@dataclass
class CropValues:
    """Cropped equirectangular pictures metadata

    Attributes:
        fullWidth (int): Full panorama width
        fullHeight (int): Full panorama height
        width (int): Cropped area width
        height (int): Cropped area height
        left (int): Cropped area left offset
        top (int): Cropped area top offset
    """

    fullWidth: int
    fullHeight: int
    width: int
    height: int
    left: int
    top: int


@dataclass
class GeoPicTags:
    """Tags associated to a geolocated picture

    Attributes:
        lat (float): GPS Latitude (in WGS84)
        lon (float): GPS Longitude (in WGS84)
        ts (float): The capture date (as POSIX timestamp)
        heading (int): Picture heading (in degrees, North = 0°, East = 90°, South = 180°, West = 270°)
        type (str): The kind of picture (flat, equirectangular)
        make (str): The camera manufacturer name
        model (str): The camera model name
        focal_length (float): The camera focal length (in mm)
        crop (CropValues): The picture cropped area metadata (optional)
        exif (dict[str, str]): Raw EXIF tags from picture
        tagreader_warnings (list[str]): List of thrown warnings during metadata reading
    """

    lat: float
    lon: float
    ts: float
    heading: Optional[int]
    type: str
    make: Optional[str]
    model: Optional[str]
    focal_length: Optional[float]
    crop: Optional[CropValues]
    exif: Dict[str, str] = field(default_factory=lambda: {})
    tagreader_warnings: List[str] = field(default_factory=lambda: [])


class PartialExifException(Exception):
    """Exception for partial / missing EXIF information from image"""

    def __init__(self, msg):
        super().__init__(msg)


def readPictureMetadata(picture: Image.Image) -> GeoPicTags:
    """Extracts metadata from picture file

    Args:
        picture (PIL.Image): Picture file

    Returns:
        GeoPicTags: Extracted metadata from picture
    """

    data = {}
    warnings = []

    rawExif = picture._getexif()  # type: ignore[attr-defined]
    if rawExif:
        for key, value in rawExif.items():
            keyName = ExifTags.TAGS.get(key, str(key))
            if keyName == "GPSInfo":
                for gpsKey in value:
                    gpsKeyName = ExifTags.GPSTAGS.get(gpsKey, str(gpsKey))
                    data[gpsKeyName] = value[gpsKey]
            else:
                data[keyName] = value

    # Read XMP tags
    for segment, content in picture.applist:  # type: ignore[attr-defined]
        if segment == "APP1":
            marker, body = content.split(b"\x00", 1)
            if marker == b"http://ns.adobe.com/xap/1.0/":
                body = body.strip(b"\00")
                description = xmltodict.parse(body)["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]
                if isinstance(description, list):
                    # there can be several rdf:Description, if that's the case, we merge them all
                    description = {k: v for d in description for k, v in d.items()}
                data.update(description)

    # Read Mapillary tags
    if "ImageDescription" in data:
        # Check if data can be read
        imgDesc = data["ImageDescription"]
        try:
            imgDescJson = json.loads(imgDesc)
            data.update(imgDescJson)
        except:
            pass

    # Cleanup tags
    for k in list(data):
        if k.startswith("@"):
            data[k[1:]] = data[k]
            del data[k]
            k = k[1:]

        if k.startswith("exif:"):
            data[k[5:]] = data[k]
            del data[k]
            k = k[5:]

    # Handle renamings
    if picture.info.get("comment"):
        data["UserComment"] = picture.info.get("comment")

    # ~ print(data)

    # Parse latitude/longitude
    if isExifTagUsable(data, "GPSLatitude", tuple) and isExifTagUsable(data, "GPSLongitude", tuple):
        latRaw = data["GPSLatitude"]
        if any(isinstance(l, TiffImagePlugin.IFDRational) and l.denominator == 0 for l in latRaw):
            raise PartialExifException("Broken GPS coordinates in picture EXIF tags")

        if not isExifTagUsable(data, "GPSLatitudeRef"):
            warnings.append("GPSLatitudeRef not found, assuming GPSLatitudeRef is North")
            latRef = 1
        else:
            latRef = -1 if data["GPSLatitudeRef"].startswith("S") else 1
        lat = latRef * (float(latRaw[0]) + float(latRaw[1]) / 60 + float(latRaw[2]) / 3600)

        lonRaw = data["GPSLongitude"]
        if any(isinstance(l, TiffImagePlugin.IFDRational) and l.denominator == 0 for l in lonRaw):
            raise PartialExifException("Broken GPS coordinates in picture EXIF tags")

        if not isExifTagUsable(data, "GPSLongitudeRef"):
            warnings.append("GPSLongitudeRef not found, assuming GPSLongitudeRef is East")
            lonRef = 1
        else:
            lonRef = -1 if data["GPSLongitudeRef"].startswith("W") else 1
        lon = lonRef * (float(lonRaw[0]) + float(lonRaw[1]) / 60 + float(lonRaw[2]) / 3600)

    elif isExifTagUsable(data, "GPSLatitude", float) and isExifTagUsable(data, "GPSLongitude", float):
        if not isExifTagUsable(data, "GPSLatitudeRef"):
            warnings.append("GPSLatitudeRef not found, assuming GPSLatitudeRef is North")
            latRef = 1
        else:
            latRef = -1 if data["GPSLatitudeRef"].startswith("S") else 1

        lat = latRef * float(data["GPSLatitude"])

        if not isExifTagUsable(data, "GPSLongitudeRef"):
            warnings.append("GPSLongitudeRef not found, assuming GPSLongitudeRef is East")
            lonRef = 1
        else:
            lonRef = -1 if data["GPSLongitudeRef"].startswith("W") else 1

        lon = lonRef * float(data["GPSLongitude"])

    elif isExifTagUsable(data, "MAPLatitude", float) and isExifTagUsable(data, "MAPLongitude", float):
        lat = float(data["MAPLatitude"])
        lon = float(data["MAPLongitude"])

    else:
        raise PartialExifException("No GPS coordinates or broken coordinates in picture EXIF tags")

    # Parse date/time
    d = None
    if isExifTagUsable(data, "GPSDateStamp"):
        try:
            dateRaw = data["GPSDateStamp"].replace(":", "-").replace("\x00", "")
            msRaw = data["SubsecTimeOriginal"] if isExifTagUsable(data, "SubsecTimeOriginal", float) else "0"

            # Time
            if isExifTagUsable(data, "GPSTimeStamp", tuple):
                timeRaw = data["GPSTimeStamp"]
            elif isExifTagUsable(data, "GPSDateTime", tuple):
                timeRaw = data["GPSDateTime"]
            else:
                raise ValueError("GPSTimeStamp and GPSDateTime don't contain supported time format")

            if timeRaw:
                d = datetime.datetime.combine(
                    datetime.date.fromisoformat(dateRaw),
                    datetime.time(
                        int(float(timeRaw[0])),  # float->int to avoid DeprecationWarning
                        int(float(timeRaw[1])),
                        int(float(timeRaw[2])),
                        int(msRaw[:6].ljust(6, "0")),
                        tzinfo=datetime.timezone.utc,
                    ),
                )

        except ValueError as e:
            warnings.append("Skipping GPS date/time as it was not recognized:\n\t" + str(e))

    if d is None and isExifTagUsable(data, "DateTimeOriginal"):
        try:
            dateRaw = data["DateTimeOriginal"].split(" ")[0].replace(":", "-")
            timeRaw = data["DateTimeOriginal"].split(" ")[1].split(":")
            msRaw = data["SubsecTimeOriginal"] if isExifTagUsable(data, "SubsecTimeOriginal", float) else "0"
            d = datetime.datetime.combine(
                datetime.date.fromisoformat(dateRaw),
                datetime.time(
                    int(timeRaw[0]),
                    int(timeRaw[1]),
                    int(timeRaw[2]),
                    int(msRaw[:6].ljust(6, "0")),
                    tzinfo=datetime.timezone.utc,
                ),
            )
        except ValueError as e:
            warnings.append("Skipping original date/time as it was not recognized:\n\t" + str(e))

    if d is None and isExifTagUsable(data, "MAPGpsTime"):
        try:
            year, month, day, hour, minutes, seconds, milliseconds = [int(dp) for dp in data["MAPGpsTime"].split("_")]
            d = datetime.datetime(
                year,
                month,
                day,
                hour,
                minutes,
                seconds,
                milliseconds * 1000,
                tzinfo=datetime.timezone.utc,
            )

        except Exception as e:
            warnings.append("Skipping Mapillary date/time as it was not recognized:\n\t" + str(e))

    if d is None:
        raise PartialExifException("No valid date in picture EXIF tags")

    # Heading
    heading = None
    if isExifTagUsable(data, "GPano:PoseHeadingDegrees", float) and isExifTagUsable(data, "GPSImgDirection", float):
        gpsDir = int(round(data["GPSImgDirection"]))
        gpanoHeading = int(round(float(data["GPano:PoseHeadingDegrees"])))
        if gpsDir > 0 and gpanoHeading == 0:
            heading = gpsDir
        elif gpsDir == 0 and gpanoHeading > 0:
            heading = gpanoHeading
        else:
            if gpsDir != gpanoHeading:
                warnings.append("Contradicting heading values found, GPSImgDirection value is used")
            heading = gpsDir

    elif isExifTagUsable(data, "GPano:PoseHeadingDegrees", float):
        heading = int(round(float(data["GPano:PoseHeadingDegrees"])))

    elif isExifTagUsable(data, "GPSImgDirection", float):
        heading = int(round(float(data["GPSImgDirection"])))

    elif "MAPCompassHeading" in data and isExifTagUsable(data["MAPCompassHeading"], "TrueHeading", float):
        heading = int(round(float(data["MAPCompassHeading"]["TrueHeading"])))

    # Make and model
    make = data.get("Make") or data.get("MAPDeviceMake")
    model = data.get("Model") or data.get("MAPDeviceModel")

    if make is not None:
        make = decodeMakeModel(make).strip()

    if model is not None:
        model = decodeMakeModel(model).strip()

    if make is not None and model is not None:
        model = model.replace(make, "").strip()

    # Focal length
    focalLength = None
    if isExifTagUsable(data, "FocalLength", float):
        focalLength = float(data["FocalLength"])

    elif isExifTagUsable(data, "FocalLength") and re.compile(r"^\d+/\d+$").match(data["FocalLength"]):
        parts = data["FocalLength"].split("/")
        focalLength = int(parts[0]) / int(parts[1])

    # Cropped pano data
    crop = None
    if (
        isExifTagUsable(data, "GPano:FullPanoWidthPixels", int)
        and isExifTagUsable(data, "GPano:FullPanoHeightPixels", int)
        and isExifTagUsable(data, "GPano:CroppedAreaImageWidthPixels", int)
        and isExifTagUsable(data, "GPano:CroppedAreaImageHeightPixels", int)
        and isExifTagUsable(data, "GPano:CroppedAreaLeftPixels", int)
        and isExifTagUsable(data, "GPano:CroppedAreaTopPixels", int)
    ):
        fw = int(data["GPano:FullPanoWidthPixels"])
        fh = int(data["GPano:FullPanoHeightPixels"])
        w = int(data["GPano:CroppedAreaImageWidthPixels"])
        h = int(data["GPano:CroppedAreaImageHeightPixels"])
        l = int(data["GPano:CroppedAreaLeftPixels"])
        t = int(data["GPano:CroppedAreaTopPixels"])

        if fw > w or fh > h:
            crop = CropValues(fw, fh, w, h, l, t)

    elif (
        isExifTagUsable(data, "GPano:CroppedAreaImageWidthPixels", int)
        or isExifTagUsable(data, "GPano:CroppedAreaImageHeightPixels", int)
        or isExifTagUsable(data, "GPano:CroppedAreaLeftPixels", int)
        or isExifTagUsable(data, "GPano:CroppedAreaTopPixels", int)
    ):
        raise PartialExifException("EXIF tags contain partial cropped area metadata")

    return GeoPicTags(
        lat,
        lon,
        d.timestamp(),
        heading,
        data["GPano:ProjectionType"] if isExifTagUsable(data, "GPano:ProjectionType") else "flat",
        make,
        model,
        focalLength,
        crop,
        exif=data,
        tagreader_warnings=warnings,
    )


def decodeMakeModel(value) -> str:
    """Python 2/3 compatible decoding of make/model field."""
    if hasattr(value, "decode"):
        try:
            return value.decode("utf-8").replace("\x00", "")
        except UnicodeDecodeError:
            return value
    else:
        return value.replace("\x00", "")


def isExifTagUsable(exif, tag, expectedType=str) -> bool:
    """Is a given EXIF tag usable (not null and not an empty string)

    Args:
        exif (dict): The EXIF tags
        tag (str): The tag to check
        expectedType (class): The expected data type

    Returns:
        bool: True if not empty
    """

    try:
        if not tag in exif:
            return False
        elif not (expectedType in [float, int] or isinstance(exif[tag], expectedType)):
            return False
        elif not (expectedType != str or len(exif[tag].strip().replace("\x00", "")) > 0):
            return False
        elif not (expectedType not in [float, int] or float(exif[tag]) is not None):
            return False
        else:
            return True
    except ValueError:
        return False
