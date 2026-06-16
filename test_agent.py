from agent import run_agent
from utils.data_loader import get_example_wardrobe

result = run_agent(
    query="vintage graphic tee under $30, size M",
    wardrobe=get_example_wardrobe(),
)
print("Fit Card:", result["fit_card"])
print("Error:", result["error"])   # None on success