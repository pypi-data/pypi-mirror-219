# tiupy
A library to scrape data from [TIU](https://my.tiu.edu.iq) student system

## Installation

```bash
pip install tiupy
```

## Example

```python
import tiupy

client = Client()
client.login(<username>, <password>)

print(client.sid)
print(client.profile.gpa)
print(client.get_courses_data())
```
