import sys
import mediapipe
print(sys.executable)
print(mediapipe)
print(getattr(mediapipe, '__file__', None))
print(getattr(mediapipe, '__version__', 'unknown'))
print('has solutions:', hasattr(mediapipe, 'solutions'))
print('module path:', getattr(mediapipe, '__path__', None))
print('dir sample:', [x for x in dir(mediapipe) if x.startswith('sol')][:20])
