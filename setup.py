from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return the list of requirements 
    from the requirements.txt file.
    """
    requirement_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read lines from requirements.txt
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                # Ignore empty lines and '-e .' which is handled by pip
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
        
    return requirement_list

setup(
    name="PropSight360",
    version="0.0.1",
    author="Shravan Kumar Pandey",
    author_email="shravankumarpandy825412@gmail.com",
    description="An AI-powered real estate analytics and price prediction engine for Gurgaon.",
    packages=find_packages(),
    install_requires=get_requirements(),
)