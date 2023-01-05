# TWDOWN API
Twitter video downloader(unofficial).

## Usage
1. **Get PyPi Package**
```bash
pip install -U twdown
```

2. **Quick start**

```python
from twdown import TwdownAPI
  
if __name__ == "__main__":  
    twdown = TwdownAPI("https://twitter.com/karenxcheng/status/1554864997586505729")  
    twdown.run()
```
