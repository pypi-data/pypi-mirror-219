# remote-drawing-provider

## install

```bash
pip install remote-drawing-provider
```

## using

```python
import torch
from remote_drawing_provider.provider import send

args = {
    'point_cloud': torch.randn(1000,3)
}
send(method='visualize_point_cloud', **args)
```
