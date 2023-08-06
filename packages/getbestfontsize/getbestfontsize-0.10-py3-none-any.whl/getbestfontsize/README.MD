# Determines the appropriate font size for given text and constraints

## pip install getbestfontsize 

#### Tested against Windows 10 / Python 3.10 / Anaconda 


### Automated Font Size Calculation: 

The module automates the process of determining the appropriate font size for given text and constraints. This saves users from manually testing different font sizes and ensures a faster and more accurate selection.

### Flexibility with Constraints: 

Users can specify maximum width and height constraints for the text, allowing them to control how the text fits within the given space.

### Optimal Text Rendering: 

By providing the best-fitted font size, this module helps ensure that text appears legible and visually appealing, no matter the context or screen size.

### Efficient Caching: 

The lru_cache decorator helps optimize the loading of fonts by caching previously loaded fonts, reducing the need to reload the same font multiple times during the same execution.

### Dynamic and Adaptive: 

The module can adapt to different font files and text content, making it suitable for a wide range of fonts and text strings.




## HashList

```python
# Example usage:
from getbestfontsize import calculate_text_size
text = "Hello, World!"
fs = calculate_text_size(
    text,
    font_path=r"C:\Users\hansc\Downloads\CALIBRIB.TTF",
    max_width=None,
    max_height=100,
    startfont=10,
)
print(fs)


```