subpackages = [
    "plot",
    "reference"
]

import lazy_loader as lazy
__getattr__, __dir__, _ = lazy.attach(__name__, subpackages)