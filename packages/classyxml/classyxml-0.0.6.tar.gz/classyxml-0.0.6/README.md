
---
# ClassyXml

An xml file parser that makes the element text and attributes of an xml file accessible as ClassyXml class attributes.

## Install it from PyPI

```bash
pip install classyxml
```

## Usage

### Parsing an XML file
```xml 
<!-- countries.xml -->
<root>
  <country name="Liechtenstein">
    <rank>1</rank>
    <year>2008</year>
    <gdppc>141100</gdppc>
    <neighbor name="Austria" direction="E"/>
    <neighbor name="Switzerland" direction="W"/>
  </country>
  <country name="Singapore">
    <rank>4</rank>
    <year>2011</year>
    <gdppc>59900</gdppc>
    <neighbor name="Malaysia" direction="N"/>
  </country>
</root>
```

```py
from classy_xml import ClassyXml

# Load the countries.xml file
classy = ClassyXml('countries.xml')

# Print the XML information
print(len(classy.country))                      # Output: 2

print(classy.country[0].name)                   # Output: 'Liechtenstein'
print(classy.country[0].rank.text)              # Output: '1'
print(classy.country[0].year.text)              # Output: '2008'
print(classy.country[0].gdppc.text)             # Output: '141100'
print(len(classy.country[0].neighbor))          # Output: 2
print(classy.country[0].neighbor[0].name)       # Output: 'Austria'
print(classy.country[0].neighbor[0].direction)  # Output: 'E'
print(classy.country[0].neighbor[1].name)       # Output: 'Switzerland'
print(classy.country[0].neighbor[1].direction)  # Output: 'W'

print(classy.country[1].name)                   # Output: 'Singapore'
print(classy.country[1].rank.text)              # Output: '4'
print(classy.country[1].year.text)              # Output: '2011'
print(classy.country[1].gdppc.text)             # Output: '59900'
print(len(classy.country[1].neighbor))          # Output: 1
print(classy.country[1].neighbor.name)          # Output: 'Malaysia'
print(classy.country[1].neighbor.direction)     # Output: 'N'
```

### Generating an XML file

This will generate the *countries.xml* file illustrated above.
```py
from classy_xml import ClassyXml, XmlElement

# Create an empty ClassyXml object
classy = ClassyXml()

# Creating Liechtenstein Element
# Setting the text and attributes using the XmlElement arguments
liechtenstein = XmlElement(attributes={'name': 'Liechtenstein'})
liechtenstein.rank = XmlElement(text=1)
liechtenstein.year = XmlElement(text=2008)
liechtenstein.gdppc = XmlElement(text=141100)
liechtenstein.neighbor = XmlElement(attributes={'name': 'Austria', 'direction': 'E'})
liechtenstein.neighbor = XmlElement(attributes={'name': 'Switzerland', 'direction': 'W'})

# Creating Singapore Element
# Setting the text and attributes directly
singapore = XmlElement()
singapore.name = 'Singapore'
singapore.rank = XmlElement()
singapore.rank.text = 4
singapore.year = XmlElement()
singapore.year.text = 2011
singapore.gdppc = XmlElement()
singapore.gdppc.text = 59900
singapore.neighbor = XmlElement()
singapore.neighbor[0].name = 'Malaysia'
singapore.neighbor[0].direction = 'N'

# Add the countries to ClassyXml
classy.country = liechtenstein
classy.country = singapore

# Save the XML file
classy.save_as('countries.xml')
```

### Modifying an existing XML file

This will add a USA element to the *countries.xml* file illustrated above.

```py
from classy_xml import ClassyXml, XmlElement

# Load the countries.xml file
classy = ClassyXml('countries.xml')

# Create a USA country element
usa = XmlElement(attributes={'name': 'USA'})
usa.rank = XmlElement(text=2)
usa.year = XmlElement(text=2012)
usa.gdppc = XmlElement(text=12345)
usa.neighbor = XmlElement(attributes={'name': 'Canada', 'direction': 'N'})
usa.neighbor = XmlElement(attributes={'name': 'Mexico', 'direction': 'S'})

# Add the USA country element the ClassyXml countries
classy.country = usa

# Save the XML file
classy.save()
```