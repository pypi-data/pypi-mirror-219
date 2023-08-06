from setuptools import setup

setup(
    name='jarvis_assistant_bot',
    version='1.0',
    description='Welcome to Jarvis, your personal assistant! Jarvis is here to help you stay organized and manage your contacts, reminders, notes, and files efficiently.',
    author='Python Forces',
    url='https://github.com/UkrainianEagleOwl/tp_personal_assistant/tree/97c820e0779d54e488d5d824cce404b06bb4e654',
    packages=['src','game'],
    
    entry_points={
        'console_scripts': [
            'Jarvis=src.main:main',
        ],
    },
    install_requires=[
        'prettytable',
        'prompt_toolkit',
        'colorama',
        'cryptography',
        'openai',
        'keyboard',
        'pygame'
    ],
)
