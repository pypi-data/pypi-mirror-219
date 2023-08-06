from setuptools import setup

with open('README.md', 'rt') as arq:
      readme = arq.read()


keywords = [
      'EventSimpleGUI'.lower(), 'EventSimpleGUI', 'simplegui', 'GUI', 'gui', 'events for simplegui', 'event handler simple gui',
      'generate events', 'fast events', 'events'
]

setup(name='EventSimpleGUI',
      url='https://github.com/MikalROn/EventSimpleGUI',
      version='0.3.1',
      license='MIT license',
      author='Daniel Coêlho',
      long_description=readme,
      long_description_content_type='text/markdown',
      author_email='heromon.9010@gmail.com',
      keywords=keywords,
      description='A simple tool to create events to PySimpleGUI',
      packages=['pysimpleevent'],
      install_requires=['PySimpleGUI'],
      python_requires='>=3',
      project_urls={
            'Tests': 'https://smokeshow.helpmanual.io/474z2x1c0s2u3j101i26/',
            'Source': 'https://github.com/MikalROn/EventSimpleGUI',
            'Demos': 'https://github.com/MikalROn/EventSimpleGUI/tree/main/demos',
            'Docs': 'https://mikalron.github.io/EventSimpleGUI/'
      }
)
