from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
this_directory = Path(__file__).resolve().parent
readme_path = this_directory / "readme.md"
long_description = readme_path.read_text(encoding='utf-8')

setup(
    	name = 'EASYPLOT_TOOLBOX',
    	version = '2023.6',
		url = 'https://wmpjrufg.github.io/EASYPLOTPY/',
    	description = 'The Easyplotpy toolboox is an algorithm that aims to facilitate the plotting of charts for use in articles and lectures.',
		long_description = long_description,
		long_description_content_type='text/markdown',        
		keywords = ["Plot", "Learning"],
		license = 'MIT License',
        readme = 'readme.md',
		authors = ['Wanderlei Malaquias Pereira Junior', 'Sergio Francisco da Silva', 'Nilson Jorge Leão Junior', 'Mateus Pereira da Silva'],
		author_email = 'wanderlei_junior@ufcat.edu.br',
    	maintainers = ['Wanderlei Malaquias Pereira Junior', 'Mateus Pereira da Silva'],
    	install_requires = ["matplotlib", "seaborn"],
		classifiers = [	
            			'Development Status :: 4 - Beta',
            			'Topic :: Education',
                        'Topic :: Multimedia :: Graphics',
                        'License :: OSI Approved :: MIT License',
                  		'Framework :: Matplotlib', 
						'Programming Language :: Python',
                        ],
        packages = find_packages()
    )

# https://pypi.org/classifiers/
