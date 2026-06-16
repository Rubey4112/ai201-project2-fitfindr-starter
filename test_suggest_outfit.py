"""
Quick smoke test for suggest_outfit() — runs two scenarios:
  1. With a populated wardrobe (specific outfit combinations)
  2. With an empty wardrobe (general styling advice)
"""

from tools import suggest_outfit
from utils.data_loader import load_listings, get_example_wardrobe, get_empty_wardrobe


def main():
    listings = load_listings()
    new_item = listings[0]

    print("=" * 60)
    print(f"New item: {new_item['title']} (${new_item['price']})")
    print(f"Colors: {new_item['colors']}  |  Tags: {new_item['style_tags']}")
    print("=" * 60)

    # Scenario 1: wardrobe has items
    print("\n--- Scenario 1: with wardrobe ---\n")
    wardrobe = get_example_wardrobe()
    print(f"Wardrobe has {len(wardrobe['items'])} items.")
    result = suggest_outfit(new_item, wardrobe)
    print(result)

    # Scenario 2: empty wardrobe
    print("\n--- Scenario 2: empty wardrobe ---\n")
    empty = get_empty_wardrobe()
    result_empty = suggest_outfit(new_item, empty)
    print(result_empty)


if __name__ == "__main__":
    main()
