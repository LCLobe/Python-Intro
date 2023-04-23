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
    
    planet_media = Column(Integer(), ForeignKey("planet.id"))
    character_media = Column(Integer(), ForeignKey("character.id"))
    vehicule_media = Column(Integer(), ForeignKey("vehicule.id"))

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


class Vehicule(Base):
    __tablename__ = 'vehicule'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)

    capacity = Column(String(250), nullable=True)
    speed = Column(String(250), nullable=True)
    #
    post = relationship("Post", back_populates="post.vehicule_media")

try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
