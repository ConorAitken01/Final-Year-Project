# Final-Year-Project
This project was an inquiry into whether facial matching and OCR can correctly identify a person from the passport they provided and ensure the person is over 18. Underage drinking has always been a problem in Ireland and with new technology we can find ways of preventing this happening inside registered establishments. It can be hard for a bouncer to correctly identify a person from their ID but through the use of facial recognition there is a way of ensuring that the person is definitely who they say they are, and this is what this project is aiming to accomplish. With the roll out of a project like this, it could also become a feature in off licenses and shops as long as some improvements are made. 

<pre>
├───.idea
│   └───inspectionProfiles
├───dataSet
├───FaceRecognitionFiles
├───LightLevelCheck
├───OCR
└───recognizer
PS C:\Users\conor\Documents\Proof of Concept\face-match-bouncer-IDs> cd ..
PS C:\Users\conor\Documents\Proof of Concept> tree
Folder PATH listing for volume Windows-SSD
Volume serial number is 7E48-AE4E
C:.
├───.idea
│   └───inspectionProfiles
├───.vscode
├───face-match-bouncer-IDs
│   ├───.idea
│   │   └───inspectionProfiles
│   ├───dataSet
│   ├───FaceRecognitionFiles
│   ├───LightLevelCheck
│   ├───OCR
│   └───recognizer
└───venv
    ├───Lib
    │   └───site-packages
    │       ├───cv2
    │       │   └───data
    │       ├───numpy
    │       │   ├───.libs
    │       │   ├───array_api
    │       │   │   ├───tests
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───compat
    │       │   │   ├───tests
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───core
    │       │   │   ├───include
    │       │   │   │   └───numpy
    │       │   │   │       ├───libdivide
    │       │   │   │       └───random
    │       │   │   ├───lib
    │       │   │   │   └───npy-pkg-config
    │       │   │   ├───tests
    │       │   │   │   ├───data
    │       │   │   │   ├───examples
    │       │   │   │   │   ├───cython
    │       │   │   │   │   │   └───__pycache__
    │       │   │   │   │   └───limited_api
    │       │   │   │   │       └───__pycache__
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───distutils
    │       │   │   ├───checks
    │       │   │   ├───command
    │       │   │   │   └───__pycache__
    │       │   │   ├───fcompiler
    │       │   │   │   └───__pycache__
    │       │   │   ├───mingw
    │       │   │   ├───tests
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───doc
    │       │   │   └───__pycache__
    │       │   ├───f2py
    │       │   │   ├───src
    │       │   │   ├───tests
    │       │   │   │   ├───src
    │       │   │   │   │   ├───abstract_interface
    │       │   │   │   │   ├───array_from_pyobj
    │       │   │   │   │   ├───assumed_shape
    │       │   │   │   │   ├───block_docstring
    │       │   │   │   │   ├───callback
    │       │   │   │   │   ├───cli
    │       │   │   │   │   ├───common
    │       │   │   │   │   ├───crackfortran
    │       │   │   │   │   ├───f2cmap
    │       │   │   │   │   ├───kind
    │       │   │   │   │   ├───mixed
    │       │   │   │   │   ├───module_data
    │       │   │   │   │   ├───negative_bounds
    │       │   │   │   │   ├───parameter
    │       │   │   │   │   ├───quoted_character
    │       │   │   │   │   ├───regression
    │       │   │   │   │   ├───return_character
    │       │   │   │   │   ├───return_complex
    │       │   │   │   │   ├───return_integer
    │       │   │   │   │   ├───return_logical
    │       │   │   │   │   ├───return_real
    │       │   │   │   │   ├───size
    │       │   │   │   │   ├───string
    │       │   │   │   │   └───value_attrspec
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───fft
    │       │   │   ├───tests
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───lib
    │       │   │   ├───tests
    │       │   │   │   ├───data
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───linalg
    │       │   │   ├───tests
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───ma
    │       │   │   ├───tests
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───matrixlib
    │       │   │   ├───tests
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───polynomial
    │       │   │   ├───tests
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───random
    │       │   │   ├───lib
    │       │   │   ├───tests
    │       │   │   │   ├───data
    │       │   │   │   │   └───__pycache__
    │       │   │   │   └───__pycache__
    │       │   │   ├───_examples
    │       │   │   │   ├───cffi
    │       │   │   │   │   └───__pycache__
    │       │   │   │   ├───cython
    │       │   │   │   │   └───__pycache__
    │       │   │   │   └───numba
    │       │   │   │       └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───testing
    │       │   │   ├───tests
    │       │   │   │   └───__pycache__
    │       │   │   ├───_private
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───tests
    │       │   │   └───__pycache__
    │       │   ├───typing
    │       │   │   ├───tests
    │       │   │   │   ├───data
    │       │   │   │   │   ├───fail
    │       │   │   │   │   ├───misc
    │       │   │   │   │   ├───pass
    │       │   │   │   │   │   └───__pycache__
    │       │   │   │   │   └───reveal
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───_pyinstaller
    │       │   │   └───__pycache__
    │       │   ├───_typing
    │       │   │   └───__pycache__
    │       │   └───__pycache__
    │       ├───numpy-1.24.2.dist-info
    │       ├───opencv_contrib_python-4.6.0.66.dist-info
    │       ├───opencv_python-4.6.0.66.dist-info
    │       ├───packaging
    │       │   └───__pycache__
    │       ├───packaging-23.0.dist-info
    │       ├───PIL
    │       │   └───__pycache__
    │       ├───Pillow-9.4.0.dist-info
    │       ├───pip
    │       │   ├───_internal
    │       │   │   ├───cli
    │       │   │   │   └───__pycache__
    │       │   │   ├───commands
    │       │   │   │   └───__pycache__
    │       │   │   ├───distributions
    │       │   │   │   └───__pycache__
    │       │   │   ├───index
    │       │   │   │   └───__pycache__
    │       │   │   ├───locations
    │       │   │   │   └───__pycache__
    │       │   │   ├───metadata
    │       │   │   │   ├───importlib
    │       │   │   │   └───__pycache__
    │       │   │   ├───models
    │       │   │   │   └───__pycache__
    │       │   │   ├───network
    │       │   │   │   └───__pycache__
    │       │   │   ├───operations
    │       │   │   │   ├───build
    │       │   │   │   │   └───__pycache__
    │       │   │   │   ├───install
    │       │   │   │   │   └───__pycache__
    │       │   │   │   └───__pycache__
    │       │   │   ├───req
    │       │   │   │   └───__pycache__
    │       │   │   ├───resolution
    │       │   │   │   ├───legacy
    │       │   │   │   ├───resolvelib
    │       │   │   │   │   └───__pycache__
    │       │   │   │   └───__pycache__
    │       │   │   ├───utils
    │       │   │   │   └───__pycache__
    │       │   │   ├───vcs
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   ├───_vendor
    │       │   │   ├───cachecontrol
    │       │   │   │   ├───caches
    │       │   │   │   │   └───__pycache__
    │       │   │   │   └───__pycache__
    │       │   │   ├───certifi
    │       │   │   │   └───__pycache__
    │       │   │   ├───chardet
    │       │   │   │   ├───cli
    │       │   │   │   ├───metadata
    │       │   │   │   └───__pycache__
    │       │   │   ├───colorama
    │       │   │   ├───distlib
    │       │   │   │   └───__pycache__
    │       │   │   ├───distro
    │       │   │   ├───idna
    │       │   │   │   └───__pycache__
    │       │   │   ├───msgpack
    │       │   │   │   └───__pycache__
    │       │   │   ├───packaging
    │       │   │   │   └───__pycache__
    │       │   │   ├───pep517
    │       │   │   │   ├───in_process
    │       │   │   │   │   └───__pycache__
    │       │   │   │   └───__pycache__
    │       │   │   ├───pkg_resources
    │       │   │   │   └───__pycache__
    │       │   │   ├───platformdirs
    │       │   │   │   └───__pycache__
    │       │   │   ├───pygments
    │       │   │   │   ├───filters
    │       │   │   │   │   └───__pycache__
    │       │   │   │   ├───formatters
    │       │   │   │   ├───lexers
    │       │   │   │   │   └───__pycache__
    │       │   │   │   ├───styles
    │       │   │   │   │   └───__pycache__
    │       │   │   │   └───__pycache__
    │       │   │   ├───pyparsing
    │       │   │   │   ├───diagram
    │       │   │   │   └───__pycache__
    │       │   │   ├───requests
    │       │   │   │   └───__pycache__
    │       │   │   ├───resolvelib
    │       │   │   │   ├───compat
    │       │   │   │   │   └───__pycache__
    │       │   │   │   └───__pycache__
    │       │   │   ├───rich
    │       │   │   │   └───__pycache__
    │       │   │   ├───tenacity
    │       │   │   │   └───__pycache__
    │       │   │   ├───tomli
    │       │   │   │   └───__pycache__
    │       │   │   ├───urllib3
    │       │   │   │   ├───contrib
    │       │   │   │   │   ├───_securetransport
    │       │   │   │   │   └───__pycache__
    │       │   │   │   ├───packages
    │       │   │   │   │   ├───backports
    │       │   │   │   │   └───__pycache__
    │       │   │   │   ├───util
    │       │   │   │   │   └───__pycache__
    │       │   │   │   └───__pycache__
    │       │   │   ├───webencodings
    │       │   │   └───__pycache__
    │       │   └───__pycache__
    │       ├───pip-22.3.1.dist-info
    │       ├───pkg_resources
    │       │   ├───extern
    │       │   │   └───__pycache__
    │       │   ├───_vendor
    │       │   │   ├───importlib_resources
    │       │   │   ├───jaraco
    │       │   │   │   ├───text
    │       │   │   │   │   └───__pycache__
    │       │   │   │   └───__pycache__
    │       │   │   ├───more_itertools
    │       │   │   │   └───__pycache__
    │       │   │   ├───packaging
    │       │   │   │   └───__pycache__
    │       │   │   ├───pyparsing
    │       │   │   │   ├───diagram
    │       │   │   │   └───__pycache__
    │       │   │   └───__pycache__
    │       │   └───__pycache__
    │       ├───pytesseract
    │       │   └───__pycache__
    │       ├───pytesseract-0.3.10.dist-info
    │       ├───setuptools
    │       │   ├───command
    │       │   ├───config
    │       │   │   └───_validate_pyproject
    │       │   ├───extern
    │       │   ├───_distutils
    │       │   │   └───command
    │       │   └───_vendor
    │       │       ├───importlib_metadata
    │       │       ├───importlib_resources
    │       │       ├───jaraco
    │       │       │   └───text
    │       │       ├───more_itertools
    │       │       ├───packaging
    │       │       ├───pyparsing
    │       │       │   └───diagram
    │       │       └───tomli
    │       ├───setuptools-65.5.1.dist-info
    │       ├───wheel
    │       │   ├───cli
    │       │   └───vendored
    │       │       └───packaging
    │       ├───wheel-0.38.4.dist-info
    │       ├───_distutils_hack
    │       │   └───__pycache__
    │       └───__pycache__
    └───Scripts

</pre>

# References
- Face Recognition: https://gbansal103.medium.com/simple-python-code-for-match-matching-for-beginners-face-detection-and-face-recognition-eec9d41a1195
- Tkinter GUI: https://www.geeksforgeeks.org/create-first-gui-application-using-python-tkinter/
