from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# this_directory = Path(__file__).parent
# long_description = (this_directory / "README.md").read_text()

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8", mode='rb', errors='ignore') as fh:
#     long_description = fh.read()

# long_description = ""
# with open("README.md", 'r') as f:
#   long_description = f.read()
#   print(long_description)

VERSION = '0.1.2'
DESCRIPTION = 'Transforming multiple certificates and images with personalized text has never been easier thanks to the all-new Image Bulk Editor.'
LONG_DESCRIPTION = 'Batch Processing: Our Image Bulk Editor allows you to process multiple certificates or images simultaneously. No need to edit each file individually; simply upload your entire collection, and the tool will automatically apply your customizations to all the files. Custom Text Fields: Effortlessly insert names, dates, or any other custom text onto your certificates or images. Our editor provides intuitive text fields that can be easily filled with the desired information. You can choose from various fonts, sizes, and colors to match your preferences. Dynamic Variables: To further enhance personalization, we offer dynamic variables that automatically populate data across multiple files. For example, if you have a list of names, our tool can dynamically fill in each name in the designated areas, ensuring accuracy and consistency throughout the batch. Easy Alignment and Positioning: Achieve precise placement of text or custom elements on your certificates or images using our user-friendly alignment and positioning tools. You can adjust the position, rotation, and size of the elements to fit your design perfectly. Preview and Quality Control: Before finalizing your edits, our Image Bulk Editor enables you to preview each modified file. This allows you to ensure that the personalized text or customizations are accurately applied to every certificate or image. Additionally, you can compare the original and edited versions side by side to verify the changes. Export Options: Once you are satisfied with the edits, the Image Bulk Editor provides flexible export options. You can choose to save each edited file individually or merge them into a single document or image, making it convenient for distribution or archiving purposes. Time-Saving Efficiency: Image Bulk Editor is designed to streamline your workflow, significantly reducing the time and effort required for editing multiple certificates or images. Whether you are managing a large event, running an educational program, or organizing corporate achievements, our tool empowers you to process bulk customization quickly and accurately.'

# Setting up
setup(
    include_package_data=True,
    name="bulk_editor",
    version=VERSION,
    url="https://github.com/Hari-Nikesh-R/Bulk-Image-Editor",
    author="Hari Nikesh R",
    author_email="hari.nikesh.r.cce@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="# Image Bulk Editor Python Package\n\nThe Image Bulk Editor Python Package provides a convenient and efficient way to customize multiple certificates and images with personalized text or custom elements. This package simplifies the process of batch editing by automating the application of changes across multiple files, saving you valuable time and effort.\n\n# Installation\n\nTo install the Image Bulk Editor Python Package, use the following command:\n```bash\npip install BulkImageEditor\n```\n\n# Usage\n\nTo use the Image Bulk Editor Python Package, follow these steps:\n\n- Import the necessary modules:\n\n```python\nfrom bulkeditor import BulkEditor\n```\n\n- Create an instance and start of the bulk editor:\n```python\nBulkEditor()\n```\n\n# Example\n```python\nfrom bulkeditor import BulkEditor\nBulkEditor()\n```\n\n# Conclusion\n\nThe Image Bulk Editor Python Package simplifies the task of customizing multiple certificates and images by automating the batch editing process. With its intuitive usage and comprehensive features, this package allows you to achieve consistent and professional results efficiently.\n\n# License\n\nThis is under MIT License.",
    packages=find_packages(),
    package_data={'bulkeditor': ['Certificate.txt', 'logo.png', 'Roboto-Bold.ttf']},
    install_requires=['opencv-python', 'Pillow'],
    keywords=['python','editor', 'bulk editor', 'certificate editor', 'image writer'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ])