"""
Quick smoke test for create_fit_card() — runs two scenarios:
  1. With a valid outfit string (normal caption generation)
  2. With an empty outfit string (error guard check)
"""

from tools import suggest_outfit, create_fit_card
from utils.data_loader import load_listings, get_example_wardrobe


def main():
    listings = load_listings()
    new_item = listings[0]

    print("=" * 60)
    print(f"New item: {new_item['title']} (${new_item['price']})")
    print(f"Platform: {new_item['platform']}")
    print("=" * 60)

    # Scenario 1: valid outfit → generate caption
    print("\n--- Scenario 1: valid outfit string ---\n")
    wardrobe = get_example_wardrobe()
    outfit = suggest_outfit(new_item, wardrobe)
    print(f"Outfit suggestion:\n{outfit}\n")
    print("Fit card caption:")
    caption = create_fit_card(outfit, new_item)
    print(caption)

    # Scenario 2: empty outfit → error guard
    print("\n--- Scenario 2: empty outfit string ---\n")
    result = create_fit_card("", new_item)
    print(result)


if __name__ == "__main__":
    main()
