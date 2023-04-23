import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column("id", Integer(), primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False) #Encript
    
    favourite_posts = relationship("Favourites", back_populates="post_id")
    owned_posts = relationship("Post", back_populates="owner_id")
    
    #Relationship: procedencia info. objeto a incluir
    # params: 1. tabla a relacionar. 2. contenido a popular
    # Una relaci'on debe ser bidireccional
    # Para ello se usa el relationship+foreingkey (uno a muchos)

class Favourites(Base):
    __tablename__ = 'favourite'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("post.id"))
    
    #Tablas intermedias solo foreingn keys

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer(), primary_key=True)
    owner_id = Column(Integer(), ForeignKey("user.id"))
    
    content = Column(String(250), unique=False, nullable=True)
    planet_media = relationship("Planet", back_populates="planet.post")
    character_media = relationship("Character", back_populates="character.post")
    #post_properties = (String(250), nullable=Falsle) #stringify(objecto propiedades)
    #
    #media_id = Column(Integer(), ForeignKey("planet.id"), ForeignKey("character.id"))
    #

    favourites = relationship("Favourites", back_populates="favourites.post")
    
    



class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)

    terrain = Column(String(250), nullable=True)
    gravity = Column(String(250), nullable=True)
    radius = Column(String(250), nullable=True)
    #
    post = relationship("Post", back_populates="post.planet_media")
    #
    born_here = relationship("Character", back_populates="character.id")
    
   

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)

    lastname = Column(String(250), nullable=True)
    birthdate = Column(String(250), nullable=True)
    gender = Column(String(250), nullable=True)
    eye_color = Column(String(250), nullable=True)
    #
    post = relationship("Post", back_populates="post.character_media")
    #
    origin_planet = Column(Integer(), ForeignKey("planet.id"))

    
   
# class Media(Base):
#     __tablename__ = 'media'
#     id = Column(Integer(), primary_key=True)
#     type = Column(Enum(), nullable=False)
#     url = Column(String(250), nullable=False)
#     post_id = Column(Integer(), ForeignKey("post.id"))
#     post = relationship("Post", back_populates="media")

#     def to_dict(self):
#         return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
