from decimal import Decimal

from shared.model import ProductModel

PRODUCTS = {
    "0ce5cb5e1c6441fbae122be083d34d77": ProductModel(
        description="A eco-friendly gaming chair made with high-quality titanium.",
        id="0ce5cb5e1c6441fbae122be083d34d77",
        price=Decimal("366.54"),
        title="Handcrafted Fitness Tracker",
    ),
    "4dffb52ec8ab46c4995b49167a50237d": ProductModel(
        description="A lightweight water bottle made with high-quality titanium.",
        id="4dffb52ec8ab46c4995b49167a50237d",
        price=Decimal("710.28"),
        title="Waterproof Camera",
    ),
    "9977fd6405bf46f7bf49990e7d5c8cb1": ProductModel(
        description="A modern smartwatch made with high-quality cotton.",
        id="9977fd6405bf46f7bf49990e7d5c8cb1",
        price=Decimal("574.06"),
        title="Modern Smartphone",
    ),
    "9ad8297d311a41c1a0af8b8097919f54": ProductModel(
        description="A eco-friendly gaming chair made with high-quality wood.",
        id="9ad8297d311a41c1a0af8b8097919f54",
        price=Decimal("913.63"),
        title="Handcrafted Speaker",
    ),
    "a85f28e763214a26ba32378bca07ec53": ProductModel(
        description="A high-performance speaker made with high-quality carbon fiber.",
        id="a85f28e763214a26ba32378bca07ec53",
        price=Decimal("798.70"),
        title="Limited Edition Backpack",
    ),
}
