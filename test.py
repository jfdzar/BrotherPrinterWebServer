import brother_ql

from brother_ql.devicedependent import models, label_type_specs, label_sizes
from brother_ql.devicedependent import ENDLESS_LABEL, DIE_CUT_LABEL, ROUND_DIE_CUT_LABEL
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory, guess_backend

qlr = BrotherQLRaster('QL-500')
img = cv2.imread('logo.png')

create_label(qlr, 'logo.png', "50")

selected_backend = guess_backend('/dev/usb/lp0')
BACKEND_CLASS = backend_factory(selected_backend)['backend_class']
be = BACKEND_CLASS("/dev/usb/lp0")
be.write(qlr.data)
be.dispose()
del be
