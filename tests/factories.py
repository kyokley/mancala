import factory
from faker import Factory as FakerFactory

from src.mancala.player import Player

faker = FakerFactory.create()


class PlayerFactory(factory.Factory):
    name = factory.LazyAttribute(lambda x: faker.name())
    color = 'normal'

    class Meta:
        model = Player
