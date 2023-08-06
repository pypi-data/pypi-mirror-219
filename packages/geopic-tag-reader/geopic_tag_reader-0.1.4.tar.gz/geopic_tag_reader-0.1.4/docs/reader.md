<!-- markdownlint-disable -->

<a href="../geopic_tag_reader/reader.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reader`





---

<a href="../geopic_tag_reader/reader.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `readPictureMetadata`

```python
readPictureMetadata(picture: Image) → GeoPicTags
```

Extracts metadata from picture file 



**Args:**
 
 - <b>`picture`</b> (PIL.Image):  Picture file 



**Returns:**
 
 - <b>`GeoPicTags`</b>:  Extracted metadata from picture 


---

<a href="../geopic_tag_reader/reader.py#L337"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `decodeMakeModel`

```python
decodeMakeModel(value) → str
```

Python 2/3 compatible decoding of make/model field. 


---

<a href="../geopic_tag_reader/reader.py#L348"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `isExifTagUsable`

```python
isExifTagUsable(exif, tag, expectedType=<class 'str'>) → bool
```

Is a given EXIF tag usable (not null and not an empty string) 



**Args:**
 
 - <b>`exif`</b> (dict):  The EXIF tags 
 - <b>`tag`</b> (str):  The tag to check 
 - <b>`expectedType`</b> (class):  The expected data type 



**Returns:**
 
 - <b>`bool`</b>:  True if not empty 


---

<a href="../geopic_tag_reader/reader.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CropValues`
Cropped equirectangular pictures metadata 



**Attributes:**
 
 - <b>`fullWidth`</b> (int):  Full panorama width 
 - <b>`fullHeight`</b> (int):  Full panorama height 
 - <b>`width`</b> (int):  Cropped area width 
 - <b>`height`</b> (int):  Cropped area height 
 - <b>`left`</b> (int):  Cropped area left offset 
 - <b>`top`</b> (int):  Cropped area top offset 

<a href="../<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    fullWidth: int,
    fullHeight: int,
    width: int,
    height: int,
    left: int,
    top: int
) → None
```









---

<a href="../geopic_tag_reader/reader.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GeoPicTags`
Tags associated to a geolocated picture 



**Attributes:**
 
 - <b>`lat`</b> (float):  GPS Latitude (in WGS84) 
 - <b>`lon`</b> (float):  GPS Longitude (in WGS84) 
 - <b>`ts`</b> (float):  The capture date (as POSIX timestamp) 
 - <b>`heading`</b> (int):  Picture heading (in degrees, North = 0°, East = 90°, South = 180°, West = 270°) 
 - <b>`type`</b> (str):  The kind of picture (flat, equirectangular) 
 - <b>`make`</b> (str):  The camera manufacturer name 
 - <b>`model`</b> (str):  The camera model name 
 - <b>`focal_length`</b> (float):  The camera focal length (in mm) 
 - <b>`crop`</b> (CropValues):  The picture cropped area metadata (optional) 
 - <b>`exif`</b> (dict[str, str]):  Raw EXIF tags from picture 
 - <b>`tagreader_warnings`</b> (list[str]):  List of thrown warnings during metadata reading 

<a href="../<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    lat: float,
    lon: float,
    ts: float,
    heading: Optional[int],
    type: str,
    make: Optional[str],
    model: Optional[str],
    focal_length: Optional[float],
    crop: Optional[CropValues],
    exif: Dict[str, str] = <factory>,
    tagreader_warnings: List[str] = <factory>
) → None
```









---

<a href="../geopic_tag_reader/reader.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PartialExifException`
Exception for partial / missing EXIF information from image 

<a href="../geopic_tag_reader/reader.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(msg)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
